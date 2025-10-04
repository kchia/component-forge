"""Shadcn/ui default design token fallbacks."""

from typing import Dict, Any

# Default design tokens from shadcn/ui
SHADCN_DEFAULTS: Dict[str, Any] = {
    "colors": {
        "primary": "#3B82F6",
        "background": "#FFFFFF",
        "foreground": "#09090B",
        "secondary": "#F1F5F9",
        "accent": "#F1F5F9",
        "muted": "#F1F5F9",
        "destructive": "#EF4444",
    },
    "typography": {
        "fontFamily": "Inter",
        "fontSize": "16px",
        "fontWeight": 500,
        "lineHeight": "1.5",
    },
    "spacing": {
        "padding": "16px",
        "gap": "8px",
        "margin": "16px",
        "baseUnit": "4px",
    },
    "borderRadius": {
        "default": "8px",
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
    },
}


def get_default_token(category: str, token_name: str) -> Any:
    """Get a default token value by category and name.
    
    Args:
        category: Token category (e.g., 'colors', 'typography')
        token_name: Token name within the category
        
    Returns:
        Default token value or None if not found
    """
    if category in SHADCN_DEFAULTS:
        return SHADCN_DEFAULTS[category].get(token_name)
    return None


def get_defaults_for_category(category: str) -> Dict[str, Any]:
    """Get all default tokens for a category.
    
    Args:
        category: Token category
        
    Returns:
        Dictionary of default tokens for the category
    """
    return SHADCN_DEFAULTS.get(category, {})
