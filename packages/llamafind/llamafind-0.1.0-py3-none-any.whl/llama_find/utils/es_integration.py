"""
Elasticsearch Integration Module for LlamaFind Ultimate

This module provides functionality for connecting to Elasticsearch,
creating indices, and performing search operations with advanced query options.
"""

import logging
import os
from typing import Any, Dict, List

import yaml
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Q, Search

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
        return {"elasticsearch": {"host": "localhost", "port": 9200}}


CONFIG = load_config()
ES_CONFIG = CONFIG.get("elasticsearch", {})

# Get Elasticsearch settings from environment or config
ES_HOST = os.environ.get("ELASTICSEARCH_HOST", ES_CONFIG.get("host", "localhost"))
ES_PORT = int(os.environ.get("ELASTICSEARCH_PORT", ES_CONFIG.get("port", 9200)))
ES_TIMEOUT = ES_CONFIG.get("timeout", 30)
ES_INDEX_PREFIX = ES_CONFIG.get("index_prefix", "llamafind_")

# Index configurations
INDEX_MAPPINGS = {
    "web": {
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"},
                "summary": {"type": "text", "analyzer": "standard"},
                "tags": {"type": "keyword"},
                "embedding": {"type": "dense_vector", "dims": 384},
                "source": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "rank": {"type": "float"},
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {"analyzer": {"standard": {"type": "standard", "stopwords": "_english_"}}},
        },
    },
    "queries": {
        "mappings": {
            "properties": {
                "query": {"type": "text", "analyzer": "standard"},
                "expanded_query": {"type": "text", "analyzer": "standard"},
                "timestamp": {"type": "date"},
                "user_id": {"type": "keyword"},
                "embedding": {"type": "dense_vector", "dims": 384},
            }
        }
    },
    "embeddings": {
        "mappings": {
            "properties": {
                "text": {"type": "text", "analyzer": "standard"},
                "embedding": {"type": "dense_vector", "dims": 384},
                "source": {"type": "keyword"},
                "timestamp": {"type": "date"},
            }
        }
    },
}


class ElasticsearchManager:
    """Manager class for Elasticsearch operations."""

    def __init__(self, host: str = ES_HOST, port: int = ES_PORT, timeout: int = ES_TIMEOUT):
        """
        Initialize Elasticsearch manager.

        Args:
            host: Elasticsearch host
            port: Elasticsearch port
            timeout: Connection timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = None
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to Elasticsearch.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if self.connected and self.client:
            return True

        try:
            # Create Elasticsearch client
            self.client = Elasticsearch(
                [{"host": self.host, "port": self.port, "scheme": "http"}],
                timeout=self.timeout,
            )

            # Check connection
            if self.client.ping():
                logger.info(f"Connected to Elasticsearch at {self.host}:{self.port}")
                self.connected = True
                return True
            else:
                logger.error(f"Failed to ping Elasticsearch at {self.host}:{self.port}")
                self.connected = False
                return False

        except Exception as e:
            logger.error(f"Error connecting to Elasticsearch: {e}")
            self.connected = False
            return False

    def create_indices(self, force_recreate: bool = False) -> Dict[str, bool]:
        """
        Create necessary indices in Elasticsearch.

        Args:
            force_recreate: If True, delete and recreate indices

        Returns:
            Dict[str, bool]: Dictionary of index names and creation status
        """
        if not self.connect():
            logger.error("Cannot create indices: Not connected to Elasticsearch")
            return {index: False for index in INDEX_MAPPINGS.keys()}

        results = {}

        for index_type, index_config in INDEX_MAPPINGS.items():
            index_name = f"{ES_INDEX_PREFIX}{index_type}"

            try:
                # Check if index exists
                index_exists = self.client.indices.exists(index=index_name)

                # Delete index if it exists and force_recreate is True
                if index_exists and force_recreate:
                    logger.info(f"Deleting existing index: {index_name}")
                    self.client.indices.delete(index=index_name)
                    index_exists = False

                # Create index if it doesn't exist
                if not index_exists:
                    logger.info(f"Creating index: {index_name}")
                    self.client.indices.create(index=index_name, body=index_config)
                    results[index_type] = True
                else:
                    logger.info(f"Index already exists: {index_name}")
                    results[index_type] = True

            except Exception as e:
                logger.error(f"Error creating index {index_name}: {e}")
                results[index_type] = False

        return results

    def index_document(self, index_type: str, document: Dict[str, Any]) -> bool:
        """
        Index a single document.

        Args:
            index_type: Type of index (web, queries, embeddings)
            document: Document to index

        Returns:
            bool: True if indexing successful, False otherwise
        """
        if not self.connect():
            logger.error("Cannot index document: Not connected to Elasticsearch")
            return False

        index_name = f"{ES_INDEX_PREFIX}{index_type}"

        try:
            result = self.client.index(index=index_name, body=document, refresh=True)
            logger.debug(f"Indexed document in {index_name}: {result}")
            return True

        except Exception as e:
            logger.error(f"Error indexing document in {index_name}: {e}")
            return False

    def bulk_index(self, index_type: str, documents: List[Dict[str, Any]]) -> int:
        """
        Bulk index multiple documents.

        Args:
            index_type: Type of index (web, queries, embeddings)
            documents: List of documents to index

        Returns:
            int: Number of successfully indexed documents
        """
        if not self.connect():
            logger.error("Cannot bulk index documents: Not connected to Elasticsearch")
            return 0

        if not documents:
            logger.warning("No documents to index")
            return 0

        index_name = f"{ES_INDEX_PREFIX}{index_type}"

        try:
            # Prepare bulk actions
            actions = [{"_index": index_name, "_source": document} for document in documents]

            # Execute bulk indexing
            success, failed = bulk(self.client, actions, refresh=True, raise_on_error=False)

            if failed:
                logger.warning(f"Failed to index {len(failed)} documents")

            logger.info(f"Successfully indexed {success} documents in {index_name}")
            return success

        except Exception as e:
            logger.error(f"Error bulk indexing documents in {index_name}: {e}")
            return 0

    def search(self, query: str, index_type: str = "web", size: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents matching a query.

        Args:
            query: Search query
            index_type: Type of index to search (web, queries, embeddings)
            size: Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of matching documents
        """
        if not self.connect():
            logger.error("Cannot search: Not connected to Elasticsearch")
            return []

        index_name = f"{ES_INDEX_PREFIX}{index_type}"

        try:
            # Create search object
            search = Search(using=self.client, index=index_name)

            # Add query
            q = Q("multi_match", query=query, fields=["title^2", "content", "summary^1.5"])
            search = search.query(q)

            # Set result size
            search = search.extra(size=size)

            # Execute search
            response = search.execute()

            # Process results
            results = []
            for hit in response:
                result = hit.to_dict()
                result["_score"] = hit.meta.score
                results.append(result)

            logger.info(f"Search for '{query}' returned {len(results)} results from {index_name}")
            return results

        except Exception as e:
            logger.error(f"Error searching in {index_name}: {e}")
            return []

    def vector_search(
        self, embedding: List[float], index_type: str = "web", size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for documents by vector similarity.

        Args:
            embedding: Query embedding vector
            index_type: Type of index to search (web, queries, embeddings)
            size: Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of matching documents
        """
        if not self.connect():
            logger.error("Cannot search: Not connected to Elasticsearch")
            return []

        index_name = f"{ES_INDEX_PREFIX}{index_type}"

        try:
            # Create script score query
            script_query = {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": embedding},
                    },
                }
            }

            # Execute search
            response = self.client.search(
                index=index_name,
                body={
                    "size": size,
                    "query": script_query,
                    "_source": {"excludes": ["embedding"]},
                },
            )

            # Process results
            results = []
            for hit in response["hits"]["hits"]:
                result = hit["_source"]
                result["_score"] = hit["_score"]
                results.append(result)

            logger.info(f"Vector search returned {len(results)} results from {index_name}")
            return results

        except Exception as e:
            logger.error(f"Error performing vector search in {index_name}: {e}")
            return []


# Create global manager instance
es_manager = ElasticsearchManager()


# Convenience functions
def connect_elasticsearch() -> bool:
    """Connect to Elasticsearch."""
    return es_manager.connect()


def create_indices(force_recreate: bool = False) -> Dict[str, bool]:
    """Create necessary indices."""
    return es_manager.create_indices(force_recreate)


def index_document(index_type: str, document: Dict[str, Any]) -> bool:
    """Index a single document."""
    return es_manager.index_document(index_type, document)


def bulk_index(index_type: str, documents: List[Dict[str, Any]]) -> int:
    """Bulk index multiple documents."""
    return es_manager.bulk_index(index_type, documents)


def search(query: str, index_type: str = "web", size: int = 10) -> List[Dict[str, Any]]:
    """Search for documents matching a query."""
    return es_manager.search(query, index_type, size)


def vector_search(
    embedding: List[float], index_type: str = "web", size: int = 10
) -> List[Dict[str, Any]]:
    """Search for documents by vector similarity."""
    return es_manager.vector_search(embedding, index_type, size)


def perform_search(query: str, size: int = 10) -> List[Dict[str, Any]]:
    """
    Perform a search with the given query.
    This is the main search function to be used by the API.

    Args:
        query: Search query
        size: Maximum number of results to return

    Returns:
        List[Dict[str, Any]]: List of search results
    """
    # Connect to Elasticsearch if not already connected
    if not es_manager.connected:
        es_manager.connect()

    # Search web index
    results = es_manager.search(query, "web", size)

    # If no results or fewer than requested, try ES_CONFIG search
    if len(results) < size:
        # TODO: Implement additional search strategies
        pass

    return results
