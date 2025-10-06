"""Retrieval API endpoints for pattern search.

Implements the retrieval search API (B7) for Epic 3.
POST /api/v1/retrieval/search endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from langsmith import traceable
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/retrieval", tags=["retrieval"])


# Request/Response Models
class RetrievalRequest(BaseModel):
    """Request model for pattern retrieval."""
    requirements: Dict = Field(
        ...,
        description="Component requirements from Epic 2",
        example={
            "component_type": "Button",
            "props": ["variant", "size", "disabled"],
            "variants": ["primary", "secondary", "ghost"],
            "a11y": ["aria-label", "keyboard navigation"]
        }
    )


class MatchHighlights(BaseModel):
    """Highlights of matched features."""
    matched_props: List[str] = Field(default_factory=list)
    matched_variants: List[str] = Field(default_factory=list)
    matched_a11y: List[str] = Field(default_factory=list)


class RankingDetails(BaseModel):
    """Ranking details for explainability."""
    bm25_score: float
    bm25_rank: int
    semantic_score: float
    semantic_rank: Optional[int]
    final_score: float
    final_rank: int


class PatternResult(BaseModel):
    """Individual pattern result with metadata."""
    id: str
    name: str
    category: str
    description: str
    framework: str
    library: str
    code: str
    metadata: Dict
    confidence: float = Field(..., ge=0, le=1)
    explanation: str
    match_highlights: MatchHighlights
    ranking_details: RankingDetails


class RetrievalMetadata(BaseModel):
    """Metadata about the retrieval process."""
    latency_ms: int
    methods_used: List[str]
    weights: Dict[str, float]
    total_patterns_searched: int
    query: str


class RetrievalResponse(BaseModel):
    """Response model for pattern retrieval."""
    patterns: List[PatternResult]
    retrieval_metadata: RetrievalMetadata


# Dependency injection placeholder
# In production, this would be initialized with actual Qdrant/OpenAI clients
_retrieval_service = None


def get_retrieval_service():
    """Dependency to get retrieval service instance.
    
    This is a placeholder. In production, this would be initialized
    in the FastAPI app startup with actual dependencies.
    """
    if _retrieval_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Retrieval service not initialized"
        )
    return _retrieval_service


def set_retrieval_service(service):
    """Set the retrieval service instance (for initialization)."""
    global _retrieval_service
    _retrieval_service = service


@router.post("/search", response_model=RetrievalResponse)
@traceable(name="retrieval_search_endpoint")
async def search_patterns(
    request: RetrievalRequest,
    retrieval_service=Depends(get_retrieval_service)
) -> RetrievalResponse:
    """Search for matching patterns based on requirements.
    
    This endpoint orchestrates the full retrieval pipeline:
    1. Query construction (BM25 + semantic)
    2. BM25 lexical search
    3. Semantic vector search
    4. Weighted fusion (0.3 BM25 + 0.7 semantic)
    5. Explainability and confidence scoring
    
    Args:
        request: RetrievalRequest with component requirements
        retrieval_service: Injected retrieval service
    
    Returns:
        RetrievalResponse with top-3 patterns and metadata
    
    Raises:
        HTTPException 400: Invalid request (missing required fields)
        HTTPException 422: Validation error
        HTTPException 500: Internal server error
    
    Example:
        ```
        POST /api/v1/retrieval/search
        {
            "requirements": {
                "component_type": "Button",
                "props": ["variant", "size"],
                "variants": ["primary", "secondary"]
            }
        }
        ```
    """
    try:
        logger.info(f"Received retrieval request: {request.requirements}")
        
        # Validate requirements has component_type
        if "component_type" not in request.requirements:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="requirements.component_type is required"
            )
        
        # Execute retrieval
        result = await retrieval_service.search(
            requirements=request.requirements,
            top_k=3
        )
        
        logger.info(
            f"Retrieval successful: {len(result['patterns'])} patterns, "
            f"{result['retrieval_metadata']['latency_ms']}ms"
        )
        
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Retrieval search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retrieval search failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for retrieval service.
    
    Returns:
        Status dict indicating service health
    """
    try:
        service = get_retrieval_service()
        return {
            "status": "healthy",
            "total_patterns": len(service.patterns) if service else 0
        }
    except Exception:
        return {
            "status": "unavailable",
            "total_patterns": 0
        }
