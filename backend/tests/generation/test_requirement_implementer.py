"""
Tests for Requirements Implementer

Tests implementation of props, events, and states from requirements.
"""

import pytest

from src.generation.requirement_implementer import RequirementImplementer


class TestRequirementImplementer:
    """Test suite for RequirementImplementer."""
    
    @pytest.fixture
    def implementer(self):
        """Create requirement implementer instance."""
        return RequirementImplementer()
    
    @pytest.fixture
    def sample_requirements(self):
        """Sample requirements for testing."""
        return {
            "props": [
                {
                    "name": "variant",
                    "type": "string",
                    "values": ["default", "secondary", "ghost"],
                    "required": False,
                    "description": "Visual style variant"
                },
                {
                    "name": "size",
                    "type": "string",
                    "values": ["sm", "default", "lg"],
                    "required": False,
                    "description": "Size of the component"
                },
                {
                    "name": "disabled",
                    "type": "boolean",
                    "required": False,
                    "description": "Disable the component"
                }
            ],
            "events": [
                {"name": "onClick", "type": "MouseEvent"},
                {"name": "onFocus", "type": "FocusEvent"}
            ],
            "states": [
                {"name": "isLoading", "type": "boolean", "default": "false"},
                {"name": "isHovered", "type": "boolean", "default": "false"}
            ]
        }
    
    def test_implementer_initialization(self, implementer):
        """Test that implementer initializes correctly."""
        assert implementer is not None
    
    def test_implement_requirements(self, implementer, sample_requirements):
        """Test implementing requirements in component."""
        component_code = "const Button = () => {}"
        
        result = implementer.implement(
            component_code,
            sample_requirements,
            "Button"
        )
        
        assert result is not None
        assert "props_interface" in result
        assert "event_handlers" in result
        assert "state_code" in result
    
    def test_generate_props_interface(self, implementer, sample_requirements):
        """Test generating TypeScript props interface."""
        props_interface = implementer._generate_props_interface(
            sample_requirements["props"],
            "Button"
        )
        
        assert "interface ButtonProps" in props_interface
        assert "variant?" in props_interface
        assert "size?" in props_interface
        assert "disabled?" in props_interface
        
        # Should contain type definitions
        assert '"default" | "secondary" | "ghost"' in props_interface
        assert "boolean" in props_interface
    
    def test_infer_prop_type_enum(self, implementer):
        """Test inferring enum type from values."""
        prop = {
            "name": "variant",
            "values": ["primary", "secondary", "ghost"]
        }
        
        prop_type = implementer._infer_prop_type(prop)
        
        assert '"primary"' in prop_type
        assert '"secondary"' in prop_type
        assert '"ghost"' in prop_type
        assert "|" in prop_type
    
    def test_infer_prop_type_boolean(self, implementer):
        """Test inferring boolean type."""
        prop = {"name": "disabled", "type": "boolean"}
        
        prop_type = implementer._infer_prop_type(prop)
        
        assert prop_type == "boolean"
    
    def test_infer_prop_type_function(self, implementer):
        """Test inferring function type."""
        prop = {"name": "onClick", "type": "function"}
        
        prop_type = implementer._infer_prop_type(prop)
        
        assert "=>" in prop_type or "void" in prop_type
    
    def test_generate_event_handlers(self, implementer, sample_requirements):
        """Test generating event handler types."""
        handlers = implementer._generate_event_handlers(
            sample_requirements["events"]
        )
        
        assert len(handlers) == 2
        
        # Should contain onClick and onFocus handlers
        handlers_str = " ".join(handlers)
        assert "onClick" in handlers_str
        assert "onFocus" in handlers_str
        assert "MouseEvent" in handlers_str
        assert "FocusEvent" in handlers_str
    
    def test_generate_state_management(self, implementer, sample_requirements):
        """Test generating state management code."""
        state_code = implementer._generate_state_management(
            sample_requirements["states"]
        )
        
        assert "useState" in state_code
        assert "isLoading" in state_code
        assert "setIsLoading" in state_code
        assert "isHovered" in state_code
        assert "setIsHovered" in state_code
        assert "false" in state_code
    
    def test_get_default_value(self, implementer):
        """Test getting default values for types."""
        assert implementer._get_default_value("boolean") == "false"
        assert implementer._get_default_value("string") == '""'
        assert implementer._get_default_value("number") == "0"
        assert implementer._get_default_value("object") == "{}"
        assert implementer._get_default_value("array") == "[]"
    
    def test_generate_accessibility_props_button(self, implementer):
        """Test generating accessibility props for button."""
        requirements = {"variants": [{"name": "icon"}]}
        
        aria_props = implementer.generate_accessibility_props("button", requirements)
        
        assert len(aria_props) > 0
        aria_str = " ".join(aria_props)
        assert "aria-label" in aria_str
        assert "aria-disabled" in aria_str
        assert "aria-busy" in aria_str
    
    def test_generate_accessibility_props_input(self, implementer):
        """Test generating accessibility props for input."""
        aria_props = implementer.generate_accessibility_props("input", {})
        
        assert len(aria_props) > 0
        aria_str = " ".join(aria_props)
        assert "aria-label" in aria_str
        assert "aria-required" in aria_str
        assert "aria-invalid" in aria_str
    
    def test_add_validation_logic(self, implementer):
        """Test generating validation logic."""
        requirements = {
            "validation": [
                {"type": "required", "field": "email"},
                {"type": "minLength", "field": "password", "value": 8}
            ]
        }
        
        validation = implementer.add_validation_logic(requirements)
        
        assert "email" in validation
        assert "password" in validation
        assert "8" in validation
