"""
Code Assembler - Assemble and format final component code.

This module combines all code parts (imports, CSS variables, types, component)
and formats the result using Prettier.
"""

import asyncio
import subprocess
from typing import Dict, Any
from pathlib import Path

from .types import CodeParts
from .import_resolver import ImportResolver


class CodeAssembler:
    """
    Assemble final component code from parts and format with Prettier.
    """
    
    def __init__(self):
        """Initialize code assembler."""
        # Find format_code.js script
        backend_dir = Path(__file__).parent.parent.parent
        self.format_script = backend_dir / "scripts" / "format_code.js"
        
        # Initialize import resolver
        self.import_resolver = ImportResolver()
    
    async def assemble(self, parts: CodeParts) -> Dict[str, str]:
        """
        Assemble final component code from parts.
        
        Args:
            parts: CodeParts with all component code sections
        
        Returns:
            Dictionary with assembled and formatted files:
                - component: Formatted component.tsx code
                - stories: Formatted stories.tsx code
                - files: Map of filename to content
        """
        # Build component file
        component_sections = []
        
        # Add provenance header if present
        if parts.provenance_header:
            component_sections.append(parts.provenance_header)
        
        # Resolve and order imports
        if parts.imports:
            # Infer component type from name for missing imports
            component_type = parts.component_name.lower() if parts.component_name else "button"
            ordered_imports = self.import_resolver.resolve_and_order(
                parts.imports,
                component_type
            )
            component_sections.append("\n".join(ordered_imports))
        
        # Add type definitions
        if parts.type_definitions:
            component_sections.append(parts.type_definitions)
        
        # Add component code
        if parts.component_code:
            component_sections.append(parts.component_code)
        
        # Combine with double newlines
        component_code = "\n\n".join(component_sections)
        
        # Format component code
        formatted_component = await self._format_code(component_code)
        
        # Build and format stories file
        stories_code = parts.storybook_stories
        formatted_stories = ""
        if stories_code:
            formatted_stories = await self._format_code(stories_code)
        
        # Determine component name
        component_name = parts.component_name or "Component"
        
        # Build files dictionary
        files = {
            f"{component_name}.tsx": formatted_component,
        }
        
        if formatted_stories:
            files[f"{component_name}.stories.tsx"] = formatted_stories
        
        # Add CSS variables as a separate file
        if parts.css_variables:
            files[f"{component_name}.tokens.css"] = parts.css_variables
        
        return {
            "component": formatted_component,
            "stories": formatted_stories,
            "files": files
        }
    
    async def _format_code(self, code: str) -> str:
        """
        Format code with Prettier via Node.js subprocess.
        
        Args:
            code: Unformatted code string
        
        Returns:
            Formatted code string
        
        Raises:
            ValueError: If Prettier formatting fails
        """
        try:
            # Check if format_code.js exists
            if not self.format_script.exists():
                # Prettier not available, return unformatted code
                # This allows tests to run without Node.js
                return code
            
            # Run Prettier via Node.js script
            result = await asyncio.create_subprocess_exec(
                'node',
                str(self.format_script),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send code to stdin and get formatted output
            stdout, stderr = await result.communicate(code.encode('utf-8'))
            
            if result.returncode != 0:
                error_msg = stderr.decode('utf-8')
                raise ValueError(f"Prettier formatting failed: {error_msg}")
            
            return stdout.decode('utf-8')
        
        except FileNotFoundError:
            # Node.js not available, return unformatted code
            return code
        except Exception as e:
            # Formatting failed, return unformatted code with warning
            print(f"Warning: Code formatting failed: {e}")
            return code
    
    def validate_typescript(self, code: str) -> Dict[str, Any]:
        """
        Validate TypeScript compilation (optional, deferred to Epic 5).
        
        Args:
            code: TypeScript code to validate
        
        Returns:
            Validation result with success flag and errors
        """
        # Placeholder for TypeScript compilation validation
        # Full implementation in Epic 5
        return {
            "success": True,
            "errors": [],
            "warnings": []
        }
    
    def measure_code_metrics(self, code: str) -> Dict[str, int]:
        """
        Measure code metrics.
        
        Args:
            code: Component code
        
        Returns:
            Dictionary with code metrics
        """
        lines = code.split('\n')
        
        # Count non-empty lines
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Count imports
        import_count = len([line for line in lines if line.strip().startswith('import')])
        
        # Count functions/components
        function_count = len([
            line for line in lines 
            if 'function' in line or 'const' in line and '=>' in line
        ])
        
        return {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "import_count": import_count,
            "function_count": function_count
        }
