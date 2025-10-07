"""
Prompt Builder for LLM Code Generation

Constructs comprehensive prompts for generating React/TypeScript components.
Includes pattern reference, design tokens, requirements, and examples.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json

# Try to import tiktoken for accurate token counting
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


@dataclass
class PromptTemplate:
    """Template for LLM prompts."""
    system_prompt: str
    user_prompt_template: str
    version: str = "1.0.0"


class PromptBuilder:
    """
    Build comprehensive prompts for component generation.
    
    Constructs prompts that include:
    - Pattern reference code
    - Design tokens with semantic meaning
    - Requirements (props, events, states, a11y)
    - Component naming and conventions
    - Validation constraints
    """
    
    # System prompt that defines the AI's role and capabilities
    SYSTEM_PROMPT = """You are an expert React and TypeScript developer specializing in creating accessible, production-ready UI components following shadcn/ui conventions.

Your expertise includes:
- Writing clean, type-safe TypeScript with strict mode (no 'any' types)
- Creating accessible components with proper ARIA attributes
- Following React best practices and modern patterns
- Implementing design systems with design tokens
- Writing comprehensive Storybook stories

CRITICAL REQUIREMENTS:
1. **Self-contained code**: Do NOT import from '@/lib/utils' or any utility files
2. **ALWAYS inline the cn utility** at the top of your component:
   ```typescript
   // Inline utility for merging classes
   const cn = (...classes: (string | undefined | null | false)[]) =>
     classes.filter(Boolean).join(' ');
   ```
3. **Use cn() for all className merging** - NEVER use template literals like `bg-${variant}`
4. **Static Tailwind classes only** - Use conditional logic, not dynamic class names
5. **Proper TypeScript** - NO 'any' types, including 'as any'
6. **Conditional button semantics** - Only add role="button"/tabIndex if onClick exists

Example of correct className usage with design tokens:
```typescript
// Button example - Complete styling with proper defaults
className={cn(
  // Base styles: layout, spacing, borders, transitions (REQUIRED)
  "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors",
  // Border for outline variant
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
  // Color variants using extracted design tokens
  variant === "primary" && "bg-[#3B82F6] text-white hover:bg-[#2563EB]",
  variant === "secondary" && "bg-[#6B7280] text-white hover:bg-[#4B5563]",
  variant === "outline" && "border border-[#E5E7EB] bg-transparent hover:bg-[#F3F4F6]",
  // State modifiers
  disabled && "opacity-50 cursor-not-allowed",
  className
)}

// Card example - Complete card styling
className={cn(
  // Base styles: MUST include border, padding, rounded corners
  "border border-[#E5E7EB] rounded-lg p-6 bg-white",
  // Optional enhancements
  shadow && "shadow-md",
  interactive && "hover:shadow-lg transition-shadow cursor-pointer",
  variant === "primary" && "border-[#3B82F6] bg-[#EFF6FF]",
  className
)}
```

**CRITICAL**: Every component MUST have complete functional styling by default:
- Cards MUST have: `border`, `border-[color]`, `rounded-lg`, `p-4` or `p-6`, background
- Buttons MUST have: `px-4 py-2`, `rounded-md`, `font-medium`, background, hover states
- Inputs MUST have: `border`, padding, `rounded-md`, focus states

**IMPORTANT**: When design tokens specify colors, use the EXACT color values provided:
- If tokens specify `primary: #3B82F6`, use `bg-[#3B82F6]` (not `bg-blue-500`)
- If tokens specify `secondary: rgb(107, 114, 128)`, use `bg-[rgb(107,114,128)]`
- This ensures the component matches the extracted design system exactly

You generate complete, working component code that compiles without errors."""

    # Template for the user prompt
    USER_PROMPT_TEMPLATE = """## Task
Generate a production-ready React component based on the requirements below.

## Reference Pattern (shadcn/ui)
Use this pattern as a reference for style and structure. DO NOT copy it directly - adapt it to meet the specific requirements.

```tsx
{pattern_code}
```

## Component Information
**Name**: {component_name}
**Type**: {component_type}
**Description**: {component_description}

## Design Tokens
Apply these design tokens to the component using CSS variables.

{design_tokens}

## Component Base Styling Requirements

Based on the component type **{component_type}**, ensure these base styles are included:

**Card components:**
- Base: `border border-[extracted-color] rounded-lg p-6 bg-white`
- Must be visually distinct as a container with clear boundaries
- Include proper spacing between content

**Button components:**
- Base: `inline-flex items-center justify-center px-4 py-2 rounded-md font-medium transition-colors`
- Must have visible background and hover states
- Include focus-visible styles for accessibility

**Input/Form components:**
- Base: `border border-[extracted-color] rounded-md px-3 py-2 w-full`
- Must have visible border and focus states
- Include proper spacing for text content

**If component type doesn't match above, use appropriate spacing, borders, and visual hierarchy for the component type.**

## Requirements

### Props
{props_requirements}

### Events
{events_requirements}

### States
{states_requirements}

### Accessibility
{accessibility_requirements}

## Constraints
- **MUST inline cn utility** - First line inside component should define the cn function
- **MUST use cn() for className** - NEVER use template literals for dynamic classes
- **Static Tailwind classes only** - No `bg-${{variant}}`, use conditionals instead
- **MUST use EXACT extracted token values** - Use `bg-[#3B82F6]` with the exact color from design tokens
- **MUST include complete base styling** - Every component needs padding, borders, rounded corners, etc.
- **Cards MUST have**: `border border-[color] rounded-lg p-6 bg-white` as base styles
- **Buttons MUST have**: `px-4 py-2 rounded-md font-medium` plus background/hover states
- **Inputs MUST have**: `border border-[color] rounded-md px-3 py-2` plus focus states
- Match colors EXACTLY to the design tokens provided (don't approximate with Tailwind color names)
- TypeScript strict mode (no 'any' types allowed, including 'as any')
- All props must have explicit types
- Only add role="button" and tabIndex if onClick prop exists
- Include proper ARIA attributes for accessibility
- Use Tailwind arbitrary values for extracted colors: `bg-[#HEX]`, `text-[rgb(r,g,b)]`, etc.
- Export component with displayName set
- Include proper JSDoc comments for props
- Component must compile without TypeScript errors
- Component must pass ESLint validation
- **Showcase MUST have descriptions**: Each variant must include technical description with exact values (colors, spacing, purpose)

## Output Format
**CRITICAL: You MUST return ALL THREE code files!**

Return a JSON object with the following structure:
{{
  "component_code": "complete .tsx file content (REQUIRED)",
  "stories_code": "complete .stories.tsx file content for Storybook (REQUIRED)",
  "showcase_code": "complete .showcase.tsx file that renders all variations (REQUIRED - see example below)",
  "imports": ["list of import statements"],
  "exports": ["list of exported names"],
  "explanation": "brief explanation of key implementation decisions"
}}

**IMPORTANT**: If showcase_code is missing or empty, your response will be rejected!

### Showcase File Example
The showcase file should render all component variations with DETAILED DESCRIPTIONS:

```tsx
import {{ {component_name} }} from './{component_name}';

export default function {component_name}Showcase() {{
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-2">{component_name}</h2>
        <p className="text-gray-600">Generated by Component Forge</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {{/* Each variation MUST have a descriptive title and explanation */}}
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-gray-900">Default Variant</h3>
          <div className="p-6 bg-white rounded-lg border">
            <{component_name}>Example Content</{component_name}>
          </div>
          <p className="text-sm text-gray-600">
            This is the default variant with standard styling.
            Uses base colors and spacing. Border: 1px solid #E5E7EB.
            Padding: 24px. Border-radius: 12px.
          </p>
        </div>

        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-gray-900">Primary Variant</h3>
          <div className="p-6 bg-white rounded-lg border">
            <{component_name} variant="primary">Example Content</{component_name}>
          </div>
          <p className="text-sm text-gray-600">
            Primary variant with brand color emphasis.
            Background: #3B82F6. Text: White.
            Used for main actions or highlighted content.
          </p>
        </div>

        {{/* Add more variations with descriptions for ALL props/variants */}}
      </div>
    </div>
  );
}}
```

**CRITICAL**: Each showcase variation MUST include:
1. **Descriptive title**: What the variant is called (e.g., "Primary Variant", "With Shadow")
2. **Component example**: Actual rendered component with the variant
3. **Technical description**: Explain the styling (colors, spacing, effects, purpose)
   - Include exact values: padding, border-radius, colors, shadows
   - Explain when to use this variant
   - Describe visual differences from other variants

Generate complete, working code that meets all requirements."""

    def __init__(self):
        """Initialize prompt builder."""
        self.template = PromptTemplate(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt_template=self.USER_PROMPT_TEMPLATE,
        )
    
    def build_prompt(
        self,
        pattern_code: str,
        component_name: str,
        component_type: str,
        tokens: Dict[str, Any],
        requirements: Dict[str, Any],
        component_description: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Build a complete prompt for component generation.
        
        Args:
            pattern_code: Reference pattern code (shadcn/ui)
            component_name: Name of the component to generate
            component_type: Type (button, card, input, etc.)
            tokens: Design tokens (colors, typography, spacing)
            requirements: Component requirements (props, events, states, a11y)
            component_description: Optional description of the component
        
        Returns:
            Dict with 'system' and 'user' prompts
        """
        # Format design tokens
        tokens_str = self._format_design_tokens(tokens)
        
        # Format requirements by category
        props_str = self._format_requirements(
            requirements.get("props", []),
            "No specific props required. Use common patterns for this component type."
        )
        
        events_str = self._format_requirements(
            requirements.get("events", []),
            "No specific events required. Include standard event handlers."
        )
        
        states_str = self._format_requirements(
            requirements.get("states", []),
            "No specific state requirements. Use appropriate state management."
        )
        
        a11y_str = self._format_requirements(
            requirements.get("accessibility", []),
            "Follow WCAG 2.1 AA standards with proper ARIA attributes."
        )
        
        # Build user prompt
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            pattern_code=pattern_code,
            component_name=component_name,
            component_type=component_type,
            component_description=component_description or f"A {component_type} component",
            design_tokens=tokens_str,
            props_requirements=props_str,
            events_requirements=events_str,
            states_requirements=states_str,
            accessibility_requirements=a11y_str,
        )
        
        return {
            "system": self.SYSTEM_PROMPT,
            "user": user_prompt,
        }
    
    def _format_design_tokens(self, tokens: Dict[str, Any]) -> str:
        """Format design tokens for the prompt."""
        sections = []

        # Format colors with usage instructions
        if "colors" in tokens and tokens["colors"]:
            colors = tokens["colors"]
            color_lines = []
            for name, value in colors.items():
                # Show token name, value, and how to use it
                color_lines.append(f"  - {name}: `{value}` → Use as `bg-[{value}]` or `text-[{value}]`")
            sections.append("**Colors:**\n" + "\n".join(color_lines))
        
        # Format typography
        if "typography" in tokens and tokens["typography"]:
            typo = tokens["typography"]
            typo_lines = []
            for key, value in typo.items():
                typo_lines.append(f"  - {key}: {value}")
            sections.append("**Typography:**\n" + "\n".join(typo_lines))
        
        # Format spacing
        if "spacing" in tokens and tokens["spacing"]:
            spacing = tokens["spacing"]
            spacing_lines = []
            for key, value in spacing.items():
                spacing_lines.append(f"  - {key}: {value}")
            sections.append("**Spacing:**\n" + "\n".join(spacing_lines))
        
        # Format borders
        if "borders" in tokens and tokens["borders"]:
            borders = tokens["borders"]
            border_lines = []
            for key, value in borders.items():
                border_lines.append(f"  - {key}: {value}")
            sections.append("**Borders:**\n" + "\n".join(border_lines))
        
        if not sections:
            return "No specific design tokens provided. Use sensible defaults."
        
        return "\n\n".join(sections)
    
    def _format_requirements(
        self, 
        requirements: List[Dict[str, Any]], 
        default_message: str
    ) -> str:
        """Format requirements list for the prompt."""
        if not requirements:
            return default_message
        
        lines = []
        for req in requirements:
            # Handle different requirement formats
            if isinstance(req, dict):
                name = req.get("name", "")
                req_type = req.get("type", "")
                description = req.get("description", "")
                
                if name:
                    line = f"- **{name}**"
                    if req_type:
                        line += f" ({req_type})"
                    if description:
                        line += f": {description}"
                    lines.append(line)
            elif isinstance(req, str):
                lines.append(f"- {req}")
        
        return "\n".join(lines) if lines else default_message
    
    def estimate_token_count(self, prompts: Dict[str, str]) -> int:
        """
        Estimate token count for the prompts.
        
        Uses tiktoken for accurate counting if available, otherwise falls back
        to rough estimate (~4 characters per token).
        
        Args:
            prompts: Dict with 'system' and 'user' prompts
        
        Returns:
            Estimated token count
        """
        if TIKTOKEN_AVAILABLE:
            try:
                # Use tiktoken for accurate token counting
                encoder = tiktoken.encoding_for_model("gpt-4o")
                system_tokens = len(encoder.encode(prompts["system"]))
                user_tokens = len(encoder.encode(prompts["user"]))
                return system_tokens + user_tokens
            except Exception:
                # Fall back to rough estimate if encoding fails
                pass
        
        # Fallback: rough estimate
        total_chars = len(prompts["system"]) + len(prompts["user"])
        return total_chars // 4
    
    def truncate_pattern_if_needed(
        self, 
        pattern_code: str, 
        max_lines: int = 200
    ) -> str:
        """
        Truncate pattern code if it's too long.
        
        Args:
            pattern_code: Pattern code to potentially truncate
            max_lines: Maximum number of lines to keep
        
        Returns:
            Potentially truncated pattern code
        """
        lines = pattern_code.split('\n')
        if len(lines) <= max_lines:
            return pattern_code
        
        # Keep first portion and add truncation notice
        truncated = '\n'.join(lines[:max_lines])
        truncated += f"\n\n// ... truncated {len(lines) - max_lines} lines ..."
        return truncated
