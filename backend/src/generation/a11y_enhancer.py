"""
Accessibility Enhancer - Add ARIA attributes and semantic HTML.

This module enhances generated components with accessibility features including
ARIA attributes, semantic HTML elements, keyboard navigation, and screen reader support.
"""

import re
from typing import Dict, Any, List


class A11yEnhancer:
    """
    Enhance components with accessibility features.
    """
    
    def __init__(self):
        """Initialize accessibility enhancer."""
        # Component-specific ARIA rules
        self.component_rules = {
            "button": self._enhance_button,
            "input": self._enhance_input,
            "card": self._enhance_card,
            "checkbox": self._enhance_checkbox,
            "radio": self._enhance_radio,
            "select": self._enhance_select,
            "switch": self._enhance_switch,
            "tabs": self._enhance_tabs,
            "alert": self._enhance_alert,
            "badge": self._enhance_badge
        }
    
    def enhance(
        self,
        component_code: str,
        component_type: str,
        component_name: str = "Component"
    ) -> str:
        """
        Enhance component with accessibility features.
        
        Args:
            component_code: Original component code
            component_type: Type of component (button, input, etc.)
            component_name: Name of the component
        
        Returns:
            Enhanced component code with a11y features
        """
        # Get component-specific enhancement function
        enhance_func = self.component_rules.get(
            component_type.lower(),
            self._enhance_generic
        )
        
        # Apply enhancements
        enhanced_code = enhance_func(component_code, component_name)
        
        return enhanced_code
    
    def _enhance_button(self, code: str, name: str) -> str:
        """Enhance button with accessibility features."""
        enhanced = code
        
        # Add aria-disabled for disabled state
        if "disabled" in code and "aria-disabled" not in code:
            # Find the button element opening tag
            enhanced = re.sub(
                r'(<button[^>]*)(disabled={disabled})',
                r'\1\2 aria-disabled={disabled}',
                enhanced
            )
        
        # Add aria-busy for loading state
        if "loading" in code.lower() and "aria-busy" not in code:
            enhanced = re.sub(
                r'(<button[^>]*)(disabled={)',
                r'\1aria-busy={loading} \2',
                enhanced
            )
        
        # Ensure button type is specified
        if 'type=' not in enhanced:
            enhanced = re.sub(
                r'<button\s',
                r'<button type="button" ',
                enhanced
            )
        
        return enhanced
    
    def _enhance_input(self, code: str, name: str) -> str:
        """Enhance input with accessibility features."""
        enhanced = code
        
        # Add aria-invalid for validation
        if "error" in code.lower() and "aria-invalid" not in code:
            enhanced = re.sub(
                r'(<input[^>]*)',
                r'\1 aria-invalid={!!error}',
                enhanced
            )
        
        # Add aria-describedby for helper text
        if "helper" in code.lower() or "description" in code.lower():
            if "aria-describedby" not in enhanced:
                enhanced = re.sub(
                    r'(<input[^>]*)',
                    r'\1 aria-describedby={`${id}-description`}',
                    enhanced
                )
        
        # Ensure proper input type
        if 'type=' not in enhanced:
            enhanced = re.sub(
                r'<input\s',
                r'<input type="text" ',
                enhanced
            )
        
        return enhanced
    
    def _enhance_card(self, code: str, name: str) -> str:
        """Enhance card with accessibility features."""
        enhanced = code
        
        # Add role="region" for landmark
        if "role=" not in enhanced:
            enhanced = re.sub(
                r'<div([^>]*className[^>]*Card[^>]*)',
                r'<div\1 role="region"',
                enhanced
            )
        
        # Add aria-labelledby if card has a title
        if "title" in code.lower() and "aria-labelledby" not in code:
            enhanced = re.sub(
                r'(<div[^>]*role="region"[^>]*)',
                r'\1 aria-labelledby={`${id}-title`}',
                enhanced
            )
        
        return enhanced
    
    def _enhance_checkbox(self, code: str, name: str) -> str:
        """Enhance checkbox with accessibility features."""
        enhanced = code
        
        # Add aria-checked for custom checkboxes
        if 'type="checkbox"' in enhanced and "aria-checked" not in enhanced:
            enhanced = re.sub(
                r'(<input[^>]*type="checkbox"[^>]*)',
                r'\1 aria-checked={checked}',
                enhanced
            )
        
        # Ensure proper labeling
        if "<label" not in enhanced:
            # Wrap in label for better a11y
            enhanced = re.sub(
                r'(<input[^>]*type="checkbox"[^>]*>)',
                r'<label>\1</label>',
                enhanced
            )
        
        return enhanced
    
    def _enhance_radio(self, code: str, name: str) -> str:
        """Enhance radio button with accessibility features."""
        enhanced = code
        
        # Add role="radio" for custom radios
        if 'type="radio"' in enhanced and 'role=' not in enhanced:
            enhanced = re.sub(
                r'(<input[^>]*type="radio"[^>]*)',
                r'\1 role="radio" aria-checked={checked}',
                enhanced
            )
        
        # Add role="radiogroup" to container
        if "radiogroup" not in enhanced.lower():
            # This would be added at the container level
            pass
        
        return enhanced
    
    def _enhance_select(self, code: str, name: str) -> str:
        """Enhance select/dropdown with accessibility features."""
        enhanced = code
        
        # Add aria-expanded for custom dropdowns
        if "dropdown" in code.lower() and "aria-expanded" not in code:
            enhanced = re.sub(
                r'(<button[^>]*)',
                r'\1 aria-expanded={open} aria-haspopup="listbox"',
                enhanced
            )
        
        # Add aria-selected for options
        if "option" in code.lower() and "aria-selected" not in code:
            enhanced = re.sub(
                r'(<div[^>]*role="option"[^>]*)',
                r'\1 aria-selected={selected}',
                enhanced
            )
        
        return enhanced
    
    def _enhance_switch(self, code: str, name: str) -> str:
        """Enhance switch with accessibility features."""
        enhanced = code
        
        # Add role="switch" and aria-checked
        if "switch" in code.lower() and 'role="switch"' not in code:
            enhanced = re.sub(
                r'(<button[^>]*)',
                r'\1 role="switch" aria-checked={checked}',
                enhanced
            )
        
        return enhanced
    
    def _enhance_tabs(self, code: str, name: str) -> str:
        """Enhance tabs with accessibility features."""
        enhanced = code
        
        # Add role="tablist", "tab", "tabpanel"
        if "tabs" in code.lower():
            if 'role="tablist"' not in enhanced:
                enhanced = re.sub(
                    r'(<div[^>]*className[^>]*TabsList[^>]*)',
                    r'\1 role="tablist"',
                    enhanced
                )
            
            if 'role="tab"' not in enhanced:
                enhanced = re.sub(
                    r'(<button[^>]*className[^>]*TabsTrigger[^>]*)',
                    r'\1 role="tab" aria-selected={active}',
                    enhanced
                )
            
            if 'role="tabpanel"' not in enhanced:
                enhanced = re.sub(
                    r'(<div[^>]*className[^>]*TabsContent[^>]*)',
                    r'\1 role="tabpanel"',
                    enhanced
                )
        
        return enhanced
    
    def _enhance_alert(self, code: str, name: str) -> str:
        """Enhance alert with accessibility features."""
        enhanced = code
        
        # Add role="alert" for important messages
        if 'role="alert"' not in enhanced:
            enhanced = re.sub(
                r'<div([^>]*className[^>]*Alert[^>]*)',
                r'<div\1 role="alert"',
                enhanced
            )
        
        # Add aria-live for dynamic alerts
        if "aria-live" not in enhanced:
            enhanced = re.sub(
                r'(<div[^>]*role="alert"[^>]*)',
                r'\1 aria-live="polite" aria-atomic="true"',
                enhanced
            )
        
        return enhanced
    
    def _enhance_badge(self, code: str, name: str) -> str:
        """Enhance badge with accessibility features."""
        enhanced = code
        
        # Add role="status" for status badges
        if "status" in code.lower() or "badge" in code.lower():
            if 'role=' not in enhanced:
                enhanced = re.sub(
                    r'<div([^>]*className[^>]*Badge[^>]*)',
                    r'<div\1 role="status"',
                    enhanced
                )
        
        return enhanced
    
    def _enhance_generic(self, code: str, name: str) -> str:
        """Generic accessibility enhancements for any component."""
        enhanced = code
        
        # Add tabIndex for interactive elements without it
        if "onClick" in code or "onKeyDown" in code:
            if "tabIndex" not in enhanced and "<button" not in enhanced:
                enhanced = re.sub(
                    r'<div([^>]*onClick)',
                    r'<div\1 tabIndex={0}',
                    enhanced
                )
        
        return enhanced
    
    def add_keyboard_support(self, code: str) -> str:
        """
        Add keyboard navigation support.
        
        Args:
            code: Component code
        
        Returns:
            Code with keyboard event handlers
        """
        enhanced = code
        
        # Add onKeyDown for clickable divs
        if "onClick" in code and "onKeyDown" not in code and "<div" in code:
            # Add keyboard handler
            enhanced = re.sub(
                r'(onClick={[^}]+})',
                r'\1 onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") onClick(e); }}',
                enhanced
            )
        
        return enhanced
    
    def add_focus_indicators(self, code: str) -> str:
        """
        Ensure focus indicators are present in styles.
        
        Args:
            code: Component code
        
        Returns:
            Code with focus indicator classes
        """
        enhanced = code
        
        # Add focus-visible classes if not present
        if "focus:" in code and "focus-visible:" not in code:
            enhanced = re.sub(
                r'focus:([a-z-]+)',
                r'focus-visible:\1',
                enhanced
            )
        
        return enhanced
