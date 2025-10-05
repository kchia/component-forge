"""Accessibility requirement proposer.

This module analyzes components to propose accessibility requirements
such as aria-label, semantic HTML, and keyboard navigation.
"""

import json
import os
from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI
from PIL import Image

from .base_proposer import BaseRequirementProposer
from ..types.requirement_types import (
    RequirementProposal,
    RequirementCategory,
    ComponentClassification,
)
from ..services.image_processor import prepare_image_for_vision_api
from ..core.tracing import traced
from ..core.logging import get_logger

logger = get_logger(__name__)


class AccessibilityProposer(BaseRequirementProposer):
    """Propose accessibility requirements from component analysis.
    
    Detects:
    - aria-label requirements for screen readers
    - Semantic HTML recommendations
    - Keyboard navigation support
    - Color contrast considerations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the accessibility proposer.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        super().__init__(RequirementCategory.ACCESSIBILITY)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        # gpt-4o has vision capabilities and is the recommended model
        self.model = "gpt-4o"
    
    @traced(run_name="propose_accessibility")
    async def propose(
        self,
        image: Image.Image,
        classification: ComponentClassification,
        tokens: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> List[RequirementProposal]:
        """Propose accessibility requirements for the component.
        
        Args:
            image: Component screenshot
            classification: Component type classification
            tokens: Optional design tokens
            retry_count: Current retry attempt (for internal use)
            
        Returns:
            List of proposed accessibility requirements
        """
        logger.info(
            f"Proposing accessibility for {classification.component_type.value}",
            extra={
                "extra": {
                    "component_type": classification.component_type.value,
                    "has_tokens": tokens is not None,
                    "retry_count": retry_count,
                }
            }
        )
        
        try:
            # Prepare image
            image_data = prepare_image_for_vision_api(image)
            
            # Build accessibility analysis prompt (will use prompts module in next commit)
            prompt = self._build_accessibility_prompt(classification, tokens)
            
            # Call GPT-4V for accessibility analysis
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1500,
                temperature=0.2,
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Convert to proposals
            proposals = self._parse_accessibility_result(result, classification)
            
            # Log proposals
            for proposal in proposals:
                self.log_proposal(proposal)
            
            logger.info(
                f"Proposed {len(proposals)} accessibility requirements",
                extra={"extra": {"count": len(proposals)}}
            )
            
            return proposals
            
        except Exception as e:
            if retry_count < self.max_retries:
                logger.warning(
                    f"Accessibility proposal failed (attempt {retry_count + 1}), retrying: {e}",
                    extra={"extra": {"retry_count": retry_count, "error": str(e)}}
                )
                return await self.propose(
                    image, classification, tokens, retry_count + 1
                )
            else:
                logger.error(
                    f"Accessibility proposal failed after {self.max_retries} retries",
                    extra={
                        "extra": {
                            "max_retries": self.max_retries,
                            "error": str(e),
                        }
                    }
                )
                # Return empty list instead of raising to allow workflow to continue
                return []
    
    def _build_accessibility_prompt(
        self,
        classification: ComponentClassification,
        tokens: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build accessibility analysis prompt.
        
        This is a minimal prompt. Full prompt will be added in next commit.
        
        Args:
            classification: Component classification
            tokens: Optional design tokens
            
        Returns:
            Prompt text
        """
        component_type = classification.component_type.value
        
        prompt = f"""Analyze this {component_type} component and propose accessibility requirements.

Component Type: {component_type}

Analyze for these accessibility features:

1. **aria-label**: Screen reader text
   - Required when: Visual-only information, icon buttons, complex controls
   - Example: "Close dialog", "Submit form", "User profile menu"

2. **role**: ARIA role for semantic meaning
   - Required when: Non-semantic elements used
   - Examples: role="button", role="navigation", role="alert"

3. **Semantic HTML**: Proper HTML elements
   - Button component → <button> not <div>
   - Input component → <input> with proper type
   - Alert component → <div role="alert">

4. **Keyboard Navigation**: Keyboard accessible
   - Tab navigation support
   - Enter/Space for activation
   - Arrow keys for selection
   - Required: Almost always for interactive elements

5. **Color Contrast**: WCAG AA compliance (4.5:1 for normal text)
   - Check text on background
   - Important for readability

Return JSON with this structure:
{{
  "accessibility": [
    {{
      "name": "aria-label",
      "required": true,
      "description": "Descriptive label for screen readers",
      "visual_cues": ["icon-only button", "no visible text"],
      "confidence": 0.90
    }},
    {{
      "name": "keyboard-navigation",
      "required": true,
      "description": "Support Tab, Enter, Space keys",
      "visual_cues": ["interactive button", "clickable element"],
      "confidence": 0.95
    }}
  ]
}}

Focus on WCAG 2.1 Level AA compliance.
"""
        
        return prompt
    
    def _parse_accessibility_result(
        self,
        result: Dict[str, Any],
        classification: ComponentClassification
    ) -> List[RequirementProposal]:
        """Parse accessibility analysis result into proposals.
        
        Args:
            result: Raw JSON result from GPT-4V
            classification: Component classification for context
            
        Returns:
            List of RequirementProposal objects
        """
        proposals = []
        a11y_list = result.get("accessibility", [])
        
        for a11y_data in a11y_list:
            try:
                name = a11y_data.get("name", "unknown")
                required = a11y_data.get("required", True)  # Default to required for a11y
                description = a11y_data.get("description", "")
                visual_cues = a11y_data.get("visual_cues", [])
                base_confidence = float(a11y_data.get("confidence", 0.5))
                
                # Calculate adjusted confidence
                confidence = self.calculate_confidence(
                    base_confidence,
                    len(visual_cues),
                    min_cues=1,
                    max_cues=3
                )
                
                # Generate rationale
                rationale = self.generate_rationale(
                    name,
                    visual_cues,
                    source="accessibility analysis"
                )
                
                # Add WCAG context
                rationale += " (WCAG 2.1 Level AA)"
                
                # Create proposal
                proposal = self.create_proposal(
                    name=name,
                    confidence=confidence,
                    rationale=rationale,
                    required=required,
                    description=description,
                )
                
                proposals.append(proposal)
                
            except Exception as e:
                logger.warning(f"Failed to parse accessibility requirement: {e}")
                continue
        
        return proposals
