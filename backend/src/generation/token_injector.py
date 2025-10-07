"""
Token Injector - Inject design tokens into component styles.

This module maps extracted design tokens to component styles and generates
CSS variable definitions.
"""

from typing import Dict, Any, List
from .types import TokenMapping


class TokenInjector:
    """
    Inject design tokens into component styles and generate CSS variables.
    """
    
    def inject(
        self, 
        pattern_code: str,
        tokens: Dict[str, Any],
        component_type: str = "button"
    ) -> TokenMapping:
        """
        Inject design tokens into component and generate CSS variables.
        
        Args:
            pattern_code: Original pattern component code
            tokens: Design tokens from Epic 1 extraction
            component_type: Type of component (button, card, input, etc.)
        
        Returns:
            TokenMapping with CSS variables and token mappings
        """
        # Generate CSS variables from tokens
        css_variables = self._generate_css_variables(tokens)
        
        # Create token mappings for different categories
        color_mapping = self._map_colors(tokens.get("colors", {}), component_type)
        typography_mapping = self._map_typography(tokens.get("typography", {}))
        spacing_mapping = self._map_spacing(tokens.get("spacing", {}), component_type)
        
        return TokenMapping(
            colors=color_mapping,
            typography=typography_mapping,
            spacing=spacing_mapping,
            css_variables=css_variables
        )
    
    def _generate_css_variables(self, tokens: Dict[str, Any]) -> str:
        """
        Generate CSS variable definitions from tokens.
        
        Args:
            tokens: Design tokens dictionary
        
        Returns:
            CSS variable definitions as string
        """
        variables: List[str] = []
        
        # Process colors
        if "colors" in tokens:
            colors = tokens["colors"]
            if isinstance(colors, dict):
                for name, value in colors.items():
                    # Normalize color names (e.g., "Primary" -> "primary")
                    normalized_name = name.lower().replace(" ", "-")
                    variables.append(f"  --color-{normalized_name}: {value};")
        
        # Process typography
        if "typography" in tokens:
            typography = tokens["typography"]
            if isinstance(typography, dict):
                # Font size
                if "fontSize" in typography:
                    variables.append(f"  --font-size-base: {typography['fontSize']};")
                
                # Font family
                if "fontFamily" in typography:
                    variables.append(f"  --font-family: {typography['fontFamily']};")
                
                # Font weight
                if "fontWeight" in typography:
                    variables.append(f"  --font-weight: {typography['fontWeight']};")
                
                # Line height
                if "lineHeight" in typography:
                    variables.append(f"  --line-height: {typography['lineHeight']};")
        
        # Process spacing
        if "spacing" in tokens:
            spacing = tokens["spacing"]
            if isinstance(spacing, dict):
                for name, value in spacing.items():
                    # Normalize spacing names (e.g., "padding" -> "padding")
                    normalized_name = name.lower().replace(" ", "-")
                    variables.append(f"  --spacing-{normalized_name}: {value};")
        
        # Process border radius
        if "borderRadius" in tokens:
            border_radius = tokens["borderRadius"]
            if isinstance(border_radius, dict):
                for name, value in border_radius.items():
                    normalized_name = name.lower().replace(" ", "-")
                    variables.append(f"  --radius-{normalized_name}: {value};")
            else:
                variables.append(f"  --radius-default: {border_radius};")
        
        if not variables:
            return ""
        
        # Build complete CSS variable block
        css = ":root {\n" + "\n".join(variables) + "\n}"
        return css
    
    def _map_colors(
        self, 
        colors: Dict[str, str], 
        component_type: str
    ) -> Dict[str, str]:
        """
        Map color tokens to component-specific color roles.
        
        Args:
            colors: Color tokens dictionary
            component_type: Type of component
        
        Returns:
            Mapping of color roles to CSS variable names
        """
        mapping = {}
        
        # Normalize color keys
        normalized_colors = {
            k.lower().replace(" ", "-"): v 
            for k, v in colors.items()
        }
        
        # Common color mappings for different component types
        if component_type == "button":
            # Map primary color to button background
            if "primary" in normalized_colors:
                mapping["background"] = "var(--color-primary)"
                mapping["text"] = "white"
                mapping["hover-background"] = "var(--color-primary)/90"
            
            # Map secondary color
            if "secondary" in normalized_colors:
                mapping["secondary-background"] = "var(--color-secondary)"
                mapping["secondary-text"] = "var(--color-secondary-foreground)"
        
        elif component_type == "card":
            # Map background and border colors
            if "background" in normalized_colors:
                mapping["background"] = "var(--color-background)"
            if "border" in normalized_colors:
                mapping["border"] = "var(--color-border)"
        
        elif component_type == "input":
            # Map input-specific colors
            if "border" in normalized_colors:
                mapping["border"] = "var(--color-border)"
            if "focus" in normalized_colors:
                mapping["focus-ring"] = "var(--color-focus)"
        
        return mapping
    
    def _map_typography(self, typography: Dict[str, Any]) -> Dict[str, str]:
        """
        Map typography tokens to CSS variable references.
        
        Args:
            typography: Typography tokens dictionary
        
        Returns:
            Mapping of typography properties to CSS variables
        """
        mapping = {}
        
        if "fontSize" in typography:
            mapping["font-size"] = "var(--font-size-base)"
        
        if "fontFamily" in typography:
            mapping["font-family"] = "var(--font-family)"
        
        if "fontWeight" in typography:
            mapping["font-weight"] = "var(--font-weight)"
        
        if "lineHeight" in typography:
            mapping["line-height"] = "var(--line-height)"
        
        return mapping
    
    def _map_spacing(
        self, 
        spacing: Dict[str, str], 
        component_type: str
    ) -> Dict[str, str]:
        """
        Map spacing tokens to component-specific spacing roles.
        
        Args:
            spacing: Spacing tokens dictionary
            component_type: Type of component
        
        Returns:
            Mapping of spacing roles to CSS variable names
        """
        mapping = {}
        
        # Normalize spacing keys
        normalized_spacing = {
            k.lower().replace(" ", "-"): v 
            for k, v in spacing.items()
        }
        
        # Common spacing mappings
        if component_type == "button":
            if "padding" in normalized_spacing:
                mapping["padding"] = "var(--spacing-padding)"
            if "gap" in normalized_spacing:
                mapping["gap"] = "var(--spacing-gap)"
        
        elif component_type == "card":
            if "padding" in normalized_spacing:
                mapping["padding"] = "var(--spacing-padding)"
            if "gap" in normalized_spacing:
                mapping["gap"] = "var(--spacing-gap)"
        
        return mapping
    
    def get_fallback_tokens(self, component_type: str) -> Dict[str, Any]:
        """
        Get fallback tokens for when extraction fails.
        
        Args:
            component_type: Type of component
        
        Returns:
            Default token values
        """
        fallback = {
            "colors": {
                "primary": "#3B82F6",
                "secondary": "#64748B",
                "background": "#FFFFFF",
                "foreground": "#0F172A",
                "border": "#E2E8F0"
            },
            "typography": {
                "fontSize": "14px",
                "fontFamily": "system-ui, sans-serif",
                "fontWeight": "500",
                "lineHeight": "1.5"
            },
            "spacing": {
                "padding": "16px",
                "gap": "8px",
                "margin": "16px"
            },
            "borderRadius": "6px"
        }
        
        return fallback
