"""API routes for requirement proposal."""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import io
import time
import json
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from ....services.image_processor import (
    validate_and_process_image,
    ImageValidationError
)
from ....services.requirement_exporter import RequirementExporter
from ....agents.requirement_orchestrator import RequirementOrchestrator
from ....types.requirement_types import (
    RequirementProposal,
    ComponentType,
    RequirementCategory
)
from ....core.logging import get_logger
from ....core.database import get_async_session

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
    component_type: ComponentType = Field(..., alias="componentType")
    component_confidence: float = Field(..., alias="componentConfidence")
    proposals: Dict[str, List[RequirementProposal]] = Field(
        description="Proposals grouped by category (props, events, states, accessibility)"
    )
    metadata: Dict[str, Any] = Field(
        description="Metadata including latency, timestamp, source"
    )

    class Config:
        populate_by_name = True
        by_alias = True


@router.post("/propose")
async def propose_requirements(
    file: UploadFile = File(..., description="Screenshot or Figma image (PNG, JPG, JPEG up to 10MB)"),
    tokens: Optional[str] = Form(None, description="Optional design tokens as JSON string"),
    figma_data: Optional[str] = Form(None, description="Optional Figma frame data as JSON string")
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
        tokens: Optional JSON string of design tokens from Epic 1
        figma_data: Optional JSON string of Figma frame metadata
        
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
            image, metadata = validate_and_process_image(
                contents,
                mime_type=file.content_type
            )
        except ImageValidationError as e:
            logger.error(f"Image validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Parse optional JSON fields from form data
        tokens_dict = None
        figma_data_dict = None
        
        if tokens:
            try:
                tokens_dict = json.loads(tokens)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid tokens JSON: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid tokens JSON: {str(e)}"
                )
        
        if figma_data:
            try:
                figma_data_dict = json.loads(figma_data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid figma_data JSON: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid figma_data JSON: {str(e)}"
                )
        
        logger.info(
            "Starting requirement proposal",
            extra={"extra": {
                "has_tokens": tokens_dict is not None,
                "has_figma": figma_data_dict is not None
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
            tokens=tokens_dict,
            figma_data=figma_data_dict
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
                "a11y_count": len(state.accessibility_proposals),
                "latency_seconds": round(latency, 2)
            }}
        )

        # Group proposals by category
        proposals_by_category = {
            "props": state.props_proposals,
            "events": state.events_proposals,
            "states": state.states_proposals,
            "accessibility": state.accessibility_proposals
        }

        # Build response
        response = RequirementProposalResponse(
            component_type=state.classification.component_type,
            component_confidence=state.classification.confidence,
            proposals=proposals_by_category,
            metadata={
                "latency_seconds": round(latency, 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": "screenshot" if not figma_data_dict else "figma",
                "total_proposals": (
                    len(state.props_proposals) +
                    len(state.events_proposals) +
                    len(state.states_proposals) +
                    len(state.accessibility_proposals)
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


class ExportRequirementsRequest(BaseModel):
    """Request model for exporting requirements."""
    component_type: ComponentType
    component_confidence: float
    proposals: Dict[str, List[RequirementProposal]] = Field(
        description="All proposals grouped by category"
    )
    source_type: str = Field(
        default="screenshot",
        description="Source type: figma, screenshot, or design_file"
    )
    source_metadata: Optional[Dict[str, Any]] = None
    tokens: Optional[Dict[str, Any]] = None
    proposal_latency_ms: Optional[int] = None
    approval_duration_ms: Optional[int] = None
    proposed_at: Optional[str] = None
    approved_at: Optional[str] = None


class ExportRequirementsResponse(BaseModel):
    """Response model for requirement export."""
    export_id: str
    export_data: Dict[str, Any]
    summary: Dict[str, Any]
    status: str


class ExportPreviewResponse(BaseModel):
    """Response model for export preview."""
    component_type: str
    component_confidence: float
    statistics: Dict[str, Any]
    preview: Dict[str, List[Dict[str, Any]]]


@router.post("/export")
async def export_requirements(
    request: ExportRequirementsRequest,
    db: AsyncSession = Depends(get_async_session)
) -> ExportRequirementsResponse:
    """Export approved requirements to JSON and store in database.

    This endpoint:
    - Exports only approved requirements
    - Stores in PostgreSQL for audit trail
    - Generates export JSON for Epic 3/4 integration
    - Tracks approval workflow metrics
    - Returns export ID for future reference

    Args:
        request: Export request with approved requirements
        db: Database session (injected)

    Returns:
        Export result with ID, JSON data, and summary

    Raises:
        HTTPException: For validation or database failures
    """
    try:
        logger.info(
            f"Starting requirement export for {request.component_type.value}",
            extra={
                "extra": {
                    "component_type": request.component_type.value,
                    "total_proposals": sum(len(reqs) for reqs in request.proposals.values()),
                }
            },
        )

        # Convert proposals dict to proper format
        proposals_dict = {}
        for category, proposals_list in request.proposals.items():
            proposals_dict[category] = proposals_list

        # Parse timestamps if provided
        proposed_at = None
        if request.proposed_at:
            try:
                proposed_at = datetime.fromisoformat(request.proposed_at.replace('Z', '+00:00'))
            except Exception as e:
                logger.warning(f"Failed to parse proposed_at: {e}")

        approved_at = None
        if request.approved_at:
            try:
                approved_at = datetime.fromisoformat(request.approved_at.replace('Z', '+00:00'))
            except Exception as e:
                logger.warning(f"Failed to parse approved_at: {e}")

        # Initialize exporter
        exporter = RequirementExporter(db_session=db)

        # Export requirements
        result = await exporter.export_requirements(
            component_type=request.component_type,
            component_confidence=request.component_confidence,
            proposals_by_category=proposals_dict,
            source_type=request.source_type,
            source_metadata=request.source_metadata,
            tokens=request.tokens,
            proposal_latency_ms=request.proposal_latency_ms,
            approval_duration_ms=request.approval_duration_ms,
            proposed_at=proposed_at,
            approved_at=approved_at,
        )

        logger.info(
            f"Requirements exported successfully: {result['export_id']}",
            extra={
                "extra": {
                    "export_id": result["export_id"],
                    "approved_count": result["database_record"]["approved_count"],
                }
            },
        )

        return ExportRequirementsResponse(
            export_id=result["export_id"],
            export_data=result["export_data"],
            summary=result["database_record"],
            status=result["status"],
        )

    except Exception as e:
        logger.error(
            f"Requirement export failed: {e}",
            extra={"extra": {"error_type": type(e).__name__}},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Requirement export failed: {str(e)}"
        )


@router.post("/export/preview")
async def preview_export(
    component_type: ComponentType,
    component_confidence: float,
    proposals: Dict[str, List[RequirementProposal]],
    db: AsyncSession = Depends(get_async_session)
) -> ExportPreviewResponse:
    """Generate a preview of what will be exported.

    This allows users to review export statistics and approved
    requirements before committing to the export.

    Args:
        component_type: Detected component type
        component_confidence: Classification confidence
        proposals: All proposals grouped by category
        db: Database session (injected)

    Returns:
        Export preview with statistics and approved requirements
    """
    try:
        exporter = RequirementExporter(db_session=db)

        preview = await exporter.get_export_preview(
            proposals_by_category=proposals,
            component_type=component_type,
            component_confidence=component_confidence,
        )

        return ExportPreviewResponse(**preview)

    except Exception as e:
        logger.error(f"Export preview generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export preview failed: {str(e)}"
        )


@router.get("/exports/{export_id}")
async def get_export(
    export_id: str,
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    """Retrieve an exported requirement set by ID.

    Args:
        export_id: Unique export identifier
        db: Database session (injected)

    Returns:
        Export data with requirements and metadata

    Raises:
        HTTPException: If export not found
    """
    try:
        exporter = RequirementExporter(db_session=db)
        export_data = await exporter.get_export_by_id(export_id)

        if not export_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Export not found: {export_id}"
            )

        return export_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve export: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve export: {str(e)}"
        )


@router.get("/exports")
async def list_recent_exports(
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
) -> List[Dict[str, Any]]:
    """List recent requirement exports.

    Args:
        limit: Maximum number of exports to return (default: 10)
        db: Database session (injected)

    Returns:
        List of recent exports with summaries
    """
    try:
        exporter = RequirementExporter(db_session=db)
        exports = await exporter.get_recent_exports(limit=limit)
        return exports

    except Exception as e:
        logger.error(f"Failed to list exports: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list exports: {str(e)}"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for requirements service."""
    return {
        "status": "healthy",
        "service": "requirements",
        "version": "1.0.0"
    }
