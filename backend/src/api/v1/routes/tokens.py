"""API routes for design token extraction."""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import io
from PIL import Image

from ....services.image_processor import (
    validate_and_process_image,
    ImageValidationError
)
from ....agents.token_extractor import TokenExtractor, TokenExtractionError
from ....core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("/extract/screenshot")
async def extract_tokens_from_screenshot(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """Extract design tokens from an uploaded screenshot.
    
    Accepts PNG, JPG, JPEG formats up to 10MB.
    Returns extracted design tokens with confidence scores.
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON response with extracted tokens and metadata
        
    Raises:
        HTTPException: For validation or extraction errors
    """
    # Sanitize filename to prevent path traversal issues
    import os
    safe_filename = os.path.basename(file.filename) if file.filename else "unknown"
    
    logger.info(
        f"Received screenshot upload: {safe_filename}, "
        f"content_type: {file.content_type}"
    )
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Validate and process image
        try:
            image, metadata = validate_and_process_image(
                contents,
                mime_type=file.content_type
            )
            logger.info(
                f"Image validated: {metadata['width']}x{metadata['height']}, "
                f"format: {metadata['format']}"
            )
        except ImageValidationError as e:
            logger.warning(f"Image validation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Extract tokens using GPT-4V
        try:
            extractor = TokenExtractor()
            result = await extractor.extract_tokens(image)
            
            # Add metadata to response
            result["metadata"] = {
                "filename": safe_filename,
                "image": metadata,
                "extraction_method": "gpt-4v",
            }
            
            logger.info("Token extraction completed successfully")
            return result
            
        except TokenExtractionError as e:
            logger.error(f"Token extraction failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to extract tokens: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token extraction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    finally:
        # Clean up
        await file.close()


@router.get("/defaults")
async def get_default_tokens() -> Dict[str, Any]:
    """Get shadcn/ui default design tokens.
    
    Returns:
        JSON response with default tokens
    """
    from ....core.defaults import SHADCN_DEFAULTS
    
    return {
        "tokens": SHADCN_DEFAULTS,
        "source": "shadcn/ui",
        "description": "Default design tokens used as fallbacks"
    }
