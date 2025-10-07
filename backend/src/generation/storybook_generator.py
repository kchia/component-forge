"""
Storybook Story Generator - Generate Storybook stories in CSF 3.0 format.

This module generates Storybook stories for all component variants with
interactive controls, documentation, and example code snippets.
"""

from typing import List, Dict, Any


class StorybookGenerator:
    """
    Generate Storybook stories in CSF 3.0 format.
    """
    
    def __init__(self):
        """Initialize Storybook generator."""
        # Storybook version
        self.storybook_version = "8.0"
        self.csf_version = "3.0"
    
    def generate_stories(
        self,
        component_name: str,
        variants: List[str],
        props: List[Dict[str, Any]],
        component_type: str = "button"
    ) -> str:
        """
        Generate Storybook stories for component.
        
        Args:
            component_name: Name of the component
            variants: List of variant names
            props: List of prop definitions
            component_type: Type of component
        
        Returns:
            Complete Storybook stories file in CSF 3.0 format
        """
        # Build imports
        imports = self._generate_imports(component_name)
        
        # Build meta object
        meta = self._generate_meta(component_name, props)
        
        # Build variant stories
        stories = self._generate_variant_stories(
            component_name,
            variants,
            props,
            component_type
        )
        
        # Build state stories
        state_stories = self._generate_state_stories(
            component_name,
            component_type
        )
        
        # Combine all parts
        full_stories = "\n\n".join([
            imports,
            meta,
            stories,
            state_stories
        ])
        
        return full_stories
    
    def _generate_imports(self, component_name: str) -> str:
        """Generate import statements."""
        return f"""import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {component_name} }} from './{component_name}';"""
    
    def _generate_meta(
        self,
        component_name: str,
        props: List[Dict[str, Any]]
    ) -> str:
        """
        Generate meta object with configuration.
        
        Args:
            component_name: Name of component
            props: List of prop definitions
        
        Returns:
            Meta object definition
        """
        # Build argTypes for controls
        arg_types = self._generate_arg_types(props)
        
        meta = f"""const meta: Meta<typeof {component_name}> = {{
  title: 'Components/{component_name}',
  component: {component_name},
  tags: ['autodocs'],
  argTypes: {{
{arg_types}
  }},
}};

export default meta;
type Story = StoryObj<typeof {component_name}>;"""
        
        return meta
    
    def _generate_arg_types(self, props: List[Dict[str, Any]]) -> str:
        """
        Generate argTypes for Storybook controls.
        
        Args:
            props: List of prop definitions
        
        Returns:
            ArgTypes object properties
        """
        arg_types = []
        
        for prop in props:
            prop_name = prop.get("name", "")
            prop_type = prop.get("type", "string")
            description = prop.get("description", "")
            
            # Determine control type
            control = self._get_control_type(prop_type)
            
            arg_type = f"    {prop_name}: {{"
            
            if description:
                arg_type += f"\n      description: '{description}',"
            
            arg_type += f"\n      control: '{control}',"
            arg_type += "\n    },"
            
            arg_types.append(arg_type)
        
        # Add common props
        arg_types.append("""    className: {
      description: 'Additional CSS classes',
      control: 'text',
    },""")
        
        return "\n".join(arg_types)
    
    def _get_control_type(self, prop_type: str) -> str:
        """
        Get Storybook control type for prop type.
        
        Args:
            prop_type: Property type
        
        Returns:
            Storybook control type
        """
        control_mapping = {
            "string": "text",
            "number": "number",
            "boolean": "boolean",
            "function": "none",
            "array": "object",
            "object": "object",
        }
        
        # Check for enum/variant types
        if "|" in prop_type:
            return "select"
        
        return control_mapping.get(prop_type.lower(), "text")
    
    def _generate_variant_stories(
        self,
        component_name: str,
        variants: List[str],
        props: List[Dict[str, Any]],
        component_type: str
    ) -> str:
        """
        Generate stories for each variant.
        
        Args:
            component_name: Name of component
            variants: List of variant names
            props: List of prop definitions
            component_type: Type of component
        
        Returns:
            Variant story definitions
        """
        stories = []
        
        # Default story
        default_args = self._get_default_args(component_type)
        default_story = f"""export const Default: Story = {{
  args: {{
{default_args}
  }},
}};"""
        stories.append(default_story)
        
        # Variant stories
        for variant in variants:
            if variant.lower() == "default":
                continue
            
            variant_name = variant.capitalize()
            variant_args = self._get_variant_args(variant, component_type)
            
            variant_story = f"""export const {variant_name}: Story = {{
  args: {{
    variant: '{variant}',
{variant_args}
  }},
}};"""
            stories.append(variant_story)
        
        return "\n\n".join(stories)
    
    def _generate_state_stories(
        self,
        component_name: str,
        component_type: str
    ) -> str:
        """
        Generate stories for different states.
        
        Args:
            component_name: Name of component
            component_type: Type of component
        
        Returns:
            State story definitions
        """
        stories = []
        
        # Disabled state
        if component_type in ["button", "input", "checkbox", "radio", "select"]:
            disabled_args = self._get_default_args(component_type)
            disabled_story = f"""export const Disabled: Story = {{
  args: {{
{disabled_args}
    disabled: true,
  }},
}};"""
            stories.append(disabled_story)
        
        # Loading state for buttons
        if component_type == "button":
            loading_args = self._get_default_args(component_type)
            loading_story = f"""export const Loading: Story = {{
  args: {{
{loading_args}
    loading: true,
  }},
}};"""
            stories.append(loading_story)
        
        # Error state for inputs
        if component_type == "input":
            error_args = self._get_default_args(component_type)
            error_story = f"""export const WithError: Story = {{
  args: {{
{error_args}
    error: 'This field is required',
  }},
}};"""
            stories.append(error_story)
        
        return "\n\n".join(stories) if stories else ""
    
    def _get_default_args(self, component_type: str) -> str:
        """
        Get default args for component type.
        
        Args:
            component_type: Type of component
        
        Returns:
            Default args string
        """
        args_mapping = {
            "button": "    children: 'Button',",
            "input": "    placeholder: 'Enter text...',",
            "card": "    children: 'Card content',",
            "badge": "    children: 'Badge',",
            "alert": "    children: 'This is an alert message',",
            "checkbox": "    label: 'Checkbox label',",
            "radio": "    label: 'Radio label',",
            "select": "    placeholder: 'Select an option',",
            "switch": "    label: 'Switch label',",
            "tabs": "    defaultValue: 'tab1',",
        }
        
        return args_mapping.get(component_type.lower(), "    children: 'Component',")
    
    def _get_variant_args(self, variant: str, component_type: str) -> str:
        """
        Get variant-specific args.
        
        Args:
            variant: Variant name
            component_type: Type of component
        
        Returns:
            Variant args string
        """
        default_args = self._get_default_args(component_type)
        
        # Remove leading spaces and add appropriate spacing
        return default_args.strip().replace("    ", "    ")
    
    def generate_play_function(self, component_type: str) -> str:
        """
        Generate play function for interaction testing.
        
        Args:
            component_type: Type of component
        
        Returns:
            Play function code
        """
        if component_type == "button":
            return """  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    await userEvent.click(button);
  },"""
        
        return ""
    
    def add_parameters(self, component_type: str) -> str:
        """
        Add Storybook parameters for documentation.
        
        Args:
            component_type: Type of component
        
        Returns:
            Parameters object
        """
        return """  parameters: {
    docs: {
      description: {
        component: 'A reusable component built with shadcn/ui',
      },
    },
  },"""
