"""
Query Expander Module for LlamaFind Ultimate

This module provides MLX-accelerated query expansion to improve search relevance by:
1. Expanding search terms with related concepts
2. Adding contextual keywords
3. Detecting and handling intent
"""

import logging
import os
import re
from typing import Any, Dict, List

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
MLX_CONFIG = CONFIG.get("mlx", {})

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
            logger.info("MLX Embeddings package available for query expansion")
        except ImportError:
            HAS_MLX_EMBEDDINGS = False
            logger.warning("MLX Embeddings package not available, falling back to basic expansion")
    except ImportError:
        logger.warning("NumPy not available, using basic query expansion")
        HAS_MLX_EMBEDDINGS = False
else:
    # Fallback to basic expansion
    HAS_MLX_EMBEDDINGS = False

# Constants and resources
STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "then",
    "else",
    "when",
    "at",
    "from",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "of",
    "in",
    "on",
}

# Basic synonym mappings for non-MLX mode
SYNONYMS = {
    "car": ["automobile", "vehicle", "sedan", "suv"],
    "phone": ["smartphone", "mobile", "cellphone", "telephone"],
    "computer": ["laptop", "pc", "desktop", "workstation"],
    "program": ["software", "application", "app", "code"],
    "fast": ["quick", "rapid", "swift", "speedy"],
    "big": ["large", "huge", "enormous", "substantial"],
    "small": ["tiny", "little", "compact", "miniature"],
    "good": ["great", "excellent", "superior", "quality"],
    "bad": ["poor", "inferior", "substandard", "terrible"],
    "important": ["crucial", "essential", "key", "vital"],
    "machine learning": ["ml", "ai", "artificial intelligence", "deep learning"],
    "python": ["python language", "python programming", "python framework"],
    "javascript": ["js", "ecmascript", "typescript", "frontend development"],
    "database": ["db", "sql", "nosql", "data storage"],
}


class QueryExpander:
    """
    Query expander class for improving search queries using MLX acceleration when available.
    """

    def __init__(self, mlx_enabled: bool = True, config: Dict[str, Any] = None):
        """
        Initialize query expander.

        Args:
            mlx_enabled: Whether to use MLX acceleration if available
            config: Configuration dictionary (overrides YAML config)
        """
        self.config = config or MLX_CONFIG
        self.mlx_enabled = mlx_enabled and USE_MLX and HAS_MLX_EMBEDDINGS

        # Embedding model
        self.embedding_model = None
        self.embedding_model_loaded = False

        # Maximum terms to add to a query
        self.max_expansion_terms = self.config.get("max_expansion_terms", 3)
        self.min_term_similarity = self.config.get("min_term_similarity", 0.7)

        # Initialize MLX embedding model if available
        if self.mlx_enabled:
            self._init_mlx_embedding_model()

        logger.info(
            f"Query expander initialized. MLX: {'enabled' if self.mlx_enabled else 'disabled'}"
        )

    def _init_mlx_embedding_model(self):
        """Initialize MLX embedding model for semantic expansion."""
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

    def expand_query(self, query: str, max_terms: int = None) -> str:
        """
        Expand a search query with additional related terms.

        Args:
            query: Original search query
            max_terms: Maximum number of terms to add (overrides config)

        Returns:
            str: Expanded query
        """
        if not query or query.strip() == "":
            return query

        # Clean query
        query = query.strip()

        # Log original query
        logger.info(f"Expanding query: '{query}'")

        # Determine maximum additional terms
        max_terms = max_terms or self.max_expansion_terms

        # Use MLX-accelerated expansion if available
        if self.mlx_enabled and self.embedding_model_loaded:
            expanded_query = self._expand_query_mlx(query, max_terms)
        else:
            # Use basic expansion
            expanded_query = self._expand_query_basic(query, max_terms)

        # Log expanded query
        logger.info(f"Original query: '{query}'")
        logger.info(f"Expanded query: '{expanded_query}'")

        return expanded_query

    def _expand_query_mlx(self, query: str, max_terms: int) -> str:
        """
        Expand query using MLX embeddings for semantic similarity.

        Args:
            query: Original search query
            max_terms: Maximum number of terms to add

        Returns:
            str: Expanded query
        """
        try:
            # Tokenize query
            tokens = self._tokenize(query)
            original_tokens = set(tokens)

            # Skip if too short
            if len(tokens) <= 1:
                return query

            # Generate query embedding
            query_embedding = self.embedding_model.embed(query)

            # Get similar terms from our vocabulary
            # This is a simplified example - in a real implementation,
            # we would have a larger vocabulary with pre-computed embeddings
            expansion_candidates = {}

            # Generate embeddings for common terms and phrases
            vocabulary = list(SYNONYMS.keys()) + [
                item for sublist in SYNONYMS.values() for item in sublist
            ]

            for term in vocabulary:
                if term.lower() in original_tokens:
                    continue

                term_embedding = self.embedding_model.embed(term)
                similarity = self._compute_similarity(query_embedding, term_embedding)

                if similarity > self.min_term_similarity:
                    expansion_candidates[term] = similarity

            # Sort by similarity and take top terms
            expansion_terms = sorted(
                expansion_candidates.items(), key=lambda x: x[1], reverse=True
            )[:max_terms]

            # Combine with original query
            if expansion_terms:
                expanded_query = query + " " + " ".join([term for term, _ in expansion_terms])
                return expanded_query

            return query

        except Exception as e:
            logger.error(f"Error in MLX query expansion: {e}")
            # Fall back to basic expansion
            return self._expand_query_basic(query, max_terms)

    def _expand_query_basic(self, query: str, max_terms: int) -> str:
        """
        Expand query using basic synonym lookup.

        Args:
            query: Original search query
            max_terms: Maximum number of terms to add

        Returns:
            str: Expanded query
        """
        # Tokenize query
        tokens = self._tokenize(query)

        # Skip if too short
        if len(tokens) <= 1:
            return query

        # Find synonyms for each token
        expansion_terms = set()

        for token in tokens:
            token_lower = token.lower()

            # Check for multi-word tokens
            for key in SYNONYMS:
                if token_lower == key or key.startswith(token_lower):
                    # Add synonyms
                    expansion_terms.update(SYNONYMS[key])

                    # Stop if we have enough terms
                    if len(expansion_terms) >= max_terms:
                        break

        # Remove original tokens from expansion
        expansion_terms = set(
            term for term in expansion_terms if term.lower() not in map(str.lower, tokens)
        )

        # Take top terms
        expansion_terms = list(expansion_terms)[:max_terms]

        # Combine with original query
        if expansion_terms:
            expanded_query = query + " " + " ".join(expansion_terms)
            return expanded_query

        return query

    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words and phrases.

        Args:
            text: Text to tokenize

        Returns:
            List[str]: List of tokens
        """
        # Convert to lowercase
        text = text.lower()

        # Replace punctuation with spaces
        text = re.sub(r"[^\w\s]", " ", text)

        # Split into tokens
        tokens = text.split()

        # Remove stopwords
        tokens = [token for token in tokens if token not in STOPWORDS]

        # Combine adjacent tokens for phrases (bi-grams)
        phrases = []
        for i in range(len(tokens) - 1):
            phrases.append(tokens[i] + " " + tokens[i + 1])

        # Combine tokens and phrases
        return tokens + phrases

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


# Create global expander instance
query_expander = QueryExpander(mlx_enabled=USE_MLX)


# Convenience function
def expand_query(query: str, max_terms: int = None) -> str:
    """
    Expand a search query with additional related terms.

    Args:
        query: Original search query
        max_terms: Maximum number of terms to add

    Returns:
        str: Expanded query
    """
    return query_expander.expand_query(query, max_terms)
