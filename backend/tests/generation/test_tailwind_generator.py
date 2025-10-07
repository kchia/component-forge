"""
Tests for Tailwind Generator

Tests Tailwind CSS class generation and variant support.
"""

import pytest

from src.generation.tailwind_generator import TailwindGenerator


class TestTailwindGenerator:
    """Test suite for TailwindGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Create Tailwind generator instance."""
        return TailwindGenerator()
    
    @pytest.fixture
    def sample_tokens(self):
        """Sample design tokens."""
        return {
            "colors": {
                "Primary": "#3B82F6",
                "Secondary": "#64748B"
            },
            "typography": {
                "fontSize": "14px",
                "fontFamily": "Inter, sans-serif"
            },
            "spacing": {
                "padding": "16px",
                "gap": "8px"
            }
        }
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
    
    def test_generate_button_classes(self, generator, sample_tokens):
        """Test generating classes for button component."""
        classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            variant="default",
            size="default"
        )
        
        assert isinstance(classes, str)
        assert len(classes) > 0
        
        # Should contain base button classes
        assert "inline-flex" in classes
        assert "items-center" in classes
        assert "justify-center" in classes
    
    def test_generate_button_primary_variant(self, generator, sample_tokens):
        """Test primary variant classes."""
        classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            variant="primary",
            size="default"
        )
        
        # Should contain primary variant classes
        assert "bg-[var(--color-primary)]" in classes
        assert "text-white" in classes
        assert "hover:bg-[var(--color-primary)]/90" in classes
    
    def test_generate_button_secondary_variant(self, generator, sample_tokens):
        """Test secondary variant classes."""
        classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            variant="secondary",
            size="default"
        )
        
        assert "bg-secondary" in classes
        assert "text-secondary-foreground" in classes
    
    def test_generate_button_ghost_variant(self, generator, sample_tokens):
        """Test ghost variant classes."""
        classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            variant="ghost",
            size="default"
        )
        
        assert "hover:bg-accent" in classes
        assert "hover:text-accent-foreground" in classes
    
    def test_generate_button_outline_variant(self, generator, sample_tokens):
        """Test outline variant classes."""
        classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            variant="outline",
            size="default"
        )
        
        assert "border" in classes
        assert "border-input" in classes
        assert "bg-background" in classes
    
    def test_generate_button_sizes(self, generator, sample_tokens):
        """Test different button sizes."""
        # Small size
        sm_classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            size="sm"
        )
        assert "h-9" in sm_classes
        assert "px-3" in sm_classes
        
        # Large size
        lg_classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            size="lg"
        )
        assert "h-11" in lg_classes
        assert "px-8" in lg_classes
        
        # Icon size
        icon_classes = generator.generate_classes(
            element="button",
            tokens=sample_tokens,
            size="icon"
        )
        assert "h-10" in icon_classes
        assert "w-10" in icon_classes
    
    def test_generate_card_classes(self, generator, sample_tokens):
        """Test generating classes for card component."""
        classes = generator.generate_classes(
            element="card",
            tokens=sample_tokens
        )
        
        assert "rounded-lg" in classes
        assert "border" in classes
        assert "bg-card" in classes
    
    def test_generate_input_classes(self, generator, sample_tokens):
        """Test generating classes for input component."""
        classes = generator.generate_classes(
            element="input",
            tokens=sample_tokens
        )
        
        assert "flex" in classes
        assert "w-full" in classes
        assert "rounded-md" in classes
        assert "border" in classes
        assert "px-3" in classes
        assert "py-2" in classes
    
    def test_generate_badge_classes(self, generator, sample_tokens):
        """Test generating classes for badge component."""
        classes = generator.generate_classes(
            element="badge",
            tokens=sample_tokens,
            variant="default"
        )
        
        assert "inline-flex" in classes
        assert "items-center" in classes
        assert "rounded-full" in classes
        assert "text-xs" in classes
    
    def test_generate_responsive_classes(self, generator):
        """Test generating responsive classes."""
        base_classes = "px-4 py-2"
        breakpoints = {
            "md": "px-6 py-3",
            "lg": "px-8 py-4"
        }
        
        responsive = generator.generate_responsive_classes(base_classes, breakpoints)
        
        assert "px-4 py-2" in responsive
        assert "md:px-6" in responsive
        assert "lg:px-8" in responsive
    
    def test_generate_state_classes(self, generator):
        """Test generating state variant classes."""
        base_classes = "bg-primary"
        states = ["hover", "focus", "disabled"]
        
        state_classes = generator.generate_state_classes(base_classes, states)
        
        assert "bg-primary" in state_classes
        assert "hover:opacity-90" in state_classes
        assert "focus:ring-2" in state_classes
        assert "disabled:opacity-50" in state_classes
