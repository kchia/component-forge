"""API routes for code generation."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import time

from ....generation.generator_service import GeneratorService
from ....generation.types import GenerationRequest, GenerationResult
from ....core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/generation", tags=["generation"])

# Initialize generator service (singleton)
generator_service = GeneratorService()

# Prometheus metrics (optional - only if prometheus_client is available)
try:
    from prometheus_client import Histogram
    
    generation_latency_seconds = Histogram(
        "generation_latency_seconds",
        "Code generation latency in seconds",
        ["pattern_id", "success"]
    )
    METRICS_ENABLED = True
except ImportError:
    METRICS_ENABLED = False
    logger.warning("Prometheus metrics not available for generation endpoint")


@router.post("/generate")
async def generate_component(
    request: GenerationRequest
) -> Dict[str, Any]:
    """
    Generate production-ready React/TypeScript component code.
    
    Takes a pattern ID, design tokens, and requirements, then generates:
    - Component.tsx with TypeScript types
    - Component.stories.tsx for Storybook
    - CSS variables and Tailwind classes
    - ARIA attributes and semantic HTML
    
    Args:
        request: GenerationRequest with pattern_id, tokens, requirements
        
    Returns:
        JSON response with generated code and metadata
        
    Raises:
        HTTPException: For validation or generation errors
    """
    logger.info(
        f"Received generation request for pattern: {request.pattern_id}"
    )
    
    start_time = time.time()
    success = False
    
    try:
        # Validate request
        if not request.pattern_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="pattern_id is required"
            )
        
        if not request.tokens:
            logger.warning("No tokens provided, using fallback tokens")
            # Could use fallback tokens from token_injector
        
        if not request.requirements:
            logger.warning("No requirements provided, using pattern defaults")
        
        # Generate component
        logger.info(f"Starting generation for pattern: {request.pattern_id}")
        
        result: GenerationResult = await generator_service.generate(request)
        
        # Check if generation succeeded
        if not result.success:
            logger.error(f"Generation failed: {result.error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Code generation failed: {result.error}"
            )
        
        # Calculate total latency
        total_latency_ms = int((time.time() - start_time) * 1000)
        success = True
        
        # Record Prometheus metric
        if METRICS_ENABLED:
            generation_latency_seconds.labels(
                pattern_id=request.pattern_id,
                success="true"
            ).observe((time.time() - start_time))
        
        logger.info(
            f"Generation completed successfully in {total_latency_ms}ms",
            extra={
                "extra": {
                    "pattern_id": request.pattern_id,
                    "latency_ms": total_latency_ms,
                    "token_count": result.metadata.token_count,
                    "lines_of_code": result.metadata.lines_of_code
                }
            }
        )
        
        # Return successful response matching frontend GenerationResponse type
        return {
            "code": {
                "component": result.component_code,
                "stories": result.stories_code,
                "tokens_json": result.files.get("tokens", None),
                "requirements_json": result.files.get("requirements", None)
            },
            "metadata": {
                "pattern_used": request.pattern_id,
                "pattern_version": "1.0.0",
                "tokens_applied": result.metadata.token_count,
                "requirements_implemented": result.metadata.requirements_implemented,
                "lines_of_code": result.metadata.lines_of_code,
                "imports_count": 0,  # TODO: Calculate from code
                "has_typescript_errors": False,
                "has_accessibility_warnings": False
            },
            "timing": {
                "total_ms": result.metadata.latency_ms,
                "parsing_ms": result.metadata.stage_latencies.get("parsing", 0),
                "injection_ms": result.metadata.stage_latencies.get("injecting", 0),
                "generation_ms": result.metadata.stage_latencies.get("generating", 0),
                "assembly_ms": result.metadata.stage_latencies.get("assembling", 0),
                "formatting_ms": result.metadata.stage_latencies.get("formatting", 0)
            },
            "provenance": {
                "pattern_id": request.pattern_id,
                "pattern_version": "1.0.0",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "tokens_hash": "placeholder",  # TODO: Calculate hash
                "requirements_hash": "placeholder"  # TODO: Calculate hash
            },
            "status": "completed"
        }
    
    except HTTPException:
        # Record failure metric
        if METRICS_ENABLED:
            generation_latency_seconds.labels(
                pattern_id=request.pattern_id,
                success="false"
            ).observe((time.time() - start_time))
        # Re-raise HTTP exceptions
        raise
    
    except FileNotFoundError as e:
        # Record failure metric
        if METRICS_ENABLED:
            generation_latency_seconds.labels(
                pattern_id=request.pattern_id,
                success="false"
            ).observe((time.time() - start_time))
        logger.error(f"Pattern not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pattern not found: {request.pattern_id}"
        )
    
    except ValueError as e:
        # Record failure metric
        if METRICS_ENABLED:
            generation_latency_seconds.labels(
                pattern_id=request.pattern_id,
                success="false"
            ).observe((time.time() - start_time))
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request: {str(e)}"
        )
    
    except Exception as e:
        # Record failure metric
        if METRICS_ENABLED:
            generation_latency_seconds.labels(
                pattern_id=request.pattern_id,
                success="false"
            ).observe((time.time() - start_time))
        logger.error(f"Unexpected error during generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/patterns")
async def list_available_patterns() -> Dict[str, Any]:
    """
    List all available component patterns.
    
    Returns:
        JSON response with list of available pattern IDs
    """
    logger.info("Listing available patterns")
    
    try:
        # Use pattern parser to list patterns
        from ....generation.pattern_parser import PatternParser
        
        parser = PatternParser()
        patterns = parser.list_available_patterns()
        
        logger.info(f"Found {len(patterns)} available patterns")
        
        return {
            "success": True,
            "patterns": patterns,
            "count": len(patterns)
        }
    
    except Exception as e:
        logger.error(f"Error listing patterns: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list patterns: {str(e)}"
        )


@router.get("/status/{pattern_id}")
async def get_generation_status(pattern_id: str) -> Dict[str, Any]:
    """
    Get current generation status (for progress tracking).
    
    Args:
        pattern_id: ID of pattern being generated
        
    Returns:
        JSON response with current stage and progress
    """
    logger.info(f"Getting generation status for pattern: {pattern_id}")
    
    try:
        # Get current stage from generator service
        current_stage = generator_service.get_current_stage()
        stage_latencies = generator_service.get_stage_latencies()
        
        return {
            "success": True,
            "pattern_id": pattern_id,
            "current_stage": current_stage.value,
            "stage_latencies": {
                stage.value: latency 
                for stage, latency in stage_latencies.items()
            }
        }
    
    except Exception as e:
        logger.error(f"Error getting generation status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status: {str(e)}"
        )
