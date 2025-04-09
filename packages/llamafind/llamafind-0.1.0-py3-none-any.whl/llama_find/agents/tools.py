"""
Agent Tools Module

This module provides a set of tools/functions that can be registered with the function caller
for agents to use.
"""

import logging
import time
from typing import Any, Dict

# Attempt to import search functionality, with graceful failure if not available
try:
    from ..utils.result_ranker import rank_results
    from ..utils.search import search_documents as search_backend

    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False
    logging.warning("Search functionality not available for agent tools")

logger = logging.getLogger(__name__)

# ===== Search Tools =====


def search(query: str, limit: int = 5, expand_query: bool = True) -> Dict[str, Any]:
    """
    Search for documents matching the given query.

    Args:
        query: The search query
        limit: Maximum number of results to return
        expand_query: Whether to expand the query using MLX

    Returns:
        A dictionary containing search results
    """
    if not SEARCH_AVAILABLE:
        return {"error": "Search functionality not available", "results": []}

    try:
        logger.info(f"Agent executing search for '{query}'")

        # Call the backend search function
        results = search_backend(query=query, limit=limit, expand_query=expand_query)

        # Rank the results if possible
        try:
            ranked_results = rank_results(results, query)
        except Exception as e:
            logger.warning(f"Failed to rank search results: {e}")
            ranked_results = results

        # Extract relevant information from the results
        formatted_results = []
        for result in ranked_results:
            formatted_results.append(
                {
                    "title": result.get("title", "Unknown Title"),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "source": result.get("source", ""),
                    "score": result.get("score", 0),
                    "last_updated": result.get("last_updated", ""),
                }
            )

        return {
            "results": formatted_results,
            "count": len(formatted_results),
            "query": query,
            "expanded_query": (results[0].get("expanded_query", query) if results else query),
        }

    except Exception as e:
        logger.error(f"Error executing search: {str(e)}")
        return {"error": str(e), "results": []}


# ===== Information Tools =====


def get_current_time() -> Dict[str, Any]:
    """
    Get the current time and date.

    Returns:
        A dictionary containing the current time information
    """
    import datetime

    now = datetime.datetime.now()
    utc_now = datetime.datetime.utcnow()

    return {
        "local_time": now.strftime("%H:%M:%S"),
        "local_date": now.strftime("%Y-%m-%d"),
        "utc_time": utc_now.strftime("%H:%M:%S"),
        "utc_date": utc_now.strftime("%Y-%m-%d"),
        "timestamp": int(time.time()),
        "timezone": str(datetime.datetime.now().astimezone().tzinfo),
    }


def system_info() -> Dict[str, Any]:
    """
    Get system information.

    Returns:
        A dictionary containing system information
    """
    import platform

    import psutil

    try:
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": {
                "total": psutil.disk_usage("/").total,
                "used": psutil.disk_usage("/").used,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent,
            },
        }
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        return {
            "error": str(e),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
        }


# ===== Calculation Tools =====


def calculate(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression.

    Args:
        expression: The mathematical expression to evaluate

    Returns:
        A dictionary containing the result
    """
    import math

    # Define safe math functions
    safe_dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "len": len,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        # Clean the expression
        expression = expression.strip()

        # Evaluate the expression in a safe environment
        result = eval(expression, {"__builtins__": {}}, safe_dict)

        return {"expression": expression, "result": result}
    except Exception as e:
        logger.error(f"Error calculating expression '{expression}': {str(e)}")
        return {"expression": expression, "error": str(e)}


# ===== Analysis Tools =====


def summarize_text(text: str, max_length: int = 200) -> Dict[str, Any]:
    """
    Summarize the given text.

    Args:
        text: The text to summarize
        max_length: Maximum length of the summary

    Returns:
        A dictionary containing the summary
    """
    # Implement a simple extractive summarization method
    # In a real implementation, this would use an ML model

    # Split text into sentences
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text)

    if len(sentences) <= 3:
        return {
            "original_length": len(text),
            "summary": text,
            "summary_length": len(text),
        }

    # Take first and last sentences, plus a middle one
    summary = " ".join([sentences[0], sentences[len(sentences) // 2], sentences[-1]])

    # Truncate if needed
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."

    return {
        "original_length": len(text),
        "summary": summary,
        "summary_length": len(summary),
    }


# Register all the tools with the function registry when this module is imported
def register_all_tools(registry):
    """
    Register all tools with the given function registry.

    Args:
        registry: The function registry to register tools with
    """
    # Search tools
    registry.register(name="search")(search)

    # Information tools
    registry.register(name="get_current_time")(get_current_time)
    registry.register(name="system_info")(system_info)

    # Calculation tools
    registry.register(name="calculate")(calculate)

    # Analysis tools
    registry.register(name="summarize_text")(summarize_text)

    logger.info(f"Registered {len(registry.get_all_schemas())} agent tools")
