"""
Evaluation API routes for E2E pipeline metrics.

Endpoints:
- GET /api/v1/evaluation/metrics - Run full evaluation and return metrics
- GET /api/v1/evaluation/status - Check evaluation system readiness
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import os

from ....evaluation.e2e_evaluator import E2EEvaluator
from ....evaluation.golden_dataset import GoldenDataset
from ....evaluation.retrieval_queries import TEST_QUERIES, get_query_statistics
from ....evaluation.metrics import RetrievalMetrics
from ....services.retrieval_service import RetrievalService
from ....core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.get("/metrics")
async def get_evaluation_metrics() -> Dict[str, Any]:
    """
    Run E2E evaluation and return comprehensive metrics.

    This endpoint runs the full golden dataset evaluation pipeline:
    - Token extraction accuracy
    - Pattern retrieval accuracy (E2E + retrieval-only)
    - Code generation quality
    - End-to-end pipeline success rate

    The evaluation includes:
    1. E2E evaluation on golden dataset screenshots
    2. Retrieval-only evaluation on 22 test queries
    3. Per-category breakdown (keyword, semantic, mixed)

    Returns:
        JSON with overall metrics and per-screenshot results

    Raises:
        HTTPException: If evaluation fails or API key not configured
    """
    logger.info("Received request for evaluation metrics")

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not configured")
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Set the environment variable to run evaluation."
        )

    try:
        # ===== E2E Evaluation =====
        logger.info("Running E2E evaluation...")
        evaluator = E2EEvaluator(api_key=api_key)
        e2e_results = await evaluator.evaluate_all()

        logger.info(
            f"E2E evaluation complete. "
            f"Success rate: {e2e_results['overall']['pipeline_success_rate']:.1%}"
        )

        # ===== Retrieval-Only Evaluation =====
        logger.info("Running retrieval-only evaluation...")
        retrieval_service = RetrievalService()
        retrieval_results = []

        for query_data in TEST_QUERIES:
            query = query_data['query']
            expected = query_data['expected_pattern']
            category = query_data['category']

            # Run retrieval
            results = await retrieval_service.search(
                requirements={'description': query},
                top_k=5
            )

            # Get top result
            if results and len(results) > 0:
                retrieved = results[0].get('pattern_id', '')
                confidence = results[0].get('score', 0.0)
            else:
                retrieved = ''
                confidence = 0.0

            correct = retrieved == expected

            # Find rank of correct pattern
            rank = 999
            for i, result in enumerate(results):
                if result.get('pattern_id') == expected:
                    rank = i + 1
                    break

            retrieval_results.append({
                'query': query,
                'expected': expected,
                'retrieved': retrieved,
                'correct': correct,
                'rank': rank,
                'confidence': confidence,
                'category': category,
            })

        # Calculate retrieval metrics
        from ....evaluation.types import RetrievalResult

        retrieval_result_objects = [
            RetrievalResult(
                screenshot_id=r['query'][:20],  # Truncate for ID
                expected_pattern_id=r['expected'],
                retrieved_pattern_id=r['retrieved'],
                correct=r['correct'],
                rank=r['rank'],
                confidence=r['confidence']
            )
            for r in retrieval_results
        ]

        # Overall retrieval metrics
        overall_mrr = RetrievalMetrics.mean_reciprocal_rank(retrieval_result_objects)
        overall_hit_at_3 = RetrievalMetrics.hit_at_k(retrieval_result_objects, k=3)
        overall_precision_at_1 = RetrievalMetrics.precision_at_k(retrieval_result_objects, k=1)

        # Per-category metrics
        def calculate_category_metrics(category: str) -> Dict[str, float]:
            """Calculate metrics for a specific category."""
            category_results = [
                RetrievalResult(
                    screenshot_id=r['query'][:20],
                    expected_pattern_id=r['expected'],
                    retrieved_pattern_id=r['retrieved'],
                    correct=r['correct'],
                    rank=r['rank'],
                    confidence=r['confidence']
                )
                for r in retrieval_results
                if r['category'] == category
            ]

            if not category_results:
                return {'mrr': 0.0, 'hit_at_3': 0.0, 'precision_at_1': 0.0}

            return {
                'mrr': RetrievalMetrics.mean_reciprocal_rank(category_results),
                'hit_at_3': RetrievalMetrics.hit_at_k(category_results, k=3),
                'precision_at_1': RetrievalMetrics.precision_at_k(category_results, k=1),
            }

        retrieval_only_metrics = {
            'mrr': overall_mrr,
            'hit_at_3': overall_hit_at_3,
            'precision_at_1': overall_precision_at_1,
            'test_queries': len(TEST_QUERIES),
            'per_category': {
                'keyword': calculate_category_metrics('keyword'),
                'semantic': calculate_category_metrics('semantic'),
                'mixed': calculate_category_metrics('mixed'),
            },
            'query_results': retrieval_results,
        }

        logger.info(
            f"Retrieval-only evaluation complete. "
            f"MRR: {overall_mrr:.3f}, Hit@3: {overall_hit_at_3:.1%}"
        )

        # Combine E2E and retrieval-only results
        combined_results = {
            **e2e_results,
            'retrieval_only': retrieval_only_metrics,
        }

        return combined_results

    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/status")
async def get_evaluation_status() -> Dict[str, Any]:
    """
    Check if evaluation system is ready.

    Returns status information about:
    - API key configuration
    - Golden dataset availability
    - Retrieval query statistics

    Returns:
        Status information and readiness check
    """
    api_key_set = bool(os.getenv("OPENAI_API_KEY"))

    # Check golden dataset
    try:
        dataset = GoldenDataset()
        dataset_size = len(dataset)
        dataset_stats = dataset.get_statistics()
        dataset_loaded = True
    except Exception as e:
        logger.error(f"Failed to load golden dataset: {e}")
        dataset_size = 0
        dataset_stats = {}
        dataset_loaded = False

    # Get retrieval query statistics
    query_stats = get_query_statistics()

    return {
        "ready": api_key_set and dataset_loaded,
        "api_key_configured": api_key_set,
        "golden_dataset": {
            "loaded": dataset_loaded,
            "size": dataset_size,
            "statistics": dataset_stats,
        },
        "retrieval_queries": query_stats,
        "message": (
            "Evaluation system ready" if api_key_set and dataset_loaded
            else "Evaluation system not ready. Check API key and golden dataset."
        )
    }
