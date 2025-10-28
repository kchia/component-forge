"""
Evaluation module for E2E pipeline assessment.

This module provides tools for evaluating the complete screenshot-to-code pipeline:
- Golden dataset management
- Metrics calculation at each stage
- E2E pipeline evaluation
- Performance analysis and reporting
"""

from .types import (
    TokenExtractionResult,
    RetrievalResult,
    GenerationResult,
    E2EResult,
)

from .metrics import (
    TokenExtractionMetrics,
    RetrievalMetrics,
    GenerationMetrics,
    E2EMetrics,
)

from .golden_dataset import GoldenDataset

__all__ = [
    # Types
    'TokenExtractionResult',
    'RetrievalResult',
    'GenerationResult',
    'E2EResult',
    # Metrics
    'TokenExtractionMetrics',
    'RetrievalMetrics',
    'GenerationMetrics',
    'E2EMetrics',
    # Dataset
    'GoldenDataset',
]
