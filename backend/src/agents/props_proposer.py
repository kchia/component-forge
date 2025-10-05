"""Props requirement proposer.

This module analyzes components to propose prop requirements such as
variants, sizes, and boolean props.
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


class PropsProposer(BaseRequirementProposer):
    """Propose prop requirements from component analysis.
    
    Detects:
    - Variant props (primary, secondary, ghost)
    - Size props (sm, md, lg)
    - Boolean props (disabled, loading, fullWidth)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the props proposer.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        super().__init__(RequirementCategory.PROPS)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-4o"
    
    @traced(run_name="propose_props")
    async def propose(
        self,
        image: Image.Image,
        classification: ComponentClassification,
        tokens: Optional[Dict[str, Any]] = None,
    ) -> List[RequirementProposal]:
        """Propose prop requirements for the component.
        
        Args:
            image: Component screenshot
            classification: Component type classification
            tokens: Optional design tokens
            
        Returns:
            List of proposed prop requirements
        """
        logger.info(
            f"Proposing props for {classification.component_type.value}",
            extra={
                "extra": {
                    "component_type": classification.component_type.value,
                    "has_tokens": tokens is not None,
                }
            }
        )
        
        try:
            # Prepare image
            image_data = prepare_image_for_vision_api(image)
            
            # Build props analysis prompt (will be moved to prompts module in next commit)
            prompt = self._build_props_prompt(classification, tokens)
            
            # Call GPT-4V for props analysis
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
            proposals = self._parse_props_result(result)
            
            # Log proposals
            for proposal in proposals:
                self.log_proposal(proposal)
            
            logger.info(
                f"Proposed {len(proposals)} props requirements",
                extra={"extra": {"count": len(proposals)}}
            )
            
            return proposals
            
        except Exception as e:
            logger.error(f"Props proposal failed: {e}")
            return []
    
    def _build_props_prompt(
        self,
        classification: ComponentClassification,
        tokens: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build props analysis prompt.
        
        This is a minimal prompt. Full prompt will be added in next commit.
        
        Args:
            classification: Component classification
            tokens: Optional design tokens
            
        Returns:
            Prompt text
        """
        component_type = classification.component_type.value
        
        prompt = f"""Analyze this {component_type} component and propose prop requirements.

Component Type: {component_type}

Analyze for these prop types:

1. **Variant Props**: Different visual styles
   - Examples: variant="primary|secondary|ghost|outline"
   - Look for: Different background colors, border styles, text colors

2. **Size Props**: Different size options
   - Examples: size="sm|md|lg|xl"
   - Look for: Different dimensions, padding, font sizes

3. **Boolean Props**: On/off features
   - Examples: disabled, loading, fullWidth, icon, rounded
   - Look for: Visual states, width variations, shape variations

"""
        
        if tokens:
            prompt += f"\nDesign Tokens Available:\n{json.dumps(tokens, indent=2)}\n"
        
        prompt += """
Return JSON with this structure:
{
  "props": [
    {
      "name": "variant",
      "type": "enum",
      "values": ["primary", "secondary"],
      "visual_cues": ["solid blue background", "outlined border"],
      "confidence": 0.95
    },
    {
      "name": "disabled",
      "type": "boolean",
      "visual_cues": ["opacity-50 state visible"],
      "confidence": 0.80
    }
  ]
}

Focus on props that have clear visual evidence.
"""
        
        return prompt
    
    def _parse_props_result(self, result: Dict[str, Any]) -> List[RequirementProposal]:
        """Parse props analysis result into proposals.
        
        Args:
            result: Raw JSON result from GPT-4V
            
        Returns:
            List of RequirementProposal objects
        """
        proposals = []
        props_list = result.get("props", [])
        
        for prop_data in props_list:
            try:
                name = prop_data.get("name", "unknown")
                prop_type = prop_data.get("type", "string")
                values = prop_data.get("values")
                visual_cues = prop_data.get("visual_cues", [])
                base_confidence = float(prop_data.get("confidence", 0.5))
                
                # Calculate adjusted confidence
                confidence = self.calculate_confidence(
                    base_confidence,
                    len(visual_cues),
                    min_cues=1,
                    max_cues=4
                )
                
                # Generate rationale
                rationale = self.generate_rationale(
                    name,
                    visual_cues,
                    source="visual analysis"
                )
                
                # Create proposal
                proposal = self.create_proposal(
                    name=name,
                    confidence=confidence,
                    rationale=rationale,
                    values=values if prop_type == "enum" else None,
                )
                
                proposals.append(proposal)
                
            except Exception as e:
                logger.warning(f"Failed to parse prop: {e}")
                continue
        
        return proposals
