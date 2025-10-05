"""API routes for requirement proposal."""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import io
import time
from PIL import Image

from ....services.image_processor import (
    validate_and_process_image,
    ImageValidationError
)
from ....agents.requirement_orchestrator import RequirementOrchestrator
from ....types.requirement_types import (
    RequirementProposal,
    ComponentType,
    RequirementCategory
)
from ....core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/requirements", tags=["requirements"])


class RequirementProposalRequest(BaseModel):
    """Request model for requirement proposal."""
    tokens: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional design tokens from Epic 1 extraction"
    )
    figma_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional Figma frame data"
    )


class RequirementProposalResponse(BaseModel):
    """Response model for requirement proposal."""
    component_type: ComponentType
    component_confidence: float
    proposals: Dict[str, List[RequirementProposal]] = Field(
        description="Proposals grouped by category (props, events, states, accessibility)"
    )
    metadata: Dict[str, Any] = Field(
        description="Metadata including latency, timestamp, source"
    )


@router.post("/propose")
async def propose_requirements(
    file: UploadFile = File(...),
    request: Optional[RequirementProposalRequest] = None
) -> RequirementProposalResponse:
    """Propose functional requirements from screenshot/Figma frame.
    
    Analyzes uploaded image to propose:
    - Props (variant, size, disabled, etc.)
    - Events (onClick, onChange, onHover, etc.)
    - States (hover, focus, disabled, loading, etc.)
    - Accessibility (aria-label, semantic HTML, keyboard nav, etc.)
    
    Each proposal includes confidence score and rationale.
    Target latency: p50 ≤15s
    
    Args:
        file: Uploaded image file (PNG, JPG, JPEG up to 10MB)
        request: Optional tokens and Figma data for enhanced accuracy
        
    Returns:
        JSON response with component type, proposals by category, metadata
        
    Raises:
        HTTPException: For validation or AI failures
    """
    start_time = time.time()
    
    # Sanitize filename
    import os
    safe_filename = os.path.basename(file.filename) if file.filename else "unknown"
    
    logger.info(
        f"Received requirement proposal request: {safe_filename}",
        extra={"extra": {"content_type": file.content_type}}
    )
    
    try:
        # Read and validate image
        contents = await file.read()
        
        try:
            image = validate_and_process_image(
                contents,
                max_size_mb=10,
                allowed_formats=["PNG", "JPEG", "JPG"]
            )
        except ImageValidationError as e:
            logger.error(f"Image validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Extract request data
        tokens = request.tokens if request else None
        figma_data = request.figma_data if request else None
        
        logger.info(
            "Starting requirement proposal",
            extra={"extra": {
                "has_tokens": tokens is not None,
                "has_figma": figma_data is not None
            }}
        )
        
        # Initialize orchestrator
        import os as env_os
        openai_api_key = env_os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY not configured"
            )
        
        orchestrator = RequirementOrchestrator(openai_api_key=openai_api_key)
        
        # Run requirement proposal (use parallel for production)
        state = await orchestrator.propose_requirements_parallel(
            image=image,
            tokens=tokens,
            figma_data=figma_data
        )
        
        # Calculate latency
        latency = time.time() - start_time
        
        logger.info(
            "Requirement proposal complete",
            extra={"extra": {
                "component_type": state.classification.component_type.value,
                "props_count": len(state.props_proposals),
                "events_count": len(state.events_proposals),
                "states_count": len(state.states_proposals),
                "a11y_count": len(state.a11y_proposals),
                "latency_seconds": round(latency, 2)
            }}
        )
        
        # Group proposals by category
        proposals_by_category = {
            "props": state.props_proposals,
            "events": state.events_proposals,
            "states": state.states_proposals,
            "accessibility": state.a11y_proposals
        }
        
        # Build response
        response = RequirementProposalResponse(
            component_type=state.classification.component_type,
            component_confidence=state.classification.confidence,
            proposals=proposals_by_category,
            metadata={
                "latency_seconds": round(latency, 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": "screenshot" if not figma_data else "figma",
                "total_proposals": (
                    len(state.props_proposals) +
                    len(state.events_proposals) +
                    len(state.states_proposals) +
                    len(state.a11y_proposals)
                ),
                "target_latency_p50": 15.0,
                "meets_latency_target": latency <= 15.0
            }
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error(
            f"Requirement proposal failed: {e}",
            extra={"extra": {"error_type": type(e).__name__}},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Requirement proposal failed: {str(e)}"
        )
    
    finally:
        # Cleanup
        await file.close()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for requirements service."""
    return {
        "status": "healthy",
        "service": "requirements",
        "version": "1.0.0"
    }
