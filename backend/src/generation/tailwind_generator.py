"""
Tailwind CSS Generator - Generate Tailwind classes using design tokens.

This module generates Tailwind CSS classes with CSS variable references
for dynamic styling based on injected design tokens.
"""

from typing import List, Dict, Any, Optional


class TailwindGenerator:
    """
    Generate Tailwind CSS classes using design tokens via CSS variables.
    """
    
    def generate_classes(
        self,
        element: str,
        tokens: Dict[str, Any],
        variant: Optional[str] = None,
        size: Optional[str] = None
    ) -> str:
        """
        Generate Tailwind CSS classes for a component element.
        
        Args:
            element: Element type (button, card, input, etc.)
            tokens: Design tokens with color, typography, spacing
            variant: Optional variant name (primary, secondary, ghost, etc.)
            size: Optional size name (sm, default, lg, etc.)
        
        Returns:
            Space-separated Tailwind class string
        """
        classes: List[str] = []
        
        # Generate base classes based on element type
        if element == "button":
            classes.extend(self._generate_button_classes(tokens, variant, size))
        elif element == "card":
            classes.extend(self._generate_card_classes(tokens))
        elif element == "input":
            classes.extend(self._generate_input_classes(tokens))
        elif element == "badge":
            classes.extend(self._generate_badge_classes(tokens, variant))
        else:
            # Default generic classes
            classes.extend(self._generate_generic_classes(tokens))
        
        return " ".join(classes)
    
    def _generate_button_classes(
        self,
        tokens: Dict[str, Any],
        variant: Optional[str],
        size: Optional[str]
    ) -> List[str]:
        """Generate Tailwind classes for button component."""
        classes = [
            # Layout
            "inline-flex",
            "items-center",
            "justify-center",
            "gap-2",
            "whitespace-nowrap",
            
            # Border
            "rounded-md",
            
            # Typography
            "text-sm",
            "font-medium",
            
            # Transitions
            "transition-colors",
            
            # Focus states
            "focus-visible:outline-none",
            "focus-visible:ring-2",
            "focus-visible:ring-ring",
            "focus-visible:ring-offset-2",
            
            # Disabled state
            "disabled:pointer-events-none",
            "disabled:opacity-50"
        ]
        
        # Add variant-specific classes
        if variant == "default" or variant == "primary":
            classes.extend([
                "bg-[var(--color-primary)]",
                "text-white",
                "hover:bg-[var(--color-primary)]/90"
            ])
        elif variant == "destructive":
            classes.extend([
                "bg-destructive",
                "text-destructive-foreground",
                "hover:bg-destructive/90"
            ])
        elif variant == "outline":
            classes.extend([
                "border",
                "border-input",
                "bg-background",
                "hover:bg-accent",
                "hover:text-accent-foreground"
            ])
        elif variant == "secondary":
            classes.extend([
                "bg-secondary",
                "text-secondary-foreground",
                "hover:bg-secondary/80"
            ])
        elif variant == "ghost":
            classes.extend([
                "hover:bg-accent",
                "hover:text-accent-foreground"
            ])
        elif variant == "link":
            classes.extend([
                "text-primary",
                "underline-offset-4",
                "hover:underline"
            ])
        
        # Add size-specific classes
        if size == "sm":
            classes.extend(["h-9", "rounded-md", "px-3"])
        elif size == "lg":
            classes.extend(["h-11", "rounded-md", "px-8"])
        elif size == "icon":
            classes.extend(["h-10", "w-10"])
        else:  # default
            classes.extend(["h-10", "px-4", "py-2"])
        
        # Inject spacing from tokens if available
        if "spacing" in tokens and "padding" in tokens["spacing"]:
            # Replace px-4 with custom padding if needed
            # For now, keep standard Tailwind classes
            pass
        
        return classes
    
    def _generate_card_classes(
        self,
        tokens: Dict[str, Any]
    ) -> List[str]:
        """Generate Tailwind classes for card component."""
        classes = [
            # Layout
            "rounded-lg",
            "border",
            
            # Colors
            "bg-card",
            "text-card-foreground",
            
            # Shadows
            "shadow-sm"
        ]
        
        # Add spacing from tokens
        if "spacing" in tokens and "padding" in tokens["spacing"]:
            classes.append("p-6")  # Default padding
        
        return classes
    
    def _generate_input_classes(
        self,
        tokens: Dict[str, Any]
    ) -> List[str]:
        """Generate Tailwind classes for input component."""
        classes = [
            # Layout
            "flex",
            "w-full",
            
            # Border
            "rounded-md",
            "border",
            "border-input",
            
            # Colors
            "bg-background",
            
            # Typography
            "text-sm",
            
            # Spacing
            "px-3",
            "py-2",
            
            # Focus
            "ring-offset-background",
            "focus-visible:outline-none",
            "focus-visible:ring-2",
            "focus-visible:ring-ring",
            "focus-visible:ring-offset-2",
            
            # Disabled
            "disabled:cursor-not-allowed",
            "disabled:opacity-50"
        ]
        
        return classes
    
    def _generate_badge_classes(
        self,
        tokens: Dict[str, Any],
        variant: Optional[str]
    ) -> List[str]:
        """Generate Tailwind classes for badge component."""
        classes = [
            # Layout
            "inline-flex",
            "items-center",
            "rounded-full",
            
            # Border
            "border",
            
            # Typography
            "text-xs",
            "font-semibold",
            
            # Spacing
            "px-2.5",
            "py-0.5",
            
            # Transition
            "transition-colors"
        ]
        
        # Variant-specific colors
        if variant == "default":
            classes.extend([
                "border-transparent",
                "bg-primary",
                "text-primary-foreground",
                "hover:bg-primary/80"
            ])
        elif variant == "secondary":
            classes.extend([
                "border-transparent",
                "bg-secondary",
                "text-secondary-foreground",
                "hover:bg-secondary/80"
            ])
        elif variant == "outline":
            classes.extend([
                "text-foreground"
            ])
        elif variant == "destructive":
            classes.extend([
                "border-transparent",
                "bg-destructive",
                "text-destructive-foreground",
                "hover:bg-destructive/80"
            ])
        
        return classes
    
    def _generate_generic_classes(
        self,
        tokens: Dict[str, Any]
    ) -> List[str]:
        """Generate generic Tailwind classes for unknown elements."""
        classes = []
        
        # Add basic typography classes
        if "typography" in tokens:
            classes.append("text-sm")
        
        # Add basic spacing classes
        if "spacing" in tokens:
            classes.append("p-4")
        
        return classes
    
    def generate_responsive_classes(
        self,
        base_classes: str,
        breakpoints: Dict[str, str]
    ) -> str:
        """
        Generate responsive Tailwind classes.
        
        Args:
            base_classes: Base class string
            breakpoints: Dict of breakpoint -> classes (e.g., {"md": "px-8", "lg": "px-12"})
        
        Returns:
            Combined class string with responsive variants
        """
        classes = [base_classes]
        
        for breakpoint, bp_classes in breakpoints.items():
            # Add breakpoint prefix to each class
            prefixed = " ".join(f"{breakpoint}:{cls}" for cls in bp_classes.split())
            classes.append(prefixed)
        
        return " ".join(classes)
    
    def generate_state_classes(
        self,
        base_classes: str,
        states: List[str]
    ) -> str:
        """
        Generate state variant classes (hover, focus, active, disabled).
        
        Args:
            base_classes: Base class string
            states: List of states to generate (e.g., ["hover", "focus"])
        
        Returns:
            Combined class string with state variants
        """
        classes = [base_classes]
        
        for state in states:
            # Common state variants
            if state == "hover":
                classes.append("hover:opacity-90")
            elif state == "focus":
                classes.append("focus:ring-2 focus:ring-offset-2")
            elif state == "active":
                classes.append("active:scale-95")
            elif state == "disabled":
                classes.append("disabled:opacity-50 disabled:pointer-events-none")
        
        return " ".join(classes)
