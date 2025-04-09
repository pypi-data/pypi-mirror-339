"""
API Server for LlamaFind Ultimate

This module provides the RESTful API endpoints for searching and interacting
with the LlamaFind search platform.
"""

import asyncio
import logging
import os
import threading
import time
from datetime import datetime
from typing import Any, Dict

from flask import Flask, jsonify, request
from flask_cors import CORS
from llamafind.agents.agent import AgentFactory
from llamafind.mlx_compat import get_mlx_version, is_mlx_available, should_use_mlx
from llamafind.utils.es_integration import (
    connect_elasticsearch,
    create_indices,
    perform_search,
)

# Import internal modules
from llamafind.utils.query_expander import expand_query
from llamafind.utils.result_ranker import rank_results

# Import agent modules
from .agents.agent import AgentFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store agents and models
_agents = {}
_models = {}
_agent_lock = threading.Lock()


# Load configuration
def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = os.environ.get("LLAMAFIND_CONFIG", "config/config.yml")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.warning(f"Error loading config: {e}. Using default configuration.")
        return {}


CONFIG = load_config()
SERVER_CONFIG = CONFIG.get("server", {})


# Initialize Elasticsearch
def init_elasticsearch():
    """Initialize Elasticsearch connection and indices."""
    connected = connect_elasticsearch()
    if connected:
        logger.info("Connected to Elasticsearch")
        indices_status = create_indices()
        logger.info(f"Elasticsearch indices status: {indices_status}")
    else:
        logger.warning("Failed to connect to Elasticsearch")


# Initialize agents
def init_agents():
    """Initialize agent system."""
    # Check MLX availability for agents
    use_mlx = is_mlx_available() and should_use_mlx()

    try:
        # Create a default search agent
        with _agent_lock:
            _agents["search"] = AgentFactory.create_agent(
                agent_type="search",
                name="LlamaSearchAgent",
                description="Expert in finding information across the web using different search engines",
                use_mlx=use_mlx,
            )
            logger.info("Default search agent initialized")
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")


# API route handlers
@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    from llamafind import get_version

    mlx_status = {
        "available": is_mlx_available(),
        "enabled": should_use_mlx(),
        "version": get_mlx_version(),
    }

    agent_status = {
        "initialized": len(_agents) > 0,
        "count": len(_agents),
        "types": list(_agents.keys()),
    }

    return jsonify(
        {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "version": get_version(),
            "mlx": mlx_status,
            "agents": agent_status,
        }
    )


@app.route("/api/search", methods=["GET"])
def search():
    """
    Search endpoint.

    Query parameters:
        q: Search query
        n: Number of results (default: 10)
        expand: Whether to expand the query (default: true)
    """
    # Get query parameters
    query = request.args.get("q", "").strip()
    num_results = int(request.args.get("n", 10))
    expand_query_param = request.args.get("expand", "true").lower() in (
        "true",
        "1",
        "yes",
    )

    # Validate query
    if not query:
        return jsonify({"error": "Missing query parameter 'q'", "results": []}), 400

    # Log request
    logger.info(
        f"Search request: query='{query}', num_results={num_results}, expand={expand_query_param}"
    )

    try:
        # Start timer
        start_time = time.time()

        # Step 1: Expand query if requested
        original_query = query
        if expand_query_param:
            query = expand_query(query)
            logger.info(f"Expanded query: '{query}'")

        # Step 2: Perform search
        search_results = perform_search(query, size=num_results)

        # Step 3: Rank results
        ranked_results = rank_results(search_results, original_query)

        # End timer
        elapsed_time = time.time() - start_time

        # Log response
        logger.info(f"Search results: {len(ranked_results)} results in {elapsed_time:.2f}s")

        # Return response
        return jsonify(
            {
                "query": original_query,
                "expanded_query": query if expand_query_param else None,
                "num_results": len(ranked_results),
                "time_ms": int(elapsed_time * 1000),
                "results": ranked_results,
            }
        )

    except Exception as e:
        logger.error(f"Error processing search request: {e}")
        return (
            jsonify({"error": f"Error processing search request: {str(e)}", "results": []}),
            500,
        )


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for conversational search.

    Request JSON:
        message: User message
        context: Optional conversation context
    """
    # Get request data
    data = request.get_json()

    if not data:
        return (
            jsonify({"error": "Invalid request: missing JSON body", "response": None}),
            400,
        )

    # Get message
    message = data.get("message", "").strip()
    context = data.get("context", [])

    # Validate message
    if not message:
        return (
            jsonify({"error": "Missing required field 'message'", "response": None}),
            400,
        )

    # Log request
    logger.info(f"Chat request: message='{message}', context_length={len(context)}")

    try:
        # Process chat message
        # In a real implementation, this would use an LLM to generate a response
        # For now, we'll just echo back the message with a prefix

        # Generate a response
        response = f"I received your message: {message}"

        # Log response
        logger.info("Chat response generated")

        # Return response
        return jsonify({"response": response, "timestamp": datetime.now().isoformat()})

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return (
            jsonify({"error": f"Error processing chat request: {str(e)}", "response": None}),
            500,
        )


@app.route("/api/status", methods=["GET"])
def status():
    """Status endpoint with detailed system information."""
    # Get system information
    import platform

    import psutil
    from llamafind import get_version

    from .mlx_compat import (
        get_available_mlx_packages,
        get_mlx_device,
        get_mlx_version,
        is_mlx_available,
        should_use_mlx,
    )

    # For agents
    agent_info = {"count": len(_agents), "types": list(_agents.keys())}

    # Request statistics
    request_count = getattr(app, "_request_count", 0)
    app._request_count = request_count + 1

    # System stats
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return jsonify(
        {
            "operational": {
                "status": "online",
                "uptime": (time.time() - app.start_time if hasattr(app, "start_time") else 0),
                "version": get_version(),
                "request_count": request_count,
            },
            "system": {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": memory.total,
                "memory_available": memory.available,
                "memory_percent": memory.percent,
                "disk_total": disk.total,
                "disk_free": disk.free,
                "disk_percent": disk.percent,
            },
            "mlx": {
                "available": is_mlx_available(),
                "enabled": should_use_mlx(),
                "version": get_mlx_version(),
                "device": get_mlx_device(),
                "packages": get_available_mlx_packages(),
            },
            "agents": agent_info,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/agent/message", methods=["POST"])
async def agent_message():
    """Process a message with an agent."""
    try:
        # Parse request body
        data = request.json

        if not data:
            return (
                jsonify(
                    {
                        "error": "Missing request body",
                        "message": "Please provide a JSON request body",
                    }
                ),
                400,
            )

        message = data.get("message", "")
        agent_id = data.get("agent_id", "search")  # Default to search agent

        if not message:
            return (
                jsonify(
                    {
                        "error": "Missing message",
                        "message": "Please provide a message in the request body",
                    }
                ),
                400,
            )

        # Log agent request
        logger.info(f"Agent request: agent='{agent_id}', message='{message}'")

        # Check if agent exists
        with _agent_lock:
            if agent_id not in _agents:
                return (
                    jsonify(
                        {
                            "error": "Agent not found",
                            "message": f"Agent '{agent_id}' does not exist",
                        }
                    ),
                    404,
                )

            agent = _agents[agent_id]

        # Process message with agent
        response = await agent.process_message(message)

        # Return response
        return jsonify(
            {
                "agent_id": agent_id,
                "response": response,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error processing agent message: {e}")
        return jsonify({"error": "Agent processing failed", "message": str(e)}), 500


@app.route("/api/agent/task", methods=["POST"])
def create_agent_task():
    """Create a new task for an agent."""
    try:
        # Parse request body
        data = request.json

        if not data:
            return (
                jsonify(
                    {
                        "error": "Missing request body",
                        "message": "Please provide a JSON request body",
                    }
                ),
                400,
            )

        description = data.get("description", "")
        agent_id = data.get("agent_id", "search")  # Default to search agent

        if not description:
            return (
                jsonify(
                    {
                        "error": "Missing task description",
                        "message": "Please provide a task description in the request body",
                    }
                ),
                400,
            )

        # Log task creation
        logger.info(f"Task creation: agent='{agent_id}', description='{description}'")

        # Check if agent exists
        with _agent_lock:
            if agent_id not in _agents:
                return (
                    jsonify(
                        {
                            "error": "Agent not found",
                            "message": f"Agent '{agent_id}' does not exist",
                        }
                    ),
                    404,
                )

            agent = _agents[agent_id]

        # Create task
        task_id = agent.create_task(description)

        # Start task execution in background
        def execute_task():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(agent.run_task(task_id))
            finally:
                loop.close()

        threading.Thread(target=execute_task).start()

        # Return task ID
        return jsonify(
            {
                "agent_id": agent_id,
                "task_id": task_id,
                "status": "created",
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error creating agent task: {e}")
        return jsonify({"error": "Task creation failed", "message": str(e)}), 500


@app.route("/api/agent/task/<task_id>", methods=["GET"])
def get_agent_task(task_id):
    """Get information about a task."""
    try:
        agent_id = request.args.get("agent_id", "search")  # Default to search agent

        # Check if agent exists
        with _agent_lock:
            if agent_id not in _agents:
                return (
                    jsonify(
                        {
                            "error": "Agent not found",
                            "message": f"Agent '{agent_id}' does not exist",
                        }
                    ),
                    404,
                )

            agent = _agents[agent_id]

        # Get task information
        task_info = agent.get_task(task_id)

        if not task_info:
            return (
                jsonify(
                    {
                        "error": "Task not found",
                        "message": f"Task '{task_id}' does not exist for agent '{agent_id}'",
                    }
                ),
                404,
            )

        # Return task information
        return jsonify({"agent_id": agent_id, "task_id": task_id, "task": task_info})

    except Exception as e:
        logger.error(f"Error getting agent task: {e}")
        return jsonify({"error": "Task retrieval failed", "message": str(e)}), 500


@app.route("/api/agent/list", methods=["GET"])
def list_agents():
    """List available agents."""
    try:
        agents_info = []

        # Get agent information
        with _agent_lock:
            for agent_id, agent in _agents.items():
                agents_info.append(
                    {
                        "id": agent_id,
                        "name": agent.name,
                        "description": agent.description,
                        "capabilities": agent.get_capabilities(),
                    }
                )

        # Return agent information
        return jsonify({"agents": agents_info, "count": len(agents_info)})

    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return jsonify({"error": "Agent listing failed", "message": str(e)}), 500


@app.route("/api/agents", methods=["GET"])
def list_agents():
    """List available agents."""
    try:
        # Get available agent types
        agent_types = ["search", "chat"]

        # Return agent types
        return jsonify(
            {
                "status": "success",
                "agents": [
                    {
                        "type": "search",
                        "name": "SearchAgent",
                        "description": "Specialized in search operations using various search engines",
                        "capabilities": [
                            "search",
                            "get_current_time",
                            "system_info",
                            "calculate",
                            "summarize_text",
                        ],
                    },
                    {
                        "type": "chat",
                        "name": "ChatAgent",
                        "description": "General purpose conversational agent",
                        "capabilities": [
                            "get_current_time",
                            "system_info",
                            "calculate",
                            "summarize_text",
                        ],
                    },
                ],
            }
        )
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/agents/<agent_type>/tasks", methods=["POST"])
def create_agent_task(agent_type):
    """Create a new task for an agent."""
    try:
        # Get request data
        data = request.json
        description = data.get("description", "")

        if not description:
            return (
                jsonify({"status": "error", "message": "Task description is required"}),
                400,
            )

        # Create agent
        agent = AgentFactory.create_agent(
            agent_type=agent_type, use_mlx=config.get("use_mlx", True)
        )

        # Create task
        task_id = agent.create_task(description)

        # Return task ID
        return jsonify({"status": "success", "task_id": task_id, "agent_type": agent_type})
    except Exception as e:
        logger.error(f"Error creating agent task: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/agents/<agent_type>/tasks/<task_id>", methods=["GET"])
def get_agent_task(agent_type, task_id):
    """Get the status and result of an agent task."""
    try:
        # Create agent
        agent = AgentFactory.create_agent(
            agent_type=agent_type, use_mlx=config.get("use_mlx", True)
        )

        # Get task
        task = agent.get_task(task_id)

        if not task:
            return (
                jsonify({"status": "error", "message": f"Task {task_id} not found"}),
                404,
            )

        # Return task
        return jsonify({"status": "success", "task": task})
    except Exception as e:
        logger.error(f"Error getting agent task: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/agents/<agent_type>/tasks/<task_id>/run", methods=["POST"])
async def run_agent_task(agent_type, task_id):
    """Run an agent task."""
    try:
        # Create agent
        agent = AgentFactory.create_agent(
            agent_type=agent_type, use_mlx=config.get("use_mlx", True)
        )

        # Run task
        result = await agent.run_task(task_id)

        # Return result
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        logger.error(f"Error running agent task: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/agents/<agent_type>/message", methods=["POST"])
async def send_agent_message(agent_type):
    """Send a message to an agent."""
    try:
        # Get request data
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"status": "error", "message": "Message is required"}), 400

        # Create agent
        agent = AgentFactory.create_agent(
            agent_type=agent_type, use_mlx=config.get("use_mlx", True)
        )

        # Process message
        response = await agent.process_message(message)

        # Return response
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        logger.error(f"Error processing agent message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Start the server
def run_server(host: str = None, port: int = None, debug: bool = None):
    """
    Run the Flask server.

    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Whether to run in debug mode
    """
    # Get settings from config or environment variables
    host = host or os.environ.get("LLAMAFIND_HOST", SERVER_CONFIG.get("host", "0.0.0.0"))
    port = port or int(os.environ.get("LLAMAFIND_PORT", SERVER_CONFIG.get("port", 8080)))
    debug = debug if debug is not None else SERVER_CONFIG.get("debug", False)

    # Initialize components
    init_elasticsearch()
    init_agents()

    # Record start time for uptime tracking
    app.start_time = time.time()

    # Log server start
    logger.info(f"Starting LlamaFind API server at http://{host}:{port}")
    logger.info(f"MLX: {'enabled' if should_use_mlx() else 'disabled'}")

    # Run the Flask app
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server()
