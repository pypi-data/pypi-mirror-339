"""
Web Server Entry Point for LlamaFind Ultimate

This module serves as the entry point for starting the LlamaFind API server.
It parses command-line arguments and initializes the server.
"""

import argparse
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import API module
try:
    from llamafind.api import run_server
except ImportError as e:
    logger.error(f"Failed to import LlamaFind API module: {e}")
    sys.exit(1)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="LlamaFind API Server")

    parser.add_argument(
        "--host",
        type=str,
        default=os.environ.get("LLAMAFIND_HOST", "0.0.0.0"),
        help="Host address to bind to (default: 0.0.0.0)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("LLAMAFIND_PORT", 8080)),
        help="Port to bind to (default: 8080)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.environ.get("LLAMAFIND_DEBUG", "").lower() in ("true", "1", "yes"),
        help="Run in debug mode",
    )

    parser.add_argument("--no-mlx", action="store_true", help="Disable MLX acceleration")

    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()

    # Set MLX environment variable if --no-mlx is specified
    if args.no_mlx:
        os.environ["MLX_ENABLED"] = "false"
        logger.info("MLX acceleration disabled via command line argument")

    # Log startup information
    logger.info(f"Starting LlamaFind API server on {args.host}:{args.port}")

    try:
        # Run the server
        run_server(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
