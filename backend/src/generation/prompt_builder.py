"""
Prompt Builder for LLM Code Generation

Constructs comprehensive prompts for generating React/TypeScript components.
Includes pattern reference, design tokens, requirements, and examples.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json

# Try to import tiktoken for accurate token counting
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


@dataclass
class PromptTemplate:
    """Template for LLM prompts."""
    system_prompt: str
    user_prompt_template: str
    version: str = "1.0.0"


class PromptBuilder:
    """
    Build comprehensive prompts for component generation.
    
    Constructs prompts that include:
    - Pattern reference code
    - Design tokens with semantic meaning
    - Requirements (props, events, states, a11y)
    - Component naming and conventions
    - Validation constraints
    """
    
    # System prompt that defines the AI's role and capabilities
    SYSTEM_PROMPT = """You are an expert React and TypeScript developer specializing in creating accessible, production-ready UI components following shadcn/ui conventions.

Your expertise includes:
- Writing clean, type-safe TypeScript with strict mode (no 'any' types)
- Creating accessible components with proper ARIA attributes
- Following React best practices and modern patterns
- Implementing design systems with design tokens
- Writing comprehensive Storybook stories

You generate complete, working component code that compiles without errors."""

    # Template for the user prompt
    USER_PROMPT_TEMPLATE = """## Task
Generate a production-ready React component based on the requirements below.

## Reference Pattern (shadcn/ui)
Use this pattern as a reference for style and structure. DO NOT copy it directly - adapt it to meet the specific requirements.

```tsx
{pattern_code}
```

## Component Information
**Name**: {component_name}
**Type**: {component_type}
**Description**: {component_description}

## Design Tokens
Apply these design tokens to the component using CSS variables.

{design_tokens}

## Requirements

### Props
{props_requirements}

### Events
{events_requirements}

### States
{states_requirements}

### Accessibility
{accessibility_requirements}

## Constraints
- TypeScript strict mode (no 'any' types allowed)
- All props must have explicit types
- Include proper ARIA attributes for accessibility
- Use design tokens via CSS variables (e.g., var(--color-primary))
- Follow shadcn/ui naming conventions
- Export component with displayName set
- Include proper JSDoc comments for props
- Component must compile without TypeScript errors
- Component must pass ESLint validation

## Output Format
Return a JSON object with the following structure:
{{
  "component_code": "complete .tsx file content",
  "stories_code": "complete .stories.tsx file content for Storybook",
  "imports": ["list of import statements"],
  "exports": ["list of exported names"],
  "explanation": "brief explanation of key implementation decisions"
}}

Generate complete, working code that meets all requirements."""

    def __init__(self):
        """Initialize prompt builder."""
        self.template = PromptTemplate(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt_template=self.USER_PROMPT_TEMPLATE,
        )
    
    def build_prompt(
        self,
        pattern_code: str,
        component_name: str,
        component_type: str,
        tokens: Dict[str, Any],
        requirements: Dict[str, Any],
        component_description: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Build a complete prompt for component generation.
        
        Args:
            pattern_code: Reference pattern code (shadcn/ui)
            component_name: Name of the component to generate
            component_type: Type (button, card, input, etc.)
            tokens: Design tokens (colors, typography, spacing)
            requirements: Component requirements (props, events, states, a11y)
            component_description: Optional description of the component
        
        Returns:
            Dict with 'system' and 'user' prompts
        """
        # Format design tokens
        tokens_str = self._format_design_tokens(tokens)
        
        # Format requirements by category
        props_str = self._format_requirements(
            requirements.get("props", []),
            "No specific props required. Use common patterns for this component type."
        )
        
        events_str = self._format_requirements(
            requirements.get("events", []),
            "No specific events required. Include standard event handlers."
        )
        
        states_str = self._format_requirements(
            requirements.get("states", []),
            "No specific state requirements. Use appropriate state management."
        )
        
        a11y_str = self._format_requirements(
            requirements.get("accessibility", []),
            "Follow WCAG 2.1 AA standards with proper ARIA attributes."
        )
        
        # Build user prompt
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            pattern_code=pattern_code,
            component_name=component_name,
            component_type=component_type,
            component_description=component_description or f"A {component_type} component",
            design_tokens=tokens_str,
            props_requirements=props_str,
            events_requirements=events_str,
            states_requirements=states_str,
            accessibility_requirements=a11y_str,
        )
        
        return {
            "system": self.SYSTEM_PROMPT,
            "user": user_prompt,
        }
    
    def _format_design_tokens(self, tokens: Dict[str, Any]) -> str:
        """Format design tokens for the prompt."""
        sections = []
        
        # Format colors
        if "colors" in tokens and tokens["colors"]:
            colors = tokens["colors"]
            color_lines = []
            for name, value in colors.items():
                color_lines.append(f"  - {name}: {value}")
            sections.append("**Colors:**\n" + "\n".join(color_lines))
        
        # Format typography
        if "typography" in tokens and tokens["typography"]:
            typo = tokens["typography"]
            typo_lines = []
            for key, value in typo.items():
                typo_lines.append(f"  - {key}: {value}")
            sections.append("**Typography:**\n" + "\n".join(typo_lines))
        
        # Format spacing
        if "spacing" in tokens and tokens["spacing"]:
            spacing = tokens["spacing"]
            spacing_lines = []
            for key, value in spacing.items():
                spacing_lines.append(f"  - {key}: {value}")
            sections.append("**Spacing:**\n" + "\n".join(spacing_lines))
        
        # Format borders
        if "borders" in tokens and tokens["borders"]:
            borders = tokens["borders"]
            border_lines = []
            for key, value in borders.items():
                border_lines.append(f"  - {key}: {value}")
            sections.append("**Borders:**\n" + "\n".join(border_lines))
        
        if not sections:
            return "No specific design tokens provided. Use sensible defaults."
        
        return "\n\n".join(sections)
    
    def _format_requirements(
        self, 
        requirements: List[Dict[str, Any]], 
        default_message: str
    ) -> str:
        """Format requirements list for the prompt."""
        if not requirements:
            return default_message
        
        lines = []
        for req in requirements:
            # Handle different requirement formats
            if isinstance(req, dict):
                name = req.get("name", "")
                req_type = req.get("type", "")
                description = req.get("description", "")
                
                if name:
                    line = f"- **{name}**"
                    if req_type:
                        line += f" ({req_type})"
                    if description:
                        line += f": {description}"
                    lines.append(line)
            elif isinstance(req, str):
                lines.append(f"- {req}")
        
        return "\n".join(lines) if lines else default_message
    
    def estimate_token_count(self, prompts: Dict[str, str]) -> int:
        """
        Estimate token count for the prompts.
        
        Uses tiktoken for accurate counting if available, otherwise falls back
        to rough estimate (~4 characters per token).
        
        Args:
            prompts: Dict with 'system' and 'user' prompts
        
        Returns:
            Estimated token count
        """
        if TIKTOKEN_AVAILABLE:
            try:
                # Use tiktoken for accurate token counting
                encoder = tiktoken.encoding_for_model("gpt-4o")
                system_tokens = len(encoder.encode(prompts["system"]))
                user_tokens = len(encoder.encode(prompts["user"]))
                return system_tokens + user_tokens
            except Exception:
                # Fall back to rough estimate if encoding fails
                pass
        
        # Fallback: rough estimate
        total_chars = len(prompts["system"]) + len(prompts["user"])
        return total_chars // 4
    
    def truncate_pattern_if_needed(
        self, 
        pattern_code: str, 
        max_lines: int = 200
    ) -> str:
        """
        Truncate pattern code if it's too long.
        
        Args:
            pattern_code: Pattern code to potentially truncate
            max_lines: Maximum number of lines to keep
        
        Returns:
            Potentially truncated pattern code
        """
        lines = pattern_code.split('\n')
        if len(lines) <= max_lines:
            return pattern_code
        
        # Keep first portion and add truncation notice
        truncated = '\n'.join(lines[:max_lines])
        truncated += f"\n\n// ... truncated {len(lines) - max_lines} lines ..."
        return truncated
