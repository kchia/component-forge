"""
Tests for Storybook Story Generator

Tests Storybook CSF 3.0 story generation with variants and controls.
"""

import pytest

from src.generation.storybook_generator import StorybookGenerator


class TestStorybookGenerator:
    """Test suite for StorybookGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Create Storybook generator instance."""
        return StorybookGenerator()
    
    @pytest.fixture
    def sample_props(self):
        """Sample prop definitions."""
        return [
            {"name": "variant", "type": "string", "description": "Visual variant"},
            {"name": "size", "type": "string | number", "description": "Size"},
            {"name": "disabled", "type": "boolean", "description": "Disabled state"},
        ]
    
    @pytest.fixture
    def sample_variants(self):
        """Sample variant names."""
        return ["default", "primary", "secondary", "ghost"]
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
        assert generator.storybook_version == "8.0"
        assert generator.csf_version == "3.0"
    
    def test_generate_imports(self, generator):
        """Test generating import statements."""
        imports = generator._generate_imports("Button")
        
        assert "import type" in imports
        assert "Meta" in imports
        assert "StoryObj" in imports
        assert "from './Button'" in imports
    
    def test_generate_meta(self, generator, sample_props):
        """Test generating meta object."""
        meta = generator._generate_meta("Button", sample_props)
        
        assert "const meta: Meta<typeof Button>" in meta
        assert "title: 'Components/Button'" in meta
        assert "tags: ['autodocs']" in meta
        assert "argTypes:" in meta
    
    def test_generate_arg_types(self, generator, sample_props):
        """Test generating argTypes for controls."""
        arg_types = generator._generate_arg_types(sample_props)
        
        assert "variant:" in arg_types
        assert "size:" in arg_types
        assert "disabled:" in arg_types
        assert "className:" in arg_types
        assert "Visual variant" in arg_types
    
    def test_get_control_type_text(self, generator):
        """Test getting control type for string."""
        assert generator._get_control_type("string") == "text"
    
    def test_get_control_type_number(self, generator):
        """Test getting control type for number."""
        assert generator._get_control_type("number") == "number"
    
    def test_get_control_type_boolean(self, generator):
        """Test getting control type for boolean."""
        assert generator._get_control_type("boolean") == "boolean"
    
    def test_get_control_type_select(self, generator):
        """Test getting control type for enum/variant."""
        assert generator._get_control_type("string | number") == "select"
    
    def test_generate_variant_stories(self, generator, sample_variants, sample_props):
        """Test generating variant stories."""
        stories = generator._generate_variant_stories(
            "Button",
            sample_variants,
            sample_props,
            "button"
        )
        
        assert "export const Default: Story" in stories
        assert "export const Primary: Story" in stories
        assert "export const Secondary: Story" in stories
        assert "export const Ghost: Story" in stories
    
    def test_variant_stories_have_args(self, generator, sample_variants, sample_props):
        """Test that variant stories have proper args."""
        stories = generator._generate_variant_stories(
            "Button",
            sample_variants,
            sample_props,
            "button"
        )
        
        assert "args:" in stories
        assert "children:" in stories
    
    def test_generate_state_stories_button(self, generator):
        """Test generating state stories for button."""
        stories = generator._generate_state_stories("Button", "button")
        
        assert "export const Disabled: Story" in stories
        assert "disabled: true" in stories
        assert "export const Loading: Story" in stories
        assert "loading: true" in stories
    
    def test_generate_state_stories_input(self, generator):
        """Test generating state stories for input."""
        stories = generator._generate_state_stories("Input", "input")
        
        assert "export const Disabled: Story" in stories
        assert "export const WithError: Story" in stories
        assert "error:" in stories
    
    def test_generate_state_stories_card(self, generator):
        """Test that non-interactive components have no state stories."""
        stories = generator._generate_state_stories("Card", "card")
        
        # Card doesn't have disabled/loading states
        assert stories == ""
    
    def test_get_default_args_button(self, generator):
        """Test getting default args for button."""
        args = generator._get_default_args("button")
        
        assert "children:" in args
        assert "Button" in args
    
    def test_get_default_args_input(self, generator):
        """Test getting default args for input."""
        args = generator._get_default_args("input")
        
        assert "placeholder:" in args
    
    def test_get_default_args_various_types(self, generator):
        """Test default args for various component types."""
        types = ["button", "input", "card", "badge", "alert"]
        
        for comp_type in types:
            args = generator._get_default_args(comp_type)
            assert len(args) > 0
    
    def test_generate_stories_full(self, generator, sample_variants, sample_props):
        """Test full story generation."""
        stories = generator.generate_stories(
            "Button",
            sample_variants,
            sample_props,
            "button"
        )
        
        # Should have all sections
        assert "import type" in stories
        assert "const meta: Meta" in stories
        assert "export default meta" in stories
        assert "export const Default: Story" in stories
        assert "export const Primary: Story" in stories
        assert "export const Disabled: Story" in stories
    
    def test_stories_csf_3_format(self, generator, sample_variants, sample_props):
        """Test that stories follow CSF 3.0 format."""
        stories = generator.generate_stories(
            "Button",
            sample_variants,
            sample_props,
            "button"
        )
        
        # CSF 3.0 uses StoryObj type
        assert "StoryObj" in stories
        assert "type Story = StoryObj" in stories
        
        # CSF 3.0 uses args instead of render
        assert "args:" in stories
    
    def test_generate_play_function_button(self, generator):
        """Test generating play function for button."""
        play = generator.generate_play_function("button")
        
        assert "play:" in play
        assert "canvasElement" in play
        assert "userEvent.click" in play
    
    def test_generate_play_function_other(self, generator):
        """Test that other components return empty play function."""
        play = generator.generate_play_function("card")
        
        assert play == ""
    
    def test_add_parameters(self, generator):
        """Test adding Storybook parameters."""
        params = generator.add_parameters("button")
        
        assert "parameters:" in params
        assert "docs:" in params
        assert "description:" in params
    
    def test_stories_have_proper_structure(self, generator, sample_variants, sample_props):
        """Test that generated stories have proper structure."""
        stories = generator.generate_stories(
            "Button",
            sample_variants,
            sample_props,
            "button"
        )
        
        # Count stories
        story_count = stories.count("export const")
        
        # Should have: Default + variants (3: Primary, Secondary, Ghost) + states (2: Disabled, Loading)
        assert story_count >= 5
    
    def test_multiple_components(self, generator, sample_props):
        """Test generating stories for different components."""
        components = [
            ("Button", ["primary", "secondary"], "button"),
            ("Input", ["default"], "input"),
            ("Card", ["default"], "card"),
        ]
        
        for name, variants, comp_type in components:
            stories = generator.generate_stories(name, variants, sample_props, comp_type)
            
            assert f"title: 'Components/{name}'" in stories
            assert "export const Default: Story" in stories
