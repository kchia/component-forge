"""Component classifier prompts with few-shot examples.

This module contains the prompt templates and examples for component
type classification using GPT-4V.
"""

# Main classification prompt template
COMPONENT_CLASSIFICATION_PROMPT = """Analyze this UI component and identify its type.

You are an expert UI/UX designer analyzing component screenshots. Your task is to accurately classify the component type based on visual cues, layout patterns, and interactive elements.

## Supported Component Types

1. **Button**: Interactive clickable element
   - Visual cues: Rounded corners, clear boundaries, call-to-action text
   - Variants: Primary (solid background), Secondary (outlined), Ghost (text only)
   - Common patterns: "Sign In", "Submit", "Cancel", icon + text
   - Cursor: Usually `pointer` on hover

2. **Card**: Content container with grouped information
   - Visual cues: Box with border/shadow, contains title + description/image
   - Layout: Vertical stack with padding, often has header/body/footer sections
   - Common patterns: Product cards, user profiles, article previews
   - Cursor: Sometimes `pointer` if clickable

3. **Input**: Text input field
   - Visual cues: Rectangular field with border, often has label above/inside
   - States: Default, focused (highlighted border), error (red border)
   - Common patterns: Email input, password field, search box
   - Cursor: `text` cursor when hovering over input area

4. **Select**: Dropdown selection control
   - Visual cues: Field with down arrow/chevron icon on the right
   - Layout: Similar to input but with dropdown indicator
   - Common patterns: Country selector, dropdown menu, combobox
   - Cursor: `pointer` on the dropdown

5. **Badge**: Small status or label indicator
   - Visual cues: Compact, pill-shaped or rounded rectangle
   - Content: Short text or number (1-2 words)
   - Common patterns: Status tags, notification counts, category labels
   - Colors: Often uses semantic colors (red=error, green=success)

6. **Alert**: Notification or message banner
   - Visual cues: Full-width or prominent box with icon + message
   - Layout: Horizontal layout with icon, text, and optional close button
   - Common patterns: Success message, error alert, warning banner
   - Colors: Uses semantic colors matching severity

{figma_context}

## Classification Guidelines

1. **Visual Analysis**:
   - Shape: Rectangle? Pill? Square?
   - Size: Small badge? Medium button? Large card?
   - Layout: Single element? Container with children?
   - Interactive cues: Cursor styles, shadows, hover states

2. **Text Content**:
   - Action words → likely Button ("Submit", "Cancel")
   - Descriptive content → likely Card (title + description)
   - Labels → likely Input/Select (form fields)
   - Status text → likely Badge/Alert

3. **Color Patterns**:
   - Solid brand color → Primary Button
   - Outlined → Secondary Button
   - Semantic colors → Badge/Alert
   - Neutral/white → Card/Input

4. **Confidence Scoring**:
   - **High (0.9-1.0)**: Clear visual indicators, matches all patterns
   - **Medium (0.7-0.9)**: Most indicators present, some ambiguity
   - **Low (< 0.7)**: Ambiguous, could be multiple types

## Few-Shot Examples

### Example 1: Primary Button
**Visual Description**: Rounded rectangle, solid blue background, white text "Sign In", centered alignment, subtle shadow
**Analysis**:
- Shape: Rounded rectangle → Button candidate
- Color: Solid background → Primary variant
- Text: Action word → Confirms Button
- Size: Compact, single line → Not Card/Alert
**Classification**: Button (confidence: 0.95)
**Rationale**: Clear button pattern with solid background, action-oriented text, and interactive styling

### Example 2: Product Card
**Visual Description**: White box with shadow, contains product image at top, title "Premium Headphones" below, price "$299", and star rating
**Analysis**:
- Layout: Vertical container with multiple elements → Card candidate
- Content: Image + text + metadata → Confirms Card
- Border: Subtle shadow/border → Card pattern
- Size: Larger than button → Not Button/Badge
**Classification**: Card (confidence: 0.92)
**Rationale**: Contains grouped content in container layout with clear visual hierarchy

### Example 3: Email Input
**Visual Description**: Rectangular field with light gray border, "Email address" label above, placeholder text "Enter your email", blinking text cursor visible
**Analysis**:
- Shape: Rectangular input area → Input candidate
- Label: "Email address" → Form field pattern
- Cursor: Text cursor visible → Confirms Input
- Border: Focused state visible → Interactive input
**Classification**: Input (confidence: 0.94)
**Rationale**: Classic input field with label, focused state, and text cursor

### Example 4: Status Badge
**Visual Description**: Small pill-shaped element, green background, white text "Active", compact size
**Analysis**:
- Size: Very small, compact → Badge candidate
- Shape: Pill-shaped → Badge pattern
- Content: Single status word → Confirms Badge
- Color: Semantic green → Status indicator
**Classification**: Badge (confidence: 0.90)
**Rationale**: Compact status indicator with semantic color

### Example 5: Ambiguous Case - Clickable Card vs Large Button
**Visual Description**: Large rectangular element, light background, icon + "Upload File" text, full width
**Analysis**:
- Could be Button: Has action text, single clickable element
- Could be Card: Larger size, contains icon + text layout
- Confidence: Medium due to ambiguity
**Classification**: Button (confidence: 0.75)
**Candidates**: [
  {{"type": "Button", "confidence": 0.75}},
  {{"type": "Card", "confidence": 0.65}}
]
**Rationale**: Primarily action-oriented despite size; text "Upload File" indicates interaction over content display

## Output Format

Return a JSON object with this exact structure:

```json
{{
  "component_type": "Button|Card|Input|Select|Badge|Alert",
  "confidence": 0.0-1.0,
  "candidates": [
    {{"type": "ComponentType", "confidence": 0.0-1.0}}
  ],
  "rationale": "detailed explanation citing specific visual cues"
}}
```

**Rules**:
1. `component_type` must be one of the 6 supported types (exact match)
2. `confidence` must be between 0.0 and 1.0
3. If confidence < 0.8, provide 2-3 alternative candidates
4. `rationale` must cite specific visual cues from the image
5. Candidates should be sorted by confidence (highest first)

## Analysis Instructions

Now analyze the provided component image:
1. Examine the visual appearance, shape, and layout
2. Consider the text content and labels
3. Look for interactive indicators (cursor styles, shadows)
4. Apply the classification guidelines above
5. Choose the best matching component type
6. Calculate confidence based on how well it matches the patterns
7. Provide alternative candidates if ambiguous (confidence < 0.8)
8. Write a clear rationale citing specific visual evidence

Return only the JSON object, nothing else.
"""


def create_classification_prompt(figma_data: dict = None) -> str:
    """Create a classification prompt with optional Figma context.
    
    Args:
        figma_data: Optional Figma layer/component metadata
        
    Returns:
        Formatted classification prompt
    """
    figma_context = ""
    
    if figma_data:
        layer_name = figma_data.get("name", "")
        layer_type = figma_data.get("type", "")
        
        if layer_name or layer_type:
            figma_context = "## Figma Context\n\n"
            
        if layer_name:
            figma_context += f"**Layer name**: {layer_name}\n"
            figma_context += "- Use layer name as a hint (e.g., 'btn-primary' likely indicates Button)\n"
            
        if layer_type:
            figma_context += f"**Figma type**: {layer_type}\n"
            
        # Check for component variants
        if "variants" in figma_data:
            variants = figma_data.get("variants", [])
            if variants:
                figma_context += f"**Component variants detected**: {', '.join(variants)}\n"
                figma_context += "- Variants suggest this is a reusable component with multiple states\n"
        
        figma_context += "\n"
    
    return COMPONENT_CLASSIFICATION_PROMPT.format(figma_context=figma_context)


# Export prompt for use in classifier
__all__ = ["COMPONENT_CLASSIFICATION_PROMPT", "create_classification_prompt"]
