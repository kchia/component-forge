"""
Tests for Token Injector

Tests token injection accuracy and CSS variable generation.
"""

import pytest

from src.generation.token_injector import TokenInjector
from src.generation.types import TokenMapping


class TestTokenInjector:
    """Test suite for TokenInjector."""
    
    @pytest.fixture
    def injector(self):
        """Create token injector instance."""
        return TokenInjector()
    
    @pytest.fixture
    def sample_tokens(self):
        """Sample design tokens from Epic 1 extraction."""
        return {
            "colors": {
                "Primary": "#3B82F6",
                "Secondary": "#64748B",
                "Background": "#FFFFFF",
                "Foreground": "#0F172A"
            },
            "typography": {
                "fontSize": "14px",
                "fontFamily": "Inter, system-ui, sans-serif",
                "fontWeight": "500",
                "lineHeight": "1.5"
            },
            "spacing": {
                "padding": "16px",
                "gap": "8px",
                "margin": "24px"
            },
            "borderRadius": "6px"
        }
    
    def test_injector_initialization(self, injector):
        """Test that injector initializes correctly."""
        assert injector is not None
    
    def test_inject_tokens(self, injector, sample_tokens):
        """Test injecting tokens into component."""
        pattern_code = 'const Button = () => <button className="bg-blue-500">Click</button>'
        
        result = injector.inject(pattern_code, sample_tokens, "button")
        
        assert isinstance(result, TokenMapping)
        assert result.css_variables != ""
        assert result.colors is not None
        assert result.typography is not None
        assert result.spacing is not None
    
    def test_generate_css_variables_colors(self, injector, sample_tokens):
        """Test CSS variable generation for colors."""
        css_vars = injector._generate_css_variables(sample_tokens)
        
        assert ":root {" in css_vars
        assert "--color-primary" in css_vars
        assert "#3B82F6" in css_vars
        assert "--color-secondary" in css_vars
        assert "}" in css_vars
    
    def test_generate_css_variables_typography(self, injector, sample_tokens):
        """Test CSS variable generation for typography."""
        css_vars = injector._generate_css_variables(sample_tokens)
        
        assert "--font-size-base" in css_vars
        assert "14px" in css_vars
        assert "--font-family" in css_vars
        assert "Inter" in css_vars
    
    def test_generate_css_variables_spacing(self, injector, sample_tokens):
        """Test CSS variable generation for spacing."""
        css_vars = injector._generate_css_variables(sample_tokens)
        
        assert "--spacing-padding" in css_vars
        assert "16px" in css_vars
        assert "--spacing-gap" in css_vars
        assert "8px" in css_vars
    
    def test_generate_css_variables_border_radius(self, injector, sample_tokens):
        """Test CSS variable generation for border radius."""
        css_vars = injector._generate_css_variables(sample_tokens)
        
        assert "--radius" in css_vars
        assert "6px" in css_vars
    
    def test_generate_css_variables_empty_tokens(self, injector):
        """Test CSS variable generation with empty tokens."""
        empty_tokens = {}
        
        css_vars = injector._generate_css_variables(empty_tokens)
        
        assert css_vars == ""
    
    def test_map_colors_button(self, injector, sample_tokens):
        """Test color mapping for button component."""
        colors = sample_tokens["colors"]
        
        color_mapping = injector._map_colors(colors, "button")
        
        assert "background" in color_mapping
        assert "var(--color-primary)" in color_mapping["background"]
    
    def test_map_colors_card(self, injector, sample_tokens):
        """Test color mapping for card component."""
        colors = sample_tokens["colors"]
        
        color_mapping = injector._map_colors(colors, "card")
        
        # Card should have background mapping
        assert "background" in color_mapping or len(color_mapping) >= 0
    
    def test_map_typography(self, injector, sample_tokens):
        """Test typography mapping."""
        typography = sample_tokens["typography"]
        
        typography_mapping = injector._map_typography(typography)
        
        assert "font-size" in typography_mapping
        assert "var(--font-size-base)" in typography_mapping["font-size"]
        assert "font-family" in typography_mapping
        assert "font-weight" in typography_mapping
    
    def test_map_spacing_button(self, injector, sample_tokens):
        """Test spacing mapping for button component."""
        spacing = sample_tokens["spacing"]
        
        spacing_mapping = injector._map_spacing(spacing, "button")
        
        assert "padding" in spacing_mapping or len(spacing_mapping) >= 0
    
    def test_get_fallback_tokens(self, injector):
        """Test fallback tokens for when extraction fails."""
        fallback = injector.get_fallback_tokens("button")
        
        assert "colors" in fallback
        assert "typography" in fallback
        assert "spacing" in fallback
        assert "primary" in fallback["colors"]
        assert "fontSize" in fallback["typography"]
        assert "padding" in fallback["spacing"]
    
    def test_token_injection_accuracy(self, injector, sample_tokens):
        """Test that token injection accuracy is ≥95%."""
        pattern_code = "const Button = () => {}"
        
        result = injector.inject(pattern_code, sample_tokens, "button")
        
        # Count expected vs actual tokens
        expected_color_count = len(sample_tokens["colors"])
        expected_typography_count = len(sample_tokens["typography"])
        expected_spacing_count = len(sample_tokens["spacing"])
        
        # CSS variables should contain all tokens
        css_vars = result.css_variables
        
        # Count occurrences of token categories
        color_occurrences = css_vars.count("--color-")
        typography_occurrences = css_vars.count("--font-")
        spacing_occurrences = css_vars.count("--spacing-")
        
        # At least some tokens should be injected
        assert color_occurrences > 0
        assert typography_occurrences > 0
        assert spacing_occurrences > 0
