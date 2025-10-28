"""
End-to-end pipeline evaluator.

This module provides the E2EEvaluator class for evaluating the complete
screenshot-to-code pipeline against the golden dataset.
"""

import time
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path

from .types import (
    TokenExtractionResult,
    RetrievalResult,
    GenerationResult as EvalGenerationResult,
    E2EResult
)
from .metrics import E2EMetrics
from .golden_dataset import GoldenDataset
from ..agents.token_extractor import TokenExtractor
from ..services.retrieval_service import RetrievalService
from ..generation.generator_service import GeneratorService
from ..generation.types import GenerationRequest
from ..core.logging import get_logger

logger = get_logger(__name__)


class E2EEvaluator:
    """
    Evaluates the full screenshot-to-code pipeline.

    Runs golden dataset screenshots through:
    1. Token extraction (GPT-4V)
    2. Pattern retrieval (Hybrid BM25+Semantic)
    3. Code generation (LLM + Validation)

    Collects metrics at each stage and calculates overall pipeline performance.
    """

    def __init__(
        self,
        golden_dataset_path: Optional[Path] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize E2E evaluator.

        Args:
            golden_dataset_path: Path to golden dataset directory
            api_key: OpenAI API key (required for token extraction and generation)
        """
        self.dataset = GoldenDataset(golden_dataset_path)
        self.token_extractor = TokenExtractor(api_key=api_key)

        # Create mock patterns for evaluation testing
        # TODO: Load real patterns from database or pattern library
        mock_patterns = self._create_mock_patterns()
        self.retrieval_service = RetrievalService(patterns=mock_patterns)
        self.generator_service = GeneratorService(api_key=api_key)

        self.results: List[E2EResult] = []

        logger.info(f"E2EEvaluator initialized with {len(self.dataset)} samples")

    async def evaluate_all(self) -> Dict[str, Any]:
        """
        Run evaluation on all golden dataset screenshots.

        Returns:
            Dictionary with overall metrics and per-screenshot results
        """
        logger.info(f"Starting E2E evaluation on {len(self.dataset)} screenshots")

        self.results = []

        for screenshot_data in self.dataset:
            logger.info(f"Evaluating: {screenshot_data['id']}")
            result = await self.evaluate_single(screenshot_data)
            self.results.append(result)

        # Calculate overall metrics
        metrics = E2EMetrics.calculate_overall_metrics(self.results)

        return {
            'overall': metrics,
            'per_screenshot': [self._result_to_dict(r) for r in self.results],
            'dataset_size': len(self.dataset),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

    async def evaluate_single(self, screenshot_data: Dict) -> E2EResult:
        """
        Evaluate a single screenshot through the full pipeline.

        Args:
            screenshot_data: Golden dataset entry with screenshot and ground truth

        Returns:
            E2EResult with metrics for each stage
        """
        screenshot_id = screenshot_data['id']
        image = screenshot_data['image']
        ground_truth = screenshot_data['ground_truth']

        start_time = time.time()

        # Stage 1: Token Extraction
        logger.info(f"  Stage 1: Token Extraction")
        token_result = await self._evaluate_token_extraction(
            screenshot_id,
            image,
            ground_truth['expected_tokens']
        )

        # Stage 2: Pattern Retrieval
        logger.info(f"  Stage 2: Pattern Retrieval")
        retrieval_result = await self._evaluate_retrieval(
            screenshot_id,
            token_result.extracted_tokens,
            ground_truth['expected_pattern_id']
        )

        # Stage 3: Code Generation
        logger.info(f"  Stage 3: Code Generation")
        generation_result = await self._evaluate_generation(
            screenshot_id,
            retrieval_result.retrieved_pattern_id,
            token_result.extracted_tokens
        )

        total_latency = (time.time() - start_time) * 1000  # ms

        # Pipeline succeeds if all stages pass
        pipeline_success = (
            token_result.accuracy > 0.8 and
            retrieval_result.correct and
            generation_result.code_compiles
        )

        return E2EResult(
            screenshot_id=screenshot_id,
            token_extraction=token_result,
            retrieval=retrieval_result,
            generation=generation_result,
            pipeline_success=pipeline_success,
            total_latency_ms=total_latency
        )

    async def _evaluate_token_extraction(
        self,
        screenshot_id: str,
        image: Any,
        expected_tokens: Dict
    ) -> TokenExtractionResult:
        """
        Evaluate token extraction stage.

        Args:
            screenshot_id: Screenshot identifier
            image: PIL Image object
            expected_tokens: Ground truth tokens

        Returns:
            TokenExtractionResult with accuracy metrics
        """
        from .metrics import TokenExtractionMetrics

        # Handle case where image doesn't exist (placeholder)
        if image is None:
            logger.warning(f"No image for {screenshot_id}, using empty tokens")
            extracted_tokens = {}
        else:
            try:
                extracted = await self.token_extractor.extract_tokens(image)
                extracted_tokens = extracted.get('tokens', {})
            except Exception as e:
                logger.error(f"Token extraction failed for {screenshot_id}: {e}")
                extracted_tokens = {}

        # Calculate accuracy
        accuracy = TokenExtractionMetrics.calculate_accuracy(
            expected_tokens, extracted_tokens
        )

        # Find missing and incorrect tokens
        missing = TokenExtractionMetrics.find_missing_tokens(
            expected_tokens, extracted_tokens
        )
        incorrect = TokenExtractionMetrics.find_incorrect_tokens(
            expected_tokens, extracted_tokens
        )

        return TokenExtractionResult(
            screenshot_id=screenshot_id,
            expected_tokens=expected_tokens,
            extracted_tokens=extracted_tokens,
            accuracy=accuracy,
            missing_tokens=missing,
            incorrect_tokens=incorrect
        )

    async def _evaluate_retrieval(
        self,
        screenshot_id: str,
        tokens: Dict,
        expected_pattern_id: str
    ) -> RetrievalResult:
        """
        Evaluate pattern retrieval stage.

        Args:
            screenshot_id: Screenshot identifier
            tokens: Extracted design tokens
            expected_pattern_id: Expected pattern ID from ground truth

        Returns:
            RetrievalResult with retrieval metrics
        """
        try:
            # Convert tokens to requirements format for retrieval
            requirements = {
                'designTokens': tokens,
                'description': f"Component with tokens: {tokens}"
            }

            # Search for patterns
            results = await self.retrieval_service.search(
                requirements=requirements,
                top_k=5
            )

            # Get top result
            if results and len(results) > 0:
                retrieved_pattern_id = results[0].get('pattern_id', '')
                confidence = results[0].get('score', 0.0)
            else:
                retrieved_pattern_id = ''
                confidence = 0.0

            # Check if correct pattern was retrieved
            correct = retrieved_pattern_id == expected_pattern_id

            # Find rank of correct pattern
            rank = 999  # Large number if not found
            for i, result in enumerate(results):
                if result.get('pattern_id') == expected_pattern_id:
                    rank = i + 1
                    break

        except Exception as e:
            logger.error(f"Retrieval failed for {screenshot_id}: {e}")
            retrieved_pattern_id = ''
            correct = False
            rank = 999
            confidence = 0.0

        return RetrievalResult(
            screenshot_id=screenshot_id,
            expected_pattern_id=expected_pattern_id,
            retrieved_pattern_id=retrieved_pattern_id,
            correct=correct,
            rank=rank,
            confidence=confidence
        )

    async def _evaluate_generation(
        self,
        screenshot_id: str,
        pattern_id: str,
        tokens: Dict
    ) -> EvalGenerationResult:
        """
        Evaluate code generation stage.

        Args:
            screenshot_id: Screenshot identifier
            pattern_id: Retrieved pattern ID
            tokens: Extracted design tokens

        Returns:
            EvalGenerationResult with generation metrics
        """
        start_time = time.time()

        # If pattern retrieval failed, can't generate
        if not pattern_id:
            return EvalGenerationResult(
                screenshot_id=screenshot_id,
                code_generated=False,
                code_compiles=False,
                quality_score=0.0,
                validation_errors=['Pattern retrieval failed'],
                generation_time_ms=(time.time() - start_time) * 1000
            )

        try:
            # Create generation request
            request = GenerationRequest(
                pattern_id=pattern_id,
                tokens=tokens,
                requirements=[]  # No additional requirements for evaluation
            )

            # Generate code
            result = await self.generator_service.generate(request)

            generation_time = (time.time() - start_time) * 1000

            # Extract validation info
            code_compiles = True
            quality_score = 1.0
            validation_errors = []

            if result.validation_results:
                # Check TypeScript compilation
                code_compiles = result.validation_results.typescript_passed

                # Get quality score (convert 0-100 to 0.0-1.0)
                quality_score = result.validation_results.overall_score / 100.0

                # Collect errors
                if result.validation_results.typescript_errors:
                    validation_errors.extend([
                        f"TS: {e.message}" for e in result.validation_results.typescript_errors
                    ])
                if result.validation_results.eslint_errors:
                    validation_errors.extend([
                        f"ESLint: {e.message}" for e in result.validation_results.eslint_errors
                    ])

            return EvalGenerationResult(
                screenshot_id=screenshot_id,
                code_generated=result.success,
                code_compiles=code_compiles,
                quality_score=quality_score,
                validation_errors=validation_errors,
                generation_time_ms=generation_time
            )

        except Exception as e:
            logger.error(f"Generation failed for {screenshot_id}: {e}")
            return EvalGenerationResult(
                screenshot_id=screenshot_id,
                code_generated=False,
                code_compiles=False,
                quality_score=0.0,
                validation_errors=[str(e)],
                generation_time_ms=(time.time() - start_time) * 1000
            )

    def _create_mock_patterns(self) -> List[Dict]:
        """
        Create mock patterns for testing.

        Returns:
            List of mock pattern dictionaries with minimal required fields
        """
        return [
            {
                "id": "button",
                "name": "Button",
                "description": "Interactive button component",
                "component_type": "button",
            },
            {
                "id": "card",
                "name": "Card",
                "description": "Content container card component",
                "component_type": "card",
            },
            {
                "id": "badge",
                "name": "Badge",
                "description": "Small label or tag badge component",
                "component_type": "badge",
            },
            {
                "id": "input",
                "name": "Input",
                "description": "Text input field component",
                "component_type": "input",
            },
            {
                "id": "checkbox",
                "name": "Checkbox",
                "description": "Checkbox selection component",
                "component_type": "checkbox",
            },
            {
                "id": "alert",
                "name": "Alert",
                "description": "Alert or notification banner component",
                "component_type": "alert",
            },
            {
                "id": "select",
                "name": "Select",
                "description": "Dropdown select component",
                "component_type": "select",
            },
            {
                "id": "switch",
                "name": "Switch",
                "description": "Toggle switch component",
                "component_type": "switch",
            },
            {
                "id": "radio",
                "name": "Radio",
                "description": "Radio button group component",
                "component_type": "radio",
            },
            {
                "id": "tabs",
                "name": "Tabs",
                "description": "Tabbed navigation component",
                "component_type": "tabs",
            },
        ]

    def _result_to_dict(self, result: E2EResult) -> Dict:
        """
        Convert E2EResult to dictionary for JSON serialization.

        Args:
            result: E2EResult object

        Returns:
            Dictionary representation
        """
        return {
            'screenshot_id': result.screenshot_id,
            'pipeline_success': result.pipeline_success,
            'total_latency_ms': result.total_latency_ms,
            'token_extraction': {
                'accuracy': result.token_extraction.accuracy,
                'missing_tokens': result.token_extraction.missing_tokens,
                'incorrect_tokens': result.token_extraction.incorrect_tokens,
            },
            'retrieval': {
                'correct': result.retrieval.correct,
                'expected': result.retrieval.expected_pattern_id,
                'retrieved': result.retrieval.retrieved_pattern_id,
                'rank': result.retrieval.rank,
                'confidence': result.retrieval.confidence,
            },
            'generation': {
                'code_generated': result.generation.code_generated,
                'code_compiles': result.generation.code_compiles,
                'quality_score': result.generation.quality_score,
                'validation_errors': result.generation.validation_errors,
                'generation_time_ms': result.generation.generation_time_ms,
            }
        }
