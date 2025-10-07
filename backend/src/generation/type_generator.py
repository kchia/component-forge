"""
TypeScript Type Generator - Generate strict TypeScript types.

This module generates TypeScript interfaces, type annotations, and utility types
for components, ensuring zero `any` types and strict mode compliance.
"""

import re
from typing import List, Dict, Any, Optional


class TypeGenerator:
    """
    Generate strict TypeScript types for components.
    """
    
    def __init__(self):
        """Initialize type generator."""
        # Common TypeScript utility types
        self.utility_types = {
            "Omit", "Pick", "Partial", "Required",
            "Record", "Exclude", "Extract", "NonNullable"
        }
        
        # Standard React types
        self.react_types = {
            "ReactNode", "ReactElement", "ComponentProps",
            "HTMLAttributes", "ButtonHTMLAttributes", "InputHTMLAttributes"
        }
    
    def generate_types(
        self,
        component_code: str,
        component_name: str,
        props: List[Dict[str, Any]]
    ) -> str:
        """
        Generate TypeScript types for component.
        
        Args:
            component_code: Original component code
            component_name: Name of the component
            props: List of prop definitions
        
        Returns:
            Component code with enhanced type definitions
        """
        # Generate props interface
        props_interface = self._generate_props_interface(
            component_name,
            props
        )
        
        # Add return type annotations
        enhanced_code = self._add_return_types(component_code, component_name)
        
        # Add ref forwarding types if needed
        if "forwardRef" in enhanced_code or "ref" in str(props).lower():
            enhanced_code = self._add_ref_types(enhanced_code, component_name)
        
        return enhanced_code
    
    def _generate_props_interface(
        self,
        component_name: str,
        props: List[Dict[str, Any]]
    ) -> str:
        """
        Generate props interface with proper types.
        
        Args:
            component_name: Name of the component
            props: List of prop definitions
        
        Returns:
            TypeScript interface definition
        """
        interface_name = f"{component_name}Props"
        
        # Build interface properties
        properties = []
        
        for prop in props:
            prop_name = prop.get("name", "")
            prop_type = prop.get("type", "string")
            required = prop.get("required", False)
            description = prop.get("description", "")
            
            # Convert to TypeScript type
            ts_type = self._to_typescript_type(prop_type)
            
            # Optional property marker
            optional_marker = "" if required else "?"
            
            # Build property line with JSDoc if description exists
            prop_line = ""
            if description:
                prop_line += f"  /** {description} */\n"
            
            prop_line += f"  {prop_name}{optional_marker}: {ts_type};"
            properties.append(prop_line)
        
        # Add standard React props
        properties.append("  className?: string;")
        properties.append("  children?: React.ReactNode;")
        
        # Build interface
        interface = f"interface {interface_name} {{\n"
        interface += "\n".join(properties)
        interface += "\n}"
        
        return interface
    
    def _to_typescript_type(self, prop_type: str) -> str:
        """
        Convert prop type to TypeScript type.
        
        Args:
            prop_type: Property type (string, number, boolean, etc.)
        
        Returns:
            TypeScript type string
        """
        # Handle basic types
        type_mapping = {
            "string": "string",
            "number": "number",
            "boolean": "boolean",
            "function": "() => void",
            "array": "unknown[]",
            "object": "Record<string, unknown>",
            "node": "React.ReactNode",
            "element": "React.ReactElement",
        }
        
        # Check if it's a variant type (union of strings)
        if "|" in prop_type:
            return prop_type  # Already a union type
        
        # Check for array syntax
        if prop_type.endswith("[]"):
            base_type = prop_type[:-2]
            return f"{self._to_typescript_type(base_type)}[]"
        
        return type_mapping.get(prop_type.lower(), prop_type)
    
    def _add_return_types(self, code: str, component_name: str) -> str:
        """
        Add return type annotations to functions.
        
        Args:
            code: Component code
            component_name: Name of component
        
        Returns:
            Code with return type annotations
        """
        enhanced = code
        
        # Add return type to main component function
        # Pattern: const ComponentName = ({ ... }) => (
        component_pattern = rf'(const\s+{component_name}\s*=\s*\([^)]*\))\s*=>'
        
        if re.search(component_pattern, enhanced):
            enhanced = re.sub(
                component_pattern,
                rf'\1: React.ReactElement =>',
                enhanced
            )
        
        # Add return type to forwardRef
        forwardref_pattern = r'(React\.forwardRef\s*<[^>]*>\s*\([^)]*\))\s*=>'
        
        if re.search(forwardref_pattern, enhanced):
            enhanced = re.sub(
                forwardref_pattern,
                r'\1: React.ReactElement =>',
                enhanced
            )
        
        return enhanced
    
    def _add_ref_types(self, code: str, component_name: str) -> str:
        """
        Add proper types for ref forwarding.
        
        Args:
            code: Component code
            component_name: Name of component
        
        Returns:
            Code with ref forwarding types
        """
        enhanced = code
        
        # Add HTMLElement ref type for buttons
        if "button" in component_name.lower():
            ref_type = "HTMLButtonElement"
        elif "input" in component_name.lower():
            ref_type = "HTMLInputElement"
        elif "div" in code.lower():
            ref_type = "HTMLDivElement"
        else:
            ref_type = "HTMLElement"
        
        # Update forwardRef generic type
        enhanced = re.sub(
            r'React\.forwardRef\s*(?:<[^>]*>)?',
            f'React.forwardRef<{ref_type}, {component_name}Props>',
            enhanced
        )
        
        return enhanced
    
    def generate_variant_types(self, variants: List[str]) -> str:
        """
        Generate union type for variants.
        
        Args:
            variants: List of variant names
        
        Returns:
            TypeScript union type
        """
        if not variants:
            return "string"
        
        # Create union of string literals
        variant_literals = [f'"{v}"' for v in variants]
        return " | ".join(variant_literals)
    
    def add_type_imports(self, code: str) -> List[str]:
        """
        Determine which type imports are needed.
        
        Args:
            code: Component code
        
        Returns:
            List of import statements for types
        """
        imports = []
        
        # Check if React types are needed
        if "React.ReactNode" in code or "ReactNode" in code:
            if "import type" not in code:
                imports.append('import type { ReactNode, ReactElement } from "react"')
        
        # Check if ComponentProps is needed
        if "ComponentProps" in code:
            imports.append('import type { ComponentProps } from "react"')
        
        # Check if HTMLAttributes is needed
        if "HTMLAttributes" in code or "ButtonHTMLAttributes" in code:
            imports.append('import type { HTMLAttributes } from "react"')
        
        return imports
    
    def validate_no_any_types(self, code: str) -> bool:
        """
        Validate that code has no `any` types.
        
        Args:
            code: TypeScript code
        
        Returns:
            True if no `any` types found, False otherwise
        """
        # Check for explicit any types
        any_pattern = r':\s*any\b'
        
        if re.search(any_pattern, code):
            return False
        
        # Check for any in generic parameters
        generic_any_pattern = r'<[^>]*\bany\b[^>]*>'
        
        if re.search(generic_any_pattern, code):
            return False
        
        return True
    
    def add_jsdoc_comments(
        self,
        code: str,
        component_name: str,
        description: str = ""
    ) -> str:
        """
        Add JSDoc comments for complex types.
        
        Args:
            code: Component code
            component_name: Name of component
            description: Component description
        
        Returns:
            Code with JSDoc comments
        """
        if not description:
            description = f"{component_name} component"
        
        jsdoc = f"""/**
 * {description}
 */"""
        
        # Add before component definition
        enhanced = re.sub(
            rf'((?:export\s+)?(?:const|function)\s+{component_name})',
            f'{jsdoc}\n\\1',
            code
        )
        
        return enhanced
