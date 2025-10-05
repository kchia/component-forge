"""Component type inference agent using GPT-4V vision capabilities.

This agent analyzes screenshots and Figma frames to detect component types
(Button, Card, Input, etc.) with confidence scoring.
"""

import json
import os
from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI
from PIL import Image

from ..types.requirement_types import (
    ComponentType,
    ComponentClassification,
    get_confidence_level,
)
from ..services.image_processor import prepare_image_for_vision_api
from ..prompts.component_classifier import create_classification_prompt
from ..core.logging import get_logger

logger = get_logger(__name__)


class ComponentClassifierError(Exception):
    """Exception raised for component classification errors."""
    pass


class ComponentClassifier:
    """Classify component type from screenshots using GPT-4V.
    
    This agent uses vision-language models to detect component types
    based on visual cues, layout patterns, and interactive elements.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the component classifier.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.max_retries = 3
        self.model = "gpt-4o"  # GPT-4V model
    
    async def classify_component(
        self,
        image: Image.Image,
        figma_data: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> ComponentClassification:
        """Classify component type from an image.
        
        Args:
            image: PIL Image object
            figma_data: Optional Figma layer/component metadata
            retry_count: Current retry attempt (for internal use)
            
        Returns:
            ComponentClassification with type, confidence, and candidates
            
        Raises:
            ComponentClassifierError: If classification fails after retries
        """
        try:
            # Prepare image for vision API
            image_data = prepare_image_for_vision_api(image)
            
            # Build prompt
            prompt = self._build_classification_prompt(figma_data)
            
            # Call GPT-4V with structured output
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
                max_tokens=1000,
                temperature=0.1,  # Low temperature for consistent classification
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Validate and convert to ComponentClassification
            classification = self._parse_classification_result(result)
            
            logger.info(
                f"Component classified as {classification.component_type} "
                f"(confidence: {classification.confidence:.2f})"
            )
            
            return classification
            
        except Exception as e:
            if retry_count < self.max_retries:
                logger.warning(
                    f"Classification failed (attempt {retry_count + 1}), retrying: {e}"
                )
                return await self.classify_component(
                    image, figma_data, retry_count + 1
                )
            else:
                logger.error(f"Component classification failed after {self.max_retries} retries: {e}")
                raise ComponentClassifierError(
                    f"Failed to classify component: {e}"
                ) from e
    
    def _build_classification_prompt(
        self, figma_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build classification prompt with few-shot examples.
        
        Args:
            figma_data: Optional Figma metadata
            
        Returns:
            Classification prompt text with examples
        """
        return create_classification_prompt(figma_data)
    
    def _parse_classification_result(
        self, result: Dict[str, Any]
    ) -> ComponentClassification:
        """Parse and validate classification result.
        
        Args:
            result: Raw JSON result from GPT-4V
            
        Returns:
            Validated ComponentClassification object
            
        Raises:
            ValueError: If result format is invalid
        """
        try:
            # Extract and validate component type
            component_type_str = result.get("component_type")
            if not component_type_str:
                raise ValueError("Missing component_type in result")
            
            # Map string to enum
            component_type = ComponentType(component_type_str)
            
            # Extract confidence
            confidence = float(result.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]
            
            # Extract candidates
            candidates_raw = result.get("candidates", [])
            candidates = []
            for cand in candidates_raw:
                try:
                    candidates.append({
                        "type": ComponentType(cand["type"]),
                        "confidence": float(cand.get("confidence", 0.0))
                    })
                except (KeyError, ValueError):
                    # Skip invalid candidates
                    pass
            
            # Extract rationale
            rationale = result.get("rationale", "No rationale provided")
            
            return ComponentClassification(
                component_type=component_type,
                confidence=confidence,
                candidates=candidates,
                rationale=rationale
            )
            
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid classification result format: {e}") from e
