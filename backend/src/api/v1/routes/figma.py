"""Figma integration API routes."""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

from ....services.figma_client import (
    FigmaClient,
    FigmaClientError,
    FigmaAuthenticationError,
    FigmaFileNotFoundError,
    FigmaRateLimitError,
)
from ....core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/tokens", tags=["figma"])


# Request/Response Models


class FigmaAuthRequest(BaseModel):
    """Request model for Figma PAT authentication."""

    personal_access_token: str = Field(
        ..., 
        description="Figma Personal Access Token",
        min_length=10,
    )

    @field_validator("personal_access_token")
    @classmethod
    def validate_pat_format(cls, v):
        """Validate PAT format (basic check)."""
        if not v or not v.strip():
            raise ValueError("Personal access token cannot be empty")
        # Figma PATs typically start with 'figd_' but this isn't always the case
        return v.strip()


class FigmaAuthResponse(BaseModel):
    """Response model for Figma PAT authentication."""

    valid: bool = Field(..., description="Whether the token is valid")
    user_email: Optional[str] = Field(None, description="User email if token is valid")
    message: str = Field(..., description="Status message")


class FigmaExtractRequest(BaseModel):
    """Request model for Figma file extraction."""

    figma_url: str = Field(..., description="Figma file URL")
    personal_access_token: Optional[str] = Field(
        None,
        description="Figma PAT (if not provided, uses environment variable)",
    )

    @field_validator("figma_url")
    @classmethod
    def validate_figma_url(cls, v):
        """Validate Figma URL format."""
        if not v or not ("figma.com/file/" in v or "figma.com/design/" in v):
            raise ValueError(
                "Invalid Figma URL. Must be in format: https://figma.com/file/{key} or https://figma.com/design/{key}"
            )
        return v


class DesignTokens(BaseModel):
    """Normalized design tokens."""

    colors: Dict[str, str] = Field(default_factory=dict, description="Color tokens")
    typography: Dict[str, Any] = Field(default_factory=dict, description="Typography tokens")
    spacing: Dict[str, Any] = Field(default_factory=dict, description="Spacing tokens")


class FigmaExtractResponse(BaseModel):
    """Response model for Figma file extraction."""

    file_key: str = Field(..., description="Figma file key")
    file_name: str = Field(..., description="Figma file name")
    tokens: DesignTokens = Field(..., description="Extracted design tokens")
    cached: bool = Field(..., description="Whether response was from cache")


class CacheMetricsResponse(BaseModel):
    """Response model for cache metrics."""

    file_key: str
    hits: int
    misses: int
    total_requests: int
    hit_rate: float
    avg_latency_ms: float


# API Endpoints


@router.post("/figma/auth", response_model=FigmaAuthResponse)
async def authenticate_figma(request: FigmaAuthRequest):
    """
    Validate Figma Personal Access Token.

    This endpoint validates the provided PAT by calling Figma's /v1/me endpoint.
    The token is not stored server-side for security reasons.
    """
    try:
        async with FigmaClient(personal_access_token=request.personal_access_token) as client:
            user_data = await client.validate_token()

        return FigmaAuthResponse(
            valid=True,
            user_email=user_data.get("email"),
            message="Authentication successful",
        )

    except FigmaAuthenticationError as e:
        logger.warning(f"Figma authentication failed: {e}")
        return FigmaAuthResponse(
            valid=False, message="Invalid Personal Access Token"
        )

    except FigmaClientError as e:
        logger.error(f"Figma client error during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating token: {str(e)}",
        )


@router.post("/extract/figma", response_model=FigmaExtractResponse)
async def extract_figma_tokens(request: FigmaExtractRequest):
    """
    Extract design tokens from a Figma file.

    This endpoint fetches the Figma file and extracts:
    - Color styles (as hex values)
    - Text styles (font family, size, weight)
    - Auto-layout spacing (as spacing tokens)

    Results are cached for 5 minutes to reduce API calls.
    """
    try:
        # Extract file key from URL
        file_key = FigmaClient.extract_file_key(request.figma_url)
        logger.info(f"Extracting tokens from Figma file: {file_key}")

        # Initialize client with provided or environment PAT
        async with FigmaClient(personal_access_token=request.personal_access_token) as client:
            # Fetch file data (with caching)
            file_data = await client.get_file(file_key, use_cache=True)
            
            # Check if response was cached
            cached = file_data.get("_cached", False)
            
            # Extract file metadata
            file_name = file_data.get("name", "Unknown")
            
            # Fetch styles data (with caching)
            styles_data = await client.get_file_styles(file_key, use_cache=True)

            # Extract tokens from file and styles
            tokens = _extract_tokens(file_data, styles_data)

        return FigmaExtractResponse(
            file_key=file_key,
            file_name=file_name,
            tokens=tokens,
            cached=cached,
        )

    except ValueError as e:
        logger.warning(f"Invalid Figma URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    except FigmaAuthenticationError as e:
        logger.warning(f"Figma authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Figma Personal Access Token",
        )

    except FigmaFileNotFoundError as e:
        logger.warning(f"Figma file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    except FigmaRateLimitError as e:
        logger.warning(f"Figma rate limit exceeded: {e}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Figma API rate limit exceeded. Please try again later.",
        )

    except FigmaClientError as e:
        logger.error(f"Figma client error during extraction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting tokens: {str(e)}",
        )


@router.delete("/figma/cache/{file_key}")
async def invalidate_figma_cache(file_key: str):
    """
    Invalidate cache for a specific Figma file.

    This forces the next request to fetch fresh data from Figma API.
    """
    try:
        async with FigmaClient() as client:
            deleted = await client.invalidate_cache(file_key)

        return {
            "file_key": file_key,
            "cache_entries_deleted": deleted,
            "message": "Cache invalidated successfully" if deleted > 0 else "No cache entries found",
        }

    except Exception as e:
        logger.error(f"Error invalidating cache for {file_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error invalidating cache: {str(e)}",
        )


@router.get("/figma/cache/{file_key}/metrics", response_model=CacheMetricsResponse)
async def get_figma_cache_metrics(file_key: str):
    """
    Get cache metrics for a specific Figma file.

    Returns hit rate, latency, and other performance metrics.
    """
    try:
        async with FigmaClient() as client:
            metrics = await client.get_cache_metrics(file_key)

        return CacheMetricsResponse(**metrics)

    except Exception as e:
        logger.error(f"Error getting cache metrics for {file_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting cache metrics: {str(e)}",
        )


# Helper Functions


def _extract_tokens(file_data: Dict[str, Any], styles_data: Dict[str, Any]) -> DesignTokens:
    """
    Extract and normalize design tokens from Figma file and styles data.

    Args:
        file_data: Figma file data
        styles_data: Figma styles data

    Returns:
        Normalized design tokens
    """
    tokens = DesignTokens()

    # Extract color styles
    tokens.colors = _extract_color_tokens(styles_data)

    # Extract typography styles
    tokens.typography = _extract_typography_tokens(styles_data)

    # Extract spacing from auto-layout
    tokens.spacing = _extract_spacing_tokens(file_data)

    return tokens


def _extract_color_tokens(styles_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract color tokens from Figma styles.

    Args:
        styles_data: Figma styles data

    Returns:
        Dictionary of color name to hex value
    """
    colors = {}
    
    # Figma styles API returns styles with metadata
    # For now, return a placeholder structure
    # This would be expanded based on actual Figma API response structure
    meta = styles_data.get("meta", {})
    styles = meta.get("styles", [])
    
    for style in styles:
        if style.get("style_type") == "FILL":
            # Extract color name and value
            # This is a simplified version - actual implementation would parse the fill
            name = style.get("name", "").lower().replace(" ", "-")
            # Color extraction would require fetching style details
            # For now, we'll note this needs the full file parse
            pass
    
    return colors


def _extract_typography_tokens(styles_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract typography tokens from Figma styles.

    Args:
        styles_data: Figma styles data

    Returns:
        Dictionary of typography tokens
    """
    typography = {}
    
    meta = styles_data.get("meta", {})
    styles = meta.get("styles", [])
    
    for style in styles:
        if style.get("style_type") == "TEXT":
            name = style.get("name", "").lower().replace(" ", "-")
            # Typography details would be in the node data
            # This requires parsing the full file structure
            pass
    
    return typography


def _extract_spacing_tokens(file_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract spacing tokens from auto-layout in Figma file.

    Args:
        file_data: Figma file data

    Returns:
        Dictionary of spacing tokens
    """
    spacing = {}
    
    # Spacing extraction would require traversing the document tree
    # and finding auto-layout nodes with spacing values
    # This is a placeholder for the actual implementation
    
    return spacing
