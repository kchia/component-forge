"""
Tests for Accessibility Enhancer

Tests ARIA attributes, semantic HTML, and keyboard navigation.
"""

import pytest

from src.generation.a11y_enhancer import A11yEnhancer


class TestA11yEnhancer:
    """Test suite for A11yEnhancer."""
    
    @pytest.fixture
    def enhancer(self):
        """Create accessibility enhancer instance."""
        return A11yEnhancer()
    
    def test_enhancer_initialization(self, enhancer):
        """Test that enhancer initializes correctly."""
        assert enhancer is not None
        assert "button" in enhancer.component_rules
        assert "input" in enhancer.component_rules
    
    def test_enhance_button_with_disabled(self, enhancer):
        """Test enhancing button with disabled state."""
        code = '<button disabled={disabled}>Click me</button>'
        
        enhanced = enhancer.enhance(code, "button", "Button")
        
        assert "aria-disabled={disabled}" in enhanced
    
    def test_enhance_button_with_type(self, enhancer):
        """Test that button type is added if missing."""
        code = '<button onClick={handleClick}>Click me</button>'
        
        enhanced = enhancer.enhance(code, "button", "Button")
        
        assert 'type="button"' in enhanced
    
    def test_enhance_input_with_error(self, enhancer):
        """Test enhancing input with error state."""
        code = '<input value={value} error={error} />'
        
        enhanced = enhancer.enhance(code, "input", "Input")
        
        # Should add aria-invalid when error prop is present
        assert "aria-invalid" in enhanced
    
    def test_enhance_input_with_type(self, enhancer):
        """Test that input type is added if missing."""
        code = '<input value={value} />'
        
        enhanced = enhancer.enhance(code, "input", "Input")
        
        assert 'type="text"' in enhanced
    
    def test_enhance_card_with_role(self, enhancer):
        """Test enhancing card with role."""
        code = '<div className="Card">Content</div>'
        
        enhanced = enhancer.enhance(code, "card", "Card")
        
        assert 'role="region"' in enhanced
    
    def test_enhance_checkbox_with_aria(self, enhancer):
        """Test enhancing checkbox with ARIA."""
        code = '<input type="checkbox" />'
        
        enhanced = enhancer.enhance(code, "checkbox", "Checkbox")
        
        assert "aria-checked" in enhanced
    
    def test_enhance_radio_with_role(self, enhancer):
        """Test enhancing radio with role."""
        code = '<input type="radio" />'
        
        enhanced = enhancer.enhance(code, "radio", "Radio")
        
        assert 'role="radio"' in enhanced
        assert "aria-checked" in enhanced
    
    def test_enhance_select_with_expanded(self, enhancer):
        """Test enhancing select with aria-expanded."""
        code = '<button>Select dropdown</button>'
        
        enhanced = enhancer.enhance(code, "select", "Select")
        
        assert "aria-expanded" in enhanced
        assert "aria-haspopup" in enhanced
    
    def test_enhance_switch_with_role(self, enhancer):
        """Test enhancing switch with role."""
        code = '<button>Switch toggle</button>'
        
        enhanced = enhancer.enhance(code, "switch", "Switch")
        
        assert 'role="switch"' in enhanced
        assert "aria-checked" in enhanced
    
    def test_enhance_tabs_with_roles(self, enhancer):
        """Test enhancing tabs with proper roles."""
        code = '''
        <div className="TabsList">
            <button className="TabsTrigger">Tab 1</button>
        </div>
        <div className="TabsContent">Content</div>
        '''
        
        enhanced = enhancer.enhance(code, "tabs", "Tabs")
        
        assert 'role="tablist"' in enhanced
        assert 'role="tab"' in enhanced
        assert 'role="tabpanel"' in enhanced
    
    def test_enhance_alert_with_role(self, enhancer):
        """Test enhancing alert with role."""
        code = '<div className="Alert">Important message</div>'
        
        enhanced = enhancer.enhance(code, "alert", "Alert")
        
        assert 'role="alert"' in enhanced
        assert "aria-live" in enhanced
        assert "aria-atomic" in enhanced
    
    def test_enhance_badge_with_role(self, enhancer):
        """Test enhancing badge with role."""
        code = '<div className="Badge">Status</div>'
        
        enhanced = enhancer.enhance(code, "badge", "Badge")
        
        assert 'role="status"' in enhanced
    
    def test_generic_enhancement_with_onclick(self, enhancer):
        """Test generic enhancement for clickable divs."""
        code = '<div onClick={handleClick}>Clickable</div>'
        
        enhanced = enhancer.enhance(code, "custom", "Custom")
        
        # Should add tabIndex for keyboard accessibility
        assert "tabIndex" in enhanced
    
    def test_add_keyboard_support(self, enhancer):
        """Test adding keyboard event handlers."""
        code = '<div onClick={handleClick}>Clickable</div>'
        
        enhanced = enhancer.add_keyboard_support(code)
        
        assert "onKeyDown" in enhanced
        assert "Enter" in enhanced or "key" in enhanced
    
    def test_add_focus_indicators(self, enhancer):
        """Test adding focus indicators."""
        code = '<button className="focus:ring-2">Click</button>'
        
        enhanced = enhancer.add_focus_indicators(code)
        
        assert "focus-visible:" in enhanced
    
    def test_button_already_has_aria(self, enhancer):
        """Test that existing ARIA attributes are not duplicated."""
        code = '<button aria-disabled={disabled} disabled={disabled}>Click</button>'
        
        enhanced = enhancer.enhance(code, "button", "Button")
        
        # Should not add duplicate aria-disabled
        assert enhanced.count("aria-disabled") == 1
    
    def test_input_already_has_aria(self, enhancer):
        """Test that existing ARIA attributes are not duplicated."""
        code = '<input aria-invalid={!!error} />'
        
        enhanced = enhancer.enhance(code, "input", "Input")
        
        # Should not add duplicate aria-invalid
        assert enhanced.count("aria-invalid") == 1
    
    def test_multiple_components(self, enhancer):
        """Test enhancing different component types."""
        components = [
            ('<button disabled={disabled}>Click</button>', "button"),
            ('<input error={error} />', "input"),
            ('<div className="Card">Card</div>', "card"),
        ]
        
        for code, comp_type in components:
            enhanced = enhancer.enhance(code, comp_type, comp_type.title())
            
            # Should be enhanced (will have different content)
            assert len(enhanced) >= len(code)
    
    def test_preserve_existing_code(self, enhancer):
        """Test that existing code structure is preserved."""
        code = '''
        <button type="submit" className="btn-primary" onClick={handleClick}>
            <span>Submit</span>
        </button>
        '''
        
        enhanced = enhancer.enhance(code, "button", "Button")
        
        # Should preserve className, onClick, span
        assert "className" in enhanced
        assert "onClick" in enhanced
        assert "<span>" in enhanced
        assert "</span>" in enhanced
