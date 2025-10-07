"""
Generator Service - Orchestrate the full code generation pipeline.

This module coordinates all generation steps from pattern parsing through
code assembly, with LangSmith tracing for observability.

REFACTORED (Epic 4.5): Now uses LLM-first 3-stage pipeline instead of 8-stage template-based approach.
"""

import time
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

# Try to import LangSmith for tracing (optional dependency)
try:
    from langsmith import traceable
    LANGSMITH_AVAILABLE = True
except ImportError:
    # Create a no-op decorator if LangSmith is not available
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    LANGSMITH_AVAILABLE = False

from .types import (
    GenerationRequest,
    GenerationResult,
    GenerationStage,
    GenerationMetadata,
    ValidationMetadata,
    CodeParts
)
from .pattern_parser import PatternParser
from .code_assembler import CodeAssembler
from .provenance import ProvenanceGenerator

# New LLM-first components
from .prompt_builder import PromptBuilder
from .llm_generator import LLMComponentGenerator, MockLLMGenerator
from .code_validator import CodeValidator
from .exemplar_loader import ExemplarLoader


class GeneratorService:
    """
    Orchestrate the full code generation pipeline with tracing.
    
    NEW (Epic 4.5): 3-stage LLM-first pipeline:
    1. LLM Generation - Single pass with full context
    2. Validation - TypeScript/ESLint with LLM fixes
    3. Post-Processing - Imports, provenance, formatting
    """
    
    def __init__(
        self,
        patterns_dir: Optional[Path] = None,
        use_llm: bool = True,
        api_key: Optional[str] = None,
    ):
        """
        Initialize generator service.
        
        Args:
            patterns_dir: Optional custom patterns directory
            use_llm: Whether to use LLM generation (True) or mock (False)
            api_key: Optional OpenAI API key
        """
        # Core components
        self.pattern_parser = PatternParser(patterns_dir)
        self.code_assembler = CodeAssembler()
        self.provenance_generator = ProvenanceGenerator()
        
        # New LLM-first components
        self.prompt_builder = PromptBuilder()
        self.exemplar_loader = ExemplarLoader()
        
        # Initialize LLM generator
        if use_llm and (api_key or os.getenv("OPENAI_API_KEY")):
            try:
                self.llm_generator = LLMComponentGenerator(api_key=api_key)
            except Exception:
                # Fall back to mock if LLM initialization fails
                self.llm_generator = MockLLMGenerator()
        else:
            self.llm_generator = MockLLMGenerator()
        
        # Initialize code validator with LLM generator
        self.code_validator = CodeValidator(llm_generator=self.llm_generator)
        
        # Track current stage for progress updates
        self.current_stage = GenerationStage.LLM_GENERATING
        self.stage_latencies: Dict[GenerationStage, int] = {}
    
    def _normalize_requirements(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Convert requirements list to dict format expected by backend.

        Frontend sends: [{name, category, approved}, ...]
        Backend expects: {props: [], events: [], states: [], accessibility: []}

        Args:
            requirements: List of requirement objects with category field

        Returns:
            Dict organized by category
        """
        result = {
            "props": [],
            "events": [],
            "states": [],
            "accessibility": [],
            "validation": [],
            "variants": []
        }

        for req in requirements:
            category = req.get("category", "props")
            # Map frontend categories to backend categories
            if category in result:
                result[category].append(req)

        return result

    @traceable(run_type="chain", name="generate_component")
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate component code from pattern, tokens, and requirements.

        This is the main entry point for code generation.

        Args:
            request: GenerationRequest with pattern_id, tokens, requirements

        Returns:
            GenerationResult with generated code and metadata
        """
        start_time = time.time()

        # Normalize requirements from list to dict format
        requirements_dict = self._normalize_requirements(request.requirements)

        try:
            # Stage 1: Parse Pattern
            pattern_structure = await self._parse_pattern(request.pattern_id)
            
            # Stage 2: Inject Tokens
            token_mapping = await self._inject_tokens(
                pattern_structure.code,
                request.tokens,
                self._infer_component_type(request.pattern_id)
            )
            
            # Stage 3: Generate Tailwind Classes
            tailwind_classes = await self._generate_tailwind(
                request.tokens,
                pattern_structure
            )
            
            # Stage 4: Implement Requirements
            requirement_impl = await self._implement_requirements(
                pattern_structure.code,
                requirements_dict,
                pattern_structure.component_name
            )
            
            # Stage 4.5: Enhance Accessibility
            enhanced_code = self._enhance_accessibility(
                pattern_structure.code,
                self._infer_component_type(request.pattern_id),
                pattern_structure.component_name
            )
            
            # Stage 4.6: Generate TypeScript Types
            typed_code = self._generate_types(
                enhanced_code,
                pattern_structure.component_name,
                requirements_dict.get("props", [])
            )

            # Stage 4.7: Generate Storybook Stories
            stories = self._generate_storybook_stories(
                pattern_structure.component_name,
                pattern_structure.variants,
                requirements_dict.get("props", []),
                self._infer_component_type(request.pattern_id)
            )
            
            # Stage 5: Assemble Code
            code_parts = self._build_code_parts(
                pattern_structure,
                token_mapping,
                requirement_impl,
                request.component_name,
                request.pattern_id,
                request.tokens,
                requirements_dict,
                typed_code,
                stories
            )
            
            result_files = await self._assemble_code(code_parts)
            
            # Calculate total latency
            total_latency_ms = int((time.time() - start_time) * 1000)
            
            # Build metadata
            metadata = GenerationMetadata(
                latency_ms=total_latency_ms,
                stage_latencies=self.stage_latencies,
                token_count=len(request.tokens.get("colors", {})) + 
                           len(request.tokens.get("typography", {})) +
                           len(request.tokens.get("spacing", {})),
                lines_of_code=len(result_files["component"].split("\n")),
                requirements_implemented=len(requirements_dict.get("props", []))
            )
            
            # Build successful result
            return GenerationResult(
                component_code=result_files["component"],
                stories_code=result_files.get("stories", ""),
                files=result_files["files"],
                metadata=metadata,
                success=True,
                error=None
            )
        
        except Exception as e:
            # Handle errors gracefully
            error_latency_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                component_code="",
                stories_code="",
                files={},
                metadata=GenerationMetadata(
                    latency_ms=error_latency_ms,
                    stage_latencies=self.stage_latencies
                ),
                success=False,
                error=str(e)
            )
    
    @traceable(run_type="tool", name="parse_pattern")
    async def _parse_pattern(self, pattern_id: str):
        """Parse pattern and track latency."""
        self.current_stage = GenerationStage.PARSING
        stage_start = time.time()
        
        try:
            result = self.pattern_parser.parse(pattern_id)
            return result
        finally:
            self.stage_latencies[GenerationStage.PARSING] = int(
                (time.time() - stage_start) * 1000
            )
    
    @traceable(run_type="tool", name="inject_tokens")
    async def _inject_tokens(self, pattern_code: str, tokens: Dict[str, Any], component_type: str):
        """Inject tokens and track latency."""
        self.current_stage = GenerationStage.INJECTING
        stage_start = time.time()
        
        try:
            result = self.token_injector.inject(pattern_code, tokens, component_type)
            return result
        finally:
            self.stage_latencies[GenerationStage.INJECTING] = int(
                (time.time() - stage_start) * 1000
            )
    
    @traceable(run_type="tool", name="generate_tailwind")
    async def _generate_tailwind(self, tokens: Dict[str, Any], pattern_structure):
        """Generate Tailwind classes and track latency."""
        self.current_stage = GenerationStage.GENERATING
        stage_start = time.time()
        
        try:
            # Generate classes for main component
            component_type = self._infer_component_type_from_name(
                pattern_structure.component_name
            )
            
            classes = self.tailwind_generator.generate_classes(
                element=component_type,
                tokens=tokens,
                variant="default"
            )
            return classes
        finally:
            self.stage_latencies[GenerationStage.GENERATING] = int(
                (time.time() - stage_start) * 1000
            )
    
    @traceable(run_type="tool", name="implement_requirements")
    async def _implement_requirements(
        self,
        component_code: str,
        requirements: Dict[str, Any],
        component_name: str
    ):
        """Implement requirements and track latency."""
        self.current_stage = GenerationStage.IMPLEMENTING
        stage_start = time.time()
        
        try:
            result = self.requirement_implementer.implement(
                component_code,
                requirements,
                component_name
            )
            return result
        finally:
            self.stage_latencies[GenerationStage.IMPLEMENTING] = int(
                (time.time() - stage_start) * 1000
            )
    
    @traceable(run_type="tool", name="assemble_code")
    async def _assemble_code(self, code_parts: CodeParts):
        """Assemble and format code, track latency."""
        self.current_stage = GenerationStage.ASSEMBLING
        stage_start = time.time()
        
        try:
            result = await self.code_assembler.assemble(code_parts)
            return result
        finally:
            self.stage_latencies[GenerationStage.ASSEMBLING] = int(
                (time.time() - stage_start) * 1000
            )
            self.current_stage = GenerationStage.COMPLETE
    
    def _build_code_parts(
        self,
        pattern_structure,
        token_mapping,
        requirement_impl,
        custom_component_name: Optional[str],
        pattern_id: str,
        tokens: Dict[str, Any],
        requirements: Dict[str, Any],
        enhanced_code: str,
        stories: str
    ) -> CodeParts:
        """Build CodeParts from all generated components."""
        component_name = custom_component_name or pattern_structure.component_name
        
        # Generate provenance header with full metadata
        provenance_header = self.provenance_generator.generate_header(
            pattern_id=pattern_id,
            tokens=tokens,
            requirements=requirements,
            component_name=component_name
        )
        
        # NOTE: enhanced_code already contains the full component including types
        # Don't add requirement_impl["props_interface"] as it would duplicate types
        return CodeParts(
            provenance_header=provenance_header,
            imports=[],  # Pattern code already has imports
            css_variables=token_mapping.css_variables,
            type_definitions="",  # Don't duplicate - enhanced_code has types
            component_code=enhanced_code,  # Complete component code
            storybook_stories=stories,
            component_name=component_name
        )
    
    def _enhance_accessibility(
        self,
        component_code: str,
        component_type: str,
        component_name: str
    ) -> str:
        """Enhance component with accessibility features."""
        return self.a11y_enhancer.enhance(
            component_code,
            component_type,
            component_name
        )
    
    def _generate_types(
        self,
        component_code: str,
        component_name: str,
        props: List[Dict[str, Any]]
    ) -> str:
        """Generate TypeScript types for component."""
        return self.type_generator.generate_types(
            component_code,
            component_name,
            props
        )
    
    def _generate_storybook_stories(
        self,
        component_name: str,
        variants: List[str],
        props: List[Dict[str, Any]],
        component_type: str
    ) -> str:
        """Generate Storybook stories for component."""
        return self.storybook_generator.generate_stories(
            component_name,
            variants,
            props,
            component_type
        )
    
    def _generate_basic_story(self, component_name: str) -> str:
        """Generate basic Storybook story (full implementation in P5)."""
        return f"""import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {component_name} }} from './{component_name}';

const meta: Meta<typeof {component_name}> = {{
  title: 'Components/{component_name}',
  component: {component_name},
  tags: ['autodocs'],
}};

export default meta;
type Story = StoryObj<typeof {component_name}>;

export const Default: Story = {{
  args: {{
    children: '{component_name}',
  }},
}};
"""
    
    # ====== NEW LLM-FIRST HELPER METHODS ======
    
    async def _parse_pattern_for_reference(self, pattern_id: str):
        """Load pattern as reference (not for modification)."""
        return self.pattern_parser.parse(pattern_id)
    
    def _build_generation_prompt(
        self,
        pattern_code: str,
        component_name: str,
        component_type: str,
        tokens: Dict[str, Any],
        requirements: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Build comprehensive generation prompt using PromptBuilder.
        
        Returns:
            Dict with 'system' and 'user' prompts
        """
        return self.prompt_builder.build_prompt(
            pattern_code=pattern_code,
            component_name=component_name,
            component_type=component_type,
            tokens=tokens,
            requirements=requirements,
        )
    
    def _add_provenance(
        self,
        code: str,
        component_name: str,
        pattern_id: str,
        tokens: Dict[str, Any],
        requirements: Dict[str, Any],
    ) -> str:
        """Add provenance header to generated code."""
        header = self.provenance_generator.generate_header(
            component_name=component_name,
            pattern_id=pattern_id,
            tokens=tokens,
            requirements=requirements,
        )
        return f"{header}\n\n{code}"
    
    def _infer_component_type(self, pattern_id: str) -> str:
        """Infer component type from pattern ID."""
        # Extract type from pattern ID (e.g., "shadcn-button" -> "button")
        return pattern_id.replace("shadcn-", "").lower()
    
    def _infer_component_type_from_name(self, component_name: str) -> str:
        """Infer component type from component name."""
        return component_name.lower()
    
    def get_current_stage(self) -> GenerationStage:
        """Get current generation stage for progress tracking."""
        return self.current_stage
    
    def get_stage_latencies(self) -> Dict[GenerationStage, int]:
        """Get latency for each stage."""
        return self.stage_latencies.copy()
