"""
Tests for TypeScript Type Generator

Tests type generation, interfaces, and strict mode compliance.
"""

import pytest

from src.generation.type_generator import TypeGenerator


class TestTypeGenerator:
    """Test suite for TypeGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Create type generator instance."""
        return TypeGenerator()
    
    @pytest.fixture
    def sample_props(self):
        """Sample prop definitions."""
        return [
            {"name": "variant", "type": "string", "required": False},
            {"name": "size", "type": "string | number", "required": False},
            {"name": "disabled", "type": "boolean", "required": False},
            {"name": "onClick", "type": "function", "required": False},
        ]
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
        assert "Omit" in generator.utility_types
        assert "ReactNode" in generator.react_types
    
    def test_generate_props_interface(self, generator, sample_props):
        """Test generating props interface."""
        interface = generator._generate_props_interface("Button", sample_props)
        
        assert "interface ButtonProps" in interface
        assert "variant?" in interface
        assert "disabled?" in interface
        assert "className?" in interface
        assert "children?" in interface
    
    def test_props_interface_required_props(self, generator):
        """Test that required props don't have optional marker."""
        props = [{"name": "label", "type": "string", "required": True}]
        
        interface = generator._generate_props_interface("Button", props)
        
        assert "label:" in interface  # No ? for required
        assert "label?:" not in interface
    
    def test_props_interface_with_description(self, generator):
        """Test that descriptions are added as JSDoc."""
        props = [{
            "name": "variant",
            "type": "string",
            "required": False,
            "description": "Visual variant of the button"
        }]
        
        interface = generator._generate_props_interface("Button", props)
        
        assert "/** Visual variant of the button */" in interface
    
    def test_to_typescript_type_basic(self, generator):
        """Test converting basic types."""
        assert generator._to_typescript_type("string") == "string"
        assert generator._to_typescript_type("number") == "number"
        assert generator._to_typescript_type("boolean") == "boolean"
    
    def test_to_typescript_type_node(self, generator):
        """Test converting React node types."""
        assert generator._to_typescript_type("node") == "React.ReactNode"
        assert generator._to_typescript_type("element") == "React.ReactElement"
    
    def test_to_typescript_type_function(self, generator):
        """Test converting function types."""
        result = generator._to_typescript_type("function")
        assert "=>" in result
        assert "void" in result
    
    def test_to_typescript_type_union(self, generator):
        """Test that union types are preserved."""
        union_type = "string | number"
        assert generator._to_typescript_type(union_type) == union_type
    
    def test_to_typescript_type_array(self, generator):
        """Test converting array types."""
        result = generator._to_typescript_type("string[]")
        assert result == "string[]"
    
    def test_add_return_types(self, generator):
        """Test adding return type annotations."""
        code = "const Button = ({ variant }) => (<button>{variant}</button>)"
        
        enhanced = generator._add_return_types(code, "Button")
        
        assert "React.ReactElement" in enhanced
    
    def test_add_ref_types_button(self, generator):
        """Test adding ref types for button."""
        code = "React.forwardRef(({ variant }, ref) => <button ref={ref}>{variant}</button>)"
        
        enhanced = generator._add_ref_types(code, "Button")
        
        assert "HTMLButtonElement" in enhanced
        assert "ButtonProps" in enhanced
    
    def test_add_ref_types_input(self, generator):
        """Test adding ref types for input."""
        code = "React.forwardRef((props, ref) => <input ref={ref} />)"
        
        enhanced = generator._add_ref_types(code, "Input")
        
        assert "HTMLInputElement" in enhanced
    
    def test_generate_variant_types(self, generator):
        """Test generating variant union types."""
        variants = ["primary", "secondary", "ghost"]
        
        result = generator.generate_variant_types(variants)
        
        assert '"primary"' in result
        assert '"secondary"' in result
        assert '"ghost"' in result
        assert "|" in result
    
    def test_generate_variant_types_empty(self, generator):
        """Test generating variant types with empty list."""
        result = generator.generate_variant_types([])
        
        assert result == "string"
    
    def test_add_type_imports(self, generator):
        """Test determining needed type imports."""
        code = "const Button = ({ children }: { children: React.ReactNode }) => <button>{children}</button>"
        
        imports = generator.add_type_imports(code)
        
        assert len(imports) > 0
        assert any("ReactNode" in imp for imp in imports)
    
    def test_validate_no_any_types_valid(self, generator):
        """Test validation passes for code without any."""
        code = "const Button = ({ variant }: { variant: string }) => <button>{variant}</button>"
        
        assert generator.validate_no_any_types(code) is True
    
    def test_validate_no_any_types_invalid(self, generator):
        """Test validation fails for code with any."""
        code = "const Button = ({ data }: { data: any }) => <button>{data}</button>"
        
        assert generator.validate_no_any_types(code) is False
    
    def test_validate_no_any_in_generics(self, generator):
        """Test validation catches any in generics."""
        code = "const Button = <T extends any>({ data }: { data: T }) => <button>{data}</button>"
        
        assert generator.validate_no_any_types(code) is False
    
    def test_add_jsdoc_comments(self, generator):
        """Test adding JSDoc comments."""
        code = "const Button = ({ variant }) => <button>{variant}</button>"
        
        enhanced = generator.add_jsdoc_comments(code, "Button", "A reusable button")
        
        assert "/**" in enhanced
        assert "A reusable button" in enhanced
        assert "*/" in enhanced
    
    def test_add_jsdoc_comments_default_description(self, generator):
        """Test JSDoc with default description."""
        code = "const Button = ({ variant }) => <button>{variant}</button>"
        
        enhanced = generator.add_jsdoc_comments(code, "Button")
        
        assert "Button component" in enhanced
    
    def test_generate_types_integration(self, generator, sample_props):
        """Test full type generation flow."""
        code = "const Button = ({ variant }) => <button>{variant}</button>"
        
        enhanced = generator.generate_types(code, "Button", sample_props)
        
        # Should have enhanced code
        assert len(enhanced) >= len(code)
