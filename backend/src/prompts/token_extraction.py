"""Prompt templates for design token extraction."""

TOKEN_EXTRACTION_PROMPT = """Analyze this design system screenshot and extract design tokens.

You are a design system expert analyzing UI components to extract design tokens (colors, typography, spacing).

IMPORTANT: Return ONLY a valid JSON object with the exact structure shown below. Do not include any markdown, explanations, or text outside the JSON.

Return a JSON object with this EXACT structure:
{
  "colors": {
    "primary": {"value": "#HEX", "confidence": 0.0-1.0},
    "background": {"value": "#HEX", "confidence": 0.0-1.0},
    "foreground": {"value": "#HEX", "confidence": 0.0-1.0},
    "secondary": {"value": "#HEX", "confidence": 0.0-1.0}
  },
  "typography": {
    "fontFamily": {"value": "string", "confidence": 0.0-1.0},
    "fontSize": {"value": "16px", "confidence": 0.0-1.0},
    "fontWeight": {"value": 500, "confidence": 0.0-1.0},
    "lineHeight": {"value": "1.5", "confidence": 0.0-1.0}
  },
  "spacing": {
    "padding": {"value": "16px", "confidence": 0.0-1.0},
    "gap": {"value": "8px", "confidence": 0.0-1.0},
    "margin": {"value": "16px", "confidence": 0.0-1.0},
    "baseUnit": {"value": "4px", "confidence": 0.0-1.0}
  },
  "borderRadius": {
    "default": {"value": "8px", "confidence": 0.0-1.0}
  }
}

EXTRACTION GUIDELINES:

1. COLORS (hex format only):
   - primary: Main action/brand color (buttons, links)
   - background: Main background color
   - foreground: Text/icon color
   - secondary: Secondary/muted colors
   - Use confidence based on clarity and consistency in the image

2. TYPOGRAPHY:
   - fontFamily: Infer from visual appearance (e.g., "Inter", "Roboto", "Arial")
   - fontSize: Base text size in px (e.g., "14px", "16px")
   - fontWeight: 100-900 (e.g., 400=normal, 500=medium, 600=semibold, 700=bold)
   - lineHeight: Relative line height (e.g., "1.5", "1.6")
   - Lower confidence for font family (hard to identify exactly from visuals)

3. SPACING:
   - padding: Internal spacing in px
   - gap: Space between elements in px
   - margin: External spacing in px
   - baseUnit: Detect base spacing unit (commonly "4px" or "8px")
   - Look for consistent multiples (8px, 16px, 24px suggests 8px base)

4. BORDER RADIUS:
   - default: Corner radius in px (e.g., "4px", "8px", "12px")

CONFIDENCE SCORING (0.0 to 1.0):
- 0.9-1.0: Very certain (clear, consistent, obvious)
  Example: Button color is solid and uniform throughout (e.g., #3B82F6 with no variation)
- 0.7-0.9: Confident (visible but some ambiguity)
  Example: Color varies slightly due to gradient, shadow, or hover state visible
- 0.5-0.7: Moderate (estimated, not very clear)
  Example: Color is partially obscured or affected by transparency/overlay
- 0.0-0.5: Low confidence (guessing, unclear)
  Example: Token not clearly visible in the image

IMPORTANT NOTES:
- If a token is not visible in the image, set confidence to 0.0 and provide a reasonable default
- For font family, confidence should typically be 0.5-0.7 (hard to identify exact font from visuals)
- For colors, confidence should be high (0.8-1.0) if clearly visible with consistent appearance
- For spacing, confidence should be high (0.8-1.0) if elements have clear, measurable gaps
- Return ONLY the JSON object, no additional text
- All color values must be in uppercase hex format (e.g., "#3B82F6")
- All size values must include "px" unit
- Font weight must be a number (400, 500, 600, 700)
"""


def create_extraction_prompt() -> str:
    """Create the token extraction prompt for GPT-4V.
    
    Returns:
        Formatted prompt string
    """
    return TOKEN_EXTRACTION_PROMPT
