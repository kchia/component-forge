"""
Shared pytest fixtures for backend tests.

Provides common fixtures used across integration and performance test suites.
"""

import pytest
import importlib.util


# Check if backend generation module is available
backend_available = importlib.util.find_spec("src.generation.generator_service") is not None


@pytest.fixture
def sample_tokens():
    """
    Sample design tokens from Epic 1 (token extraction).
    
    Shared across integration and performance test suites.
    """
    return {
        "colors": {
            "Primary": "#3B82F6",
            "Secondary": "#64748B",
            "Success": "#10B981",
            "Error": "#EF4444",
            "Background": "#FFFFFF",
            "Text": "#1F2937"
        },
        "typography": {
            "fontSize": "14px",
            "fontFamily": "Inter, sans-serif",
            "fontWeight": "500",
            "lineHeight": "1.5"
        },
        "spacing": {
            "padding": "16px",
            "gap": "8px",
            "margin": "12px"
        },
        "borders": {
            "radius": "6px",
            "width": "1px"
        }
    }


@pytest.fixture
def button_requirements():
    """
    Button component requirements from Epic 2.
    
    Shared across integration and performance test suites.
    """
    return {
        "props": [
            {"name": "variant", "type": "string", "required": False},
            {"name": "size", "type": "string", "required": False},
            {"name": "disabled", "type": "boolean", "required": False}
        ],
        "events": [
            {"name": "onClick", "type": "MouseEvent", "required": False}
        ],
        "states": [],
        "accessibility": [
            {"name": "aria-label", "required": True}
        ]
    }


@pytest.fixture
def card_requirements():
    """
    Card component requirements from Epic 2.
    
    Shared across integration and performance test suites.
    """
    return {
        "props": [
            {"name": "title", "type": "string", "required": False},
            {"name": "description", "type": "string", "required": False}
        ],
        "events": [],
        "states": [],
        "accessibility": [
            {"name": "role", "value": "article", "required": False}
        ]
    }


@pytest.fixture
def input_requirements():
    """
    Input component requirements from Epic 2.
    
    Shared across integration and performance test suites.
    """
    return {
        "props": [
            {"name": "type", "type": "string", "required": False},
            {"name": "placeholder", "type": "string", "required": False},
            {"name": "disabled", "type": "boolean", "required": False}
        ],
        "events": [
            {"name": "onChange", "type": "ChangeEvent", "required": False}
        ],
        "states": [],
        "accessibility": [
            {"name": "aria-label", "required": True}
        ]
    }
