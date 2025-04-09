"""
MLX Compatibility Module for LlamaFind Ultimate

This module provides a consistent interface for MLX functionality with graceful fallbacks
when MLX is not available or disabled. It dynamically detects hardware capabilities and
optimizes performance on Apple Silicon.
"""

import importlib.util
import logging
import os
import sys
from typing import Any, Dict, Optional

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load configuration
def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "config",
        "config.yml",
    )
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.warning(f"Error loading config: {e}. Using defaults.")
        return {"mlx": {"enabled": True, "fallback_to_cpu": True}}


CONFIG = load_config()
MLX_CONFIG = CONFIG.get("mlx", {})

# Check if MLX should be disabled via environment variable (overrides config)
DISABLE_MLX = os.environ.get("MLX_ENABLED", "").lower() in (
    "false",
    "0",
    "no",
) or not MLX_CONFIG.get("enabled", True)

# Detect platform
IS_MACOS = sys.platform == "darwin"
IS_APPLE_SILICON = False

if IS_MACOS:
    try:
        import platform

        cpu_info = platform.processor()
        IS_APPLE_SILICON = "Apple" in cpu_info
        if IS_APPLE_SILICON:
            logger.info(f"Detected Apple Silicon: {cpu_info}")
        else:
            logger.info(f"Detected non-Apple Silicon Mac: {cpu_info}")
    except Exception as e:
        logger.warning(f"Error detecting CPU architecture: {e}")

# Initialize MLX state variables
HAS_MLX = False
MLX_VERSION = None
MLX_AVAILABLE_DEVICES = ["cpu"]
MLX_DEFAULT_DEVICE = "cpu"
MLX_AVAILABLE_PACKAGES = {}


def is_mlx_available() -> bool:
    """Check if MLX is available."""
    return HAS_MLX


def should_use_mlx() -> bool:
    """Check if MLX should be used (available and not disabled)."""
    return HAS_MLX and not DISABLE_MLX


def get_mlx_version() -> Optional[str]:
    """Get the installed MLX version."""
    return MLX_VERSION


def get_mlx_device() -> str:
    """Get the current MLX device."""
    return MLX_DEFAULT_DEVICE


def get_available_mlx_packages() -> Dict[str, bool]:
    """Get dictionary of available MLX packages."""
    return MLX_AVAILABLE_PACKAGES.copy()


# Attempt to import MLX and related packages if not disabled
if not DISABLE_MLX:
    try:
        # Try to import core MLX
        import mlx.core
        import mlx.nn

        HAS_MLX = True
        MLX_VERSION = getattr(mlx, "__version__", "unknown")
        logger.info(f"MLX is available (version: {MLX_VERSION})")

        # Check available devices
        MLX_DEFAULT_DEVICE = mlx.core.default_device()
        if hasattr(mlx.core, "gpu_is_available") and mlx.core.gpu_is_available():
            MLX_AVAILABLE_DEVICES = ["cpu", "gpu"]
            logger.info("MLX GPU acceleration is available")
        else:
            MLX_AVAILABLE_DEVICES = ["cpu"]
            logger.info("MLX is using CPU only")

        # Check for additional MLX packages
        mlx_packages = ["mlx-embeddings", "mlx-textgen", "mlx-whisper", "mlx-hub"]

        for package in mlx_packages:
            package_available = importlib.util.find_spec(package.replace("-", "_")) is not None
            MLX_AVAILABLE_PACKAGES[package] = package_available
            if package_available:
                logger.info(f"MLX package available: {package}")

    except ImportError as e:
        HAS_MLX = False
        logger.warning(f"MLX is not available: {e}")

        if IS_APPLE_SILICON and MLX_CONFIG.get("fallback_to_cpu", True):
            logger.warning(
                "Apple Silicon detected but MLX not available. Consider installing MLX for better performance."
            )

        # Create stub modules if requested in config (for development/testing)
        if MLX_CONFIG.get("create_stubs", False):
            logger.info("Creating MLX stub modules")

            class MLXStub:
                """Stub class for MLX functionality."""

                def __getattr__(self, name):
                    return self

                def __call__(self, *args, **kwargs):
                    return self

            # Create and register stub modules
            mlx_stub = MLXStub()
            sys.modules["mlx"] = mlx_stub
            sys.modules["mlx.core"] = mlx_stub
            sys.modules["mlx.nn"] = mlx_stub

            for package in ["mlx_embeddings", "mlx_textgen", "mlx_whisper", "mlx_hub"]:
                sys.modules[package] = mlx_stub

            logger.info("MLX stub modules created")

# Log final MLX status
if HAS_MLX and not DISABLE_MLX:
    logger.info(f"MLX is active: Version {MLX_VERSION}, Device: {MLX_DEFAULT_DEVICE}")
else:
    logger.info("MLX is inactive: Using fallback implementations")

# Export key functionality
__all__ = [
    "is_mlx_available",
    "should_use_mlx",
    "get_mlx_version",
    "get_mlx_device",
    "get_available_mlx_packages",
    "HAS_MLX",
    "MLX_VERSION",
    "MLX_AVAILABLE_DEVICES",
    "MLX_DEFAULT_DEVICE",
]
