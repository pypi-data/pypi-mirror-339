"""
Result Ranker Module for LlamaFind Ultimate

This module provides MLX-accelerated ranking for search results from different sources.
It uses embedding similarity, freshness, source quality, and diversity factors for
optimal ranking.
"""

import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import urlparse

import yaml

# Internal imports
from llamafind.mlx_compat import is_mlx_available, should_use_mlx

# Configure logging
logger = logging.getLogger(__name__)


# Load configuration
def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "config",
        "config.yml",
    )
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.warning(f"Error loading config: {e}. Using defaults.")
        return {}


CONFIG = load_config()
RANKING_CONFIG = CONFIG.get("ranking", {})

# Check MLX availability
HAS_MLX = is_mlx_available()
USE_MLX = should_use_mlx()

# Try to import MLX packages if available
if USE_MLX:
    try:
        import numpy as np

        # Try to import MLX Embeddings
        try:
            import mlx_embeddings

            HAS_MLX_EMBEDDINGS = True
            logger.info("MLX Embeddings package available for result ranking")
        except ImportError:
            HAS_MLX_EMBEDDINGS = False
            logger.warning("MLX Embeddings package not available, falling back to basic ranking")
    except ImportError:
        logger.warning("NumPy not available, using basic result ranking")
        HAS_MLX_EMBEDDINGS = False
else:
    # Fallback to basic ranking
    HAS_MLX_EMBEDDINGS = False

# Default ranking weights
DEFAULT_WEIGHTS = {
    "relevance": RANKING_CONFIG.get("relevance_weight", 0.6),
    "freshness": RANKING_CONFIG.get("freshness_weight", 0.1),
    "authority": RANKING_CONFIG.get("authority_weight", 0.15),
    "diversity": RANKING_CONFIG.get("diversity_weight", 0.15),
}

# Authority scores for different domains
AUTHORITY_SCORES = {
    "wikipedia.org": 0.9,
    "github.com": 0.85,
    "stackoverflow.com": 0.8,
    "docs.python.org": 0.9,
    "developer.mozilla.org": 0.85,
    "medium.com": 0.6,
    "reddit.com": 0.5,
    "arxiv.org": 0.8,
    "ieee.org": 0.85,
    "acm.org": 0.85,
    "nature.com": 0.9,
    "science.org": 0.9,
    "edu": 0.75,
    "gov": 0.8,
}


class ResultRanker:
    """
    MLX-accelerated search result ranker.
    Uses embedding similarity, freshness, source quality, and diversity factors.
    """

    def __init__(
        self,
        mlx_enabled: bool = True,
        weights: Dict[str, float] = None,
        config: Dict[str, Any] = None,
    ):
        """
        Initialize the result ranker.

        Args:
            mlx_enabled: Whether to use MLX acceleration if available
            weights: Custom ranking weights (overrides config)
            config: Configuration dictionary (overrides YAML config)
        """
        self.config = config or RANKING_CONFIG
        self.mlx_enabled = mlx_enabled and USE_MLX and HAS_MLX_EMBEDDINGS

        # Set ranking weights
        self.weights = weights or {
            "relevance": self.config.get("relevance_weight", DEFAULT_WEIGHTS["relevance"]),
            "freshness": self.config.get("freshness_weight", DEFAULT_WEIGHTS["freshness"]),
            "authority": self.config.get("authority_weight", DEFAULT_WEIGHTS["authority"]),
            "diversity": self.config.get("diversity_weight", DEFAULT_WEIGHTS["diversity"]),
        }

        # Normalize weights to ensure they sum to 1
        weight_sum = sum(self.weights.values())
        if weight_sum > 0:
            self.weights = {k: v / weight_sum for k, v in self.weights.items()}

        # Minimum score threshold
        self.min_score = self.config.get("min_score", 0.3)

        # Embedding model
        self.embedding_model = None
        self.embedding_model_loaded = False

        # Initialize MLX embedding model if available
        if self.mlx_enabled:
            self._init_mlx_embedding_model()

        logger.info(
            f"Result ranker initialized. MLX: {'enabled' if self.mlx_enabled else 'disabled'}"
        )

    def _init_mlx_embedding_model(self):
        """Initialize MLX embedding model for semantic ranking."""
        if not self.mlx_enabled or self.embedding_model_loaded:
            return

        try:
            # Load embedding model using MLX Embeddings
            import mlx_embeddings

            model_name = self.config.get("models", {}).get(
                "embeddings", "mlx_embeddings/all-MiniLM-L6-v2"
            )
            logger.info(f"Loading MLX embedding model: {model_name}")

            # Try to load the model
            self.embedding_model = mlx_embeddings.load_model(model_name)
            self.embedding_model_loaded = True
            logger.info(f"MLX embedding model loaded successfully: {model_name}")

        except Exception as e:
            logger.error(f"Error loading MLX embedding model: {e}")
            self.embedding_model_loaded = False
            self.mlx_enabled = False

    def rank_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Rank search results based on multiple factors.

        Args:
            results: List of search results to rank
            query: Original search query

        Returns:
            List[Dict[str, Any]]: Ranked results
        """
        if not results:
            return []

        # Log ranking request
        logger.info(f"Ranking {len(results)} results for query: '{query}'")

        # Use MLX-accelerated ranking if available
        if self.mlx_enabled and self.embedding_model_loaded:
            ranked_results = self._rank_results_mlx(results, query)
        else:
            # Use basic ranking
            ranked_results = self._rank_results_basic(results, query)

        # Filter out results below minimum score
        filtered_results = [r for r in ranked_results if r.get("_score", 0) >= self.min_score]

        # Log ranking results
        logger.info(f"Ranked {len(filtered_results)} results (filtered from {len(ranked_results)})")

        return filtered_results

    def _rank_results_mlx(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Rank results using MLX embeddings for semantic similarity.

        Args:
            results: List of search results to rank
            query: Original search query

        Returns:
            List[Dict[str, Any]]: Ranked results
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.embed(query)

            # Calculate scores for each result
            scored_results = []
            seen_urls = set()

            for i, result in enumerate(results):
                # Skip duplicate URLs
                url = result.get("url", "")
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                # Create a copy of the result
                scored_result = dict(result)

                # Calculate relevance score using semantic similarity
                text_to_embed = (
                    result.get("title", "")
                    + " "
                    + result.get("content", "")
                    + " "
                    + result.get("summary", "")
                )
                if text_to_embed.strip():
                    result_embedding = self.embedding_model.embed(text_to_embed)
                    relevance_score = self._compute_similarity(query_embedding, result_embedding)
                else:
                    relevance_score = 0.0

                # Calculate other scores
                freshness_score = self._calculate_freshness_score(result)
                authority_score = self._calculate_authority_score(result)
                diversity_score = self._calculate_diversity_score(result, i, len(results))

                # Calculate final score
                final_score = (
                    self.weights["relevance"] * relevance_score
                    + self.weights["freshness"] * freshness_score
                    + self.weights["authority"] * authority_score
                    + self.weights["diversity"] * diversity_score
                )

                # Add scores to result
                scored_result["_relevance_score"] = relevance_score
                scored_result["_freshness_score"] = freshness_score
                scored_result["_authority_score"] = authority_score
                scored_result["_diversity_score"] = diversity_score
                scored_result["_score"] = final_score

                # Add to scored results
                scored_results.append(scored_result)

            # Sort by score
            ranked_results = sorted(scored_results, key=lambda x: x.get("_score", 0), reverse=True)

            return ranked_results

        except Exception as e:
            logger.error(f"Error in MLX result ranking: {e}")
            # Fall back to basic ranking
            return self._rank_results_basic(results, query)

    def _rank_results_basic(
        self, results: List[Dict[str, Any]], query: str
    ) -> List[Dict[str, Any]]:
        """
        Rank results using basic relevance calculation.

        Args:
            results: List of search results to rank
            query: Original search query

        Returns:
            List[Dict[str, Any]]: Ranked results
        """
        # Extract query terms
        query_terms = set(re.findall(r"\w+", query.lower()))

        # Calculate scores for each result
        scored_results = []
        seen_urls = set()

        for i, result in enumerate(results):
            # Skip duplicate URLs
            url = result.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            # Create a copy of the result
            scored_result = dict(result)

            # Calculate relevance score using term frequency
            title = result.get("title", "")
            content = result.get("content", "")
            title_terms = set(re.findall(r"\w+", title.lower()))
            content_terms = set(re.findall(r"\w+", content.lower()))

            # Calculate relevance based on term overlap
            title_overlap = (
                len(query_terms.intersection(title_terms)) / len(query_terms) if query_terms else 0
            )
            content_overlap = (
                len(query_terms.intersection(content_terms)) / len(query_terms)
                if query_terms
                else 0
            )

            # Title matches are more important than content matches
            relevance_score = 0.7 * title_overlap + 0.3 * content_overlap

            # Calculate other scores
            freshness_score = self._calculate_freshness_score(result)
            authority_score = self._calculate_authority_score(result)
            diversity_score = self._calculate_diversity_score(result, i, len(results))

            # Calculate final score
            final_score = (
                self.weights["relevance"] * relevance_score
                + self.weights["freshness"] * freshness_score
                + self.weights["authority"] * authority_score
                + self.weights["diversity"] * diversity_score
            )

            # Add scores to result
            scored_result["_relevance_score"] = relevance_score
            scored_result["_freshness_score"] = freshness_score
            scored_result["_authority_score"] = authority_score
            scored_result["_diversity_score"] = diversity_score
            scored_result["_score"] = final_score

            # Add to scored results
            scored_results.append(scored_result)

        # Sort by score
        ranked_results = sorted(scored_results, key=lambda x: x.get("_score", 0), reverse=True)

        return ranked_results

    def _calculate_freshness_score(self, result: Dict[str, Any]) -> float:
        """
        Calculate freshness score based on result timestamp.

        Args:
            result: Search result

        Returns:
            float: Freshness score
        """
        # Get timestamp
        timestamp = result.get("timestamp")

        # If no timestamp, assume it's not fresh
        if not timestamp:
            return 0.5

        try:
            # Convert timestamp to datetime
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

            # Calculate age in days
            age_days = (datetime.now() - timestamp).days

            # Calculate freshness score (1.0 for today, decreasing over time)
            if age_days <= 0:
                return 1.0
            elif age_days <= 30:
                return 1.0 - (age_days / 30) * 0.5
            elif age_days <= 365:
                return 0.5 - (age_days - 30) / (365 - 30) * 0.3
            else:
                return 0.2

        except Exception:
            # If parsing fails, assume medium freshness
            return 0.5

    def _calculate_authority_score(self, result: Dict[str, Any]) -> float:
        """
        Calculate authority score based on result source.

        Args:
            result: Search result

        Returns:
            float: Authority score
        """
        # Get URL
        url = result.get("url", "")

        # If no URL, assume medium authority
        if not url:
            return 0.5

        try:
            # Parse domain
            domain = urlparse(url).netloc.lower()

            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]

            # Check for exact domain match
            if domain in AUTHORITY_SCORES:
                return AUTHORITY_SCORES[domain]

            # Check for domain suffix match (e.g., .edu, .gov)
            for suffix, score in AUTHORITY_SCORES.items():
                if domain.endswith(f".{suffix}"):
                    return score

            # Default score based on domain TLD
            tld = domain.split(".")[-1] if "." in domain else ""
            if tld in ["com", "org", "net"]:
                return 0.6
            elif tld in ["io", "ai", "co"]:
                return 0.65
            else:
                return 0.5

        except Exception:
            # If parsing fails, assume medium authority
            return 0.5

    def _calculate_diversity_score(self, result: Dict[str, Any], index: int, total: int) -> float:
        """
        Calculate diversity score based on result position and source.

        Args:
            result: Search result
            index: Result index in the original list
            total: Total number of results

        Returns:
            float: Diversity score
        """
        # Get source
        source = result.get("source", "")

        # Position-based diversity (favor earlier results from the original ranking)
        position_score = 1.0 - (index / total) if total > 1 else 1.0

        # Source-based diversity (different sources get higher scores)
        source_score = 0.7
        if source in ["google", "bing", "duckduckgo"]:
            source_score = 0.8
        elif source in ["elasticsearch", "local"]:
            source_score = 0.9

        # Combine scores
        return 0.7 * position_score + 0.3 * source_score

    def _compute_similarity(self, embedding1, embedding2) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First embedding
            embedding2: Second embedding

        Returns:
            float: Cosine similarity
        """
        # Compute dot product
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

        # Compute magnitudes
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5

        # Compute cosine similarity
        if magnitude1 * magnitude2 == 0:
            return 0

        return dot_product / (magnitude1 * magnitude2)


# Create global ranker instance
result_ranker = ResultRanker(mlx_enabled=USE_MLX)


# Convenience function
def rank_results(results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Rank search results based on multiple factors.

    Args:
        results: List of search results to rank
        query: Original search query

    Returns:
        List[Dict[str, Any]]: Ranked results
    """
    return result_ranker.rank_results(results, query)
