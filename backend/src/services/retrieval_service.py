"""Retrieval service orchestrating the full pattern retrieval pipeline.

This module implements the retrieval orchestration (B7) for Epic 3.
Coordinates query building, BM25, semantic search, fusion, and explainability.
"""

from typing import Dict, List, Optional
import time
import logging
from ..retrieval.query_builder import QueryBuilder
from ..retrieval.bm25_retriever import BM25Retriever
from ..retrieval.semantic_retriever import SemanticRetriever
from ..retrieval.weighted_fusion import WeightedFusion
from ..retrieval.explainer import RetrievalExplainer
from langsmith import traceable

logger = logging.getLogger(__name__)


class RetrievalService:
    """Orchestrates the full retrieval pipeline for pattern matching.
    
    Pipeline:
    1. QueryBuilder: Transform requirements → queries
    2. BM25Retriever: Keyword search
    3. SemanticRetriever: Vector search
    4. WeightedFusion: Combine results
    5. Explainer: Add explanations and confidence scores
    """
    
    def __init__(
        self,
        patterns: List[Dict],
        bm25_retriever: Optional[BM25Retriever] = None,
        semantic_retriever: Optional[SemanticRetriever] = None,
        query_builder: Optional[QueryBuilder] = None,
        weighted_fusion: Optional[WeightedFusion] = None,
        explainer: Optional[RetrievalExplainer] = None
    ):
        """Initialize retrieval service.
        
        Args:
            patterns: List of pattern dictionaries
            bm25_retriever: Optional BM25 retriever (created if None)
            semantic_retriever: Optional semantic retriever
            query_builder: Optional query builder (created if None)
            weighted_fusion: Optional fusion (created if None)
            explainer: Optional explainer (created if None)
        """
        self.patterns = patterns
        
        # Initialize components
        self.query_builder = query_builder or QueryBuilder()
        self.bm25_retriever = bm25_retriever or BM25Retriever(patterns)
        self.semantic_retriever = semantic_retriever
        self.weighted_fusion = weighted_fusion or WeightedFusion()
        self.explainer = explainer or RetrievalExplainer()
        
        logger.info(
            f"Initialized RetrievalService with {len(patterns)} patterns"
        )
    
    @traceable(name="retrieval_search")
    async def search(
        self,
        requirements: Dict,
        top_k: int = 3
    ) -> Dict:
        """Execute full retrieval pipeline.
        
        Args:
            requirements: Requirements dictionary from Epic 2
                Expected keys: component_type, props, variants, a11y
            top_k: Number of top patterns to return (default: 3)
        
        Returns:
            Dictionary containing:
                - patterns: List of top-k patterns with explanations
                - retrieval_metadata: Metadata about retrieval process
        
        Example:
            >>> service = RetrievalService(patterns, semantic_retriever)
            >>> requirements = {
            ...     "component_type": "Button",
            ...     "props": ["variant", "size"],
            ...     "variants": ["primary", "secondary"]
            ... }
            >>> result = await service.search(requirements, top_k=3)
            >>> len(result["patterns"])
            3
        """
        start_time = time.time()
        
        logger.info(f"Starting retrieval for requirements: {requirements}")
        
        # Step 1: Build queries
        queries = self.query_builder.build_from_requirements(requirements)
        bm25_query = queries["bm25_query"]
        semantic_query = queries["semantic_query"]
        filters = queries["filters"]
        
        logger.info(f"Built queries - BM25: '{bm25_query[:50]}...', Semantic: '{semantic_query[:50]}...'")
        
        # Step 2: BM25 search
        bm25_results = self.bm25_retriever.search(bm25_query, top_k=10)
        logger.info(f"BM25 returned {len(bm25_results)} results")
        
        # Step 3: Semantic search (if available)
        semantic_results = []
        methods_used = ["bm25"]
        
        if self.semantic_retriever:
            semantic_results = await self.semantic_retriever.search(
                semantic_query,
                top_k=10,
                filters=filters
            )
            logger.info(f"Semantic search returned {len(semantic_results)} results")
            methods_used.append("semantic")
        else:
            logger.warning("Semantic retriever not available, using BM25 only")
        
        # Step 4: Fusion
        if semantic_results:
            fusion_details = self.weighted_fusion.fuse_with_details(
                bm25_results,
                semantic_results,
                top_k=top_k
            )
        else:
            # Fallback to BM25 only
            fusion_details = [
                {
                    "pattern": pattern,
                    "final_score": score,
                    "final_rank": rank,
                    "bm25_score": score,
                    "bm25_rank": rank,
                    "semantic_score": 0.0,
                    "semantic_rank": None,
                    "weights": {"bm25": 1.0, "semantic": 0.0}
                }
                for rank, (pattern, score) in enumerate(bm25_results[:top_k], start=1)
            ]
        
        logger.info(f"Fusion produced {len(fusion_details)} results")
        
        # Step 5: Add explanations
        enriched_patterns = []
        for detail in fusion_details:
            explanation_data = self.explainer.explain(
                pattern=detail["pattern"],
                requirements=requirements,
                bm25_score=detail["bm25_score"],
                bm25_rank=detail["bm25_rank"] or 999,
                semantic_score=detail["semantic_score"],
                semantic_rank=detail["semantic_rank"] or 999,
                final_score=detail["final_score"],
                final_rank=detail["final_rank"]
            )
            
            # Combine pattern with explanation
            enriched_pattern = {
                **detail["pattern"],
                "confidence": explanation_data["confidence"],
                "explanation": explanation_data["explanation"],
                "match_highlights": explanation_data["match_highlights"],
                "ranking_details": explanation_data["ranking_details"]
            }
            enriched_patterns.append(enriched_pattern)
        
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)
        
        logger.info(f"Retrieval completed in {latency_ms}ms, returning {len(enriched_patterns)} patterns")
        
        # Build response
        return {
            "patterns": enriched_patterns,
            "retrieval_metadata": {
                "latency_ms": latency_ms,
                "methods_used": methods_used,
                "weights": {
                    "bm25": self.weighted_fusion.bm25_weight,
                    "semantic": self.weighted_fusion.semantic_weight
                },
                "total_patterns_searched": len(self.patterns),
                "query": semantic_query if semantic_query else bm25_query
            }
        }
