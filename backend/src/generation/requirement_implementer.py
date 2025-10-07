"""
Requirement Implementer - Implement approved requirements in components.

This module takes requirements from Epic 2 and implements them as props,
event handlers, states, and validation logic in the component code.
"""

from typing import Dict, Any, List


class RequirementImplementer:
    """
    Implement approved requirements from Epic 2 in component code.
    """
    
    def implement(
        self,
        component_code: str,
        requirements: Dict[str, Any],
        component_name: str = "Component"
    ) -> Dict[str, Any]:
        """
        Implement requirements in component code.
        
        Args:
            component_code: Original component code
            requirements: Requirements from Epic 2
            component_name: Name of the component
        
        Returns:
            Dictionary with:
                - modified_code: Updated component code
                - props_interface: Generated props interface
                - events: List of event handlers added
                - states: List of states added
        """
        # Generate props interface from requirements
        props_interface = self._generate_props_interface(
            requirements.get("props", []),
            component_name
        )
        
        # Generate event handler types
        event_handlers = self._generate_event_handlers(
            requirements.get("events", [])
        )
        
        # Generate state management code
        state_code = self._generate_state_management(
            requirements.get("states", [])
        )
        
        # For MVP, return the generated code parts
        # Full AST manipulation deferred to post-MVP
        return {
            "modified_code": component_code,
            "props_interface": props_interface,
            "event_handlers": event_handlers,
            "state_code": state_code,
            "events": requirements.get("events", []),
            "states": requirements.get("states", [])
        }
    
    def _generate_props_interface(
        self,
        props: List[Dict[str, Any]],
        component_name: str
    ) -> str:
        """
        Generate TypeScript props interface from requirements.
        
        Args:
            props: List of prop definitions from requirements
            component_name: Name of the component
        
        Returns:
            TypeScript interface definition
        """
        if not props:
            return f"export interface {component_name}Props {{\n  // No additional props\n}}"
        
        interface_lines = [f"export interface {component_name}Props {{"]
        
        for prop in props:
            name = prop.get("name", "")
            prop_type = self._infer_prop_type(prop)
            optional = "?" if not prop.get("required", False) else ""
            description = prop.get("description", "")
            
            # Add JSDoc comment if description exists
            if description:
                interface_lines.append(f"  /** {description} */")
            
            # Add prop definition
            interface_lines.append(f"  {name}{optional}: {prop_type};")
        
        interface_lines.append("}")
        
        return "\n".join(interface_lines)
    
    def _infer_prop_type(self, prop: Dict[str, Any]) -> str:
        """
        Infer TypeScript type from prop definition.
        
        Args:
            prop: Prop definition dictionary
        
        Returns:
            TypeScript type string
        """
        # Check for explicit type
        if "type" in prop:
            prop_type = prop["type"]
            
            # Handle primitive types
            if prop_type in ["string", "number", "boolean"]:
                return prop_type
            elif prop_type == "function":
                # Check for function signature
                if "signature" in prop:
                    return prop["signature"]
                return "() => void"
            elif prop_type == "object":
                return "Record<string, any>"
            elif prop_type == "array":
                return "any[]"
        
        # Check for enum values (union type)
        if "values" in prop and prop["values"]:
            values = prop["values"]
            if isinstance(values, list):
                # Create union type: "primary" | "secondary" | "ghost"
                quoted_values = [f'"{v}"' for v in values]
                return " | ".join(quoted_values)
        
        # Default to string
        return "string"
    
    def _generate_event_handlers(
        self,
        events: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate event handler type definitions.
        
        Args:
            events: List of event definitions from requirements
        
        Returns:
            List of event handler code snippets
        """
        handlers = []
        
        for event in events:
            name = event.get("name", "")
            event_type = event.get("type", "MouseEvent")
            
            # Generate handler type
            if name.startswith("on"):
                # e.g., onClick, onChange
                handler = f"{name}?: (event: React.{event_type}) => void;"
            else:
                # Add "on" prefix
                handler_name = f"on{name.capitalize()}"
                handler = f"{handler_name}?: (event: React.{event_type}) => void;"
            
            handlers.append(handler)
        
        return handlers
    
    def _generate_state_management(
        self,
        states: List[Dict[str, Any]]
    ) -> str:
        """
        Generate state management code using React hooks.
        
        Args:
            states: List of state definitions from requirements
        
        Returns:
            State management code snippet
        """
        if not states:
            return ""
        
        state_lines = []
        
        for state in states:
            name = state.get("name", "")
            state_type = state.get("type", "boolean")
            default_value = state.get("default", self._get_default_value(state_type))
            
            # Generate useState hook
            # e.g., const [isHovered, setIsHovered] = useState<boolean>(false);
            state_var = name
            setter_var = f"set{name.capitalize()}"
            
            state_line = f"const [{state_var}, {setter_var}] = useState<{state_type}>({default_value});"
            state_lines.append(state_line)
        
        return "\n  ".join(state_lines)
    
    def _get_default_value(self, type_str: str) -> str:
        """
        Get default value for a TypeScript type.
        
        Args:
            type_str: TypeScript type string
        
        Returns:
            Default value as string
        """
        defaults = {
            "boolean": "false",
            "string": '""',
            "number": "0",
            "object": "{}",
            "array": "[]"
        }
        
        return defaults.get(type_str, "undefined")
    
    def add_validation_logic(
        self,
        requirements: Dict[str, Any]
    ) -> str:
        """
        Generate validation logic for component props.
        
        Args:
            requirements: Requirements with validation rules
        
        Returns:
            Validation code snippet
        """
        validation_rules = requirements.get("validation", [])
        
        if not validation_rules:
            return ""
        
        validation_lines = []
        
        for rule in validation_rules:
            rule_type = rule.get("type", "")
            field = rule.get("field", "")
            
            if rule_type == "required":
                validation_lines.append(f"if (!{field}) {{")
                validation_lines.append(f'  console.error("{field} is required");')
                validation_lines.append("}")
            elif rule_type == "minLength":
                min_len = rule.get("value", 0)
                validation_lines.append(f"if ({field}.length < {min_len}) {{")
                validation_lines.append(f'  console.error("{field} must be at least {min_len} characters");')
                validation_lines.append("}")
            elif rule_type == "pattern":
                pattern = rule.get("value", "")
                validation_lines.append(f"if (!/{pattern}/.test({field})) {{")
                validation_lines.append(f'  console.error("{field} does not match pattern");')
                validation_lines.append("}")
        
        return "\n  ".join(validation_lines)
    
    def generate_accessibility_props(
        self,
        component_type: str,
        requirements: Dict[str, Any]
    ) -> List[str]:
        """
        Generate accessibility-related props based on component type.
        
        Args:
            component_type: Type of component
            requirements: Component requirements
        
        Returns:
            List of ARIA attribute definitions
        """
        aria_props = []
        
        if component_type == "button":
            aria_props.extend([
                'aria-label?: string;',
                'aria-disabled?: boolean;',
                'aria-busy?: boolean;'
            ])
            
            # Check if icon-only variant exists
            variants = requirements.get("variants", [])
            if any(v.get("name") == "icon" for v in variants):
                # Icon-only buttons require aria-label
                aria_props.append('// aria-label required for icon-only variant')
        
        elif component_type == "input":
            aria_props.extend([
                'aria-label?: string;',
                'aria-required?: boolean;',
                'aria-invalid?: boolean;',
                'aria-describedby?: string;'
            ])
        
        elif component_type == "card":
            aria_props.extend([
                'aria-label?: string;',
                'role?: string;'
            ])
        
        return aria_props
