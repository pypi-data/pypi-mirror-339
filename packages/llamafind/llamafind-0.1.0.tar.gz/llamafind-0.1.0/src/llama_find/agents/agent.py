"""
LlamaFind Agent Framework

This module provides a framework for creating autonomous agents with LLaMA models and MLX.
The agents can use function calling capabilities to interact with various systems.
"""

import logging
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field

from .function_calling import LlamaFunctionCaller
from .tools import register_all_tools

logger = logging.getLogger(__name__)


class AgentMemory:
    """Memory store for agent interactions and context."""

    def __init__(self, max_items: int = 10):
        """
        Initialize agent memory.

        Args:
            max_items: Maximum number of interactions to remember
        """
        self.interactions: List[Dict[str, Any]] = []
        self.max_items = max_items
        self.metadata: Dict[str, Any] = {}

    def add_interaction(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add an interaction to memory.

        Args:
            role: Role of the speaker (user, assistant, system, function)
            content: Content of the message
            metadata: Optional metadata about the interaction
        """
        interaction = {"role": role, "content": content, "timestamp": time.time()}

        if metadata:
            interaction["metadata"] = metadata

        self.interactions.append(interaction)

        # Trim if exceeding max items
        if len(self.interactions) > self.max_items:
            self.interactions = self.interactions[-self.max_items :]

    def get_conversation_history(self, as_string: bool = False) -> Union[List[Dict[str, Any]], str]:
        """
        Get the conversation history.

        Args:
            as_string: Whether to return as a formatted string

        Returns:
            Conversation history as a list or string
        """
        if not as_string:
            return self.interactions

        # Format as string
        result = []
        for interaction in self.interactions:
            if interaction["role"] == "system":
                result.append(f"System: {interaction['content']}")
            elif interaction["role"] == "user":
                result.append(f"User: {interaction['content']}")
            elif interaction["role"] == "assistant":
                result.append(f"Assistant: {interaction['content']}")
            elif interaction["role"] == "function":
                result.append(
                    f"Function ({interaction.get('metadata', {}).get('name', 'unknown')}): {interaction['content']}"
                )

        return "\n".join(result)

    def clear(self):
        """Clear all interactions from memory."""
        self.interactions = []
        self.metadata = {}


class AgentTask(BaseModel):
    """A task for the agent to perform."""

    id: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class Agent:
    """An autonomous agent powered by LLaMA and MLX."""

    def __init__(
        self,
        name: str,
        description: str,
        model_path: Optional[str] = None,
        use_mlx: bool = True,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize an agent.

        Args:
            name: Agent name
            description: Agent description
            model_path: Path to LLaMA model
            use_mlx: Whether to use MLX acceleration
            system_prompt: Optional system prompt to override default
        """
        self.name = name
        self.description = description
        self.memory = AgentMemory()
        self.tasks: Dict[str, AgentTask] = {}
        self.capabilities: Set[str] = set()

        # Initialize function caller
        self.function_caller = LlamaFunctionCaller(model_path=model_path, use_mlx=use_mlx)

        # Register tools with function caller
        try:
            register_all_tools(self.function_caller.registry)
        except Exception as e:
            logger.error(f"Failed to register agent tools: {e}")

        # Set default system prompt if not provided
        self.system_prompt = (
            system_prompt
            or f"""You are {name}, an AI assistant with these capabilities:
- {description}
- You can use functions when appropriate to complete tasks
- You should respond directly when a function isn't needed
- You prioritize being helpful, accurate, and efficient"""
        )

        # Add system prompt to memory
        self.memory.add_interaction("system", self.system_prompt)

        logger.info(f"Agent '{name}' initialized")

    def register_capability(self, name: str, func: Callable):
        """
        Register a capability (function) that the agent can use.

        Args:
            name: Capability name
            func: Function to register
        """
        # Register function with the function caller
        self.function_caller.registry.register(name=name)(func)

        # Add to agent's capabilities
        self.capabilities.add(name)
        logger.info(f"Agent '{self.name}' registered capability: {name}")

    def create_task(self, description: str) -> str:
        """
        Create a new task for the agent.

        Args:
            description: Task description

        Returns:
            Task ID
        """
        import uuid

        task_id = str(uuid.uuid4())

        task = AgentTask(id=task_id, description=description)

        self.tasks[task_id] = task
        logger.info(f"Created task {task_id} for agent '{self.name}': {description}")

        return task_id

    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message and generate a response.

        Args:
            message: User message

        Returns:
            Dict containing response and any function calls
        """
        # Add user message to memory
        self.memory.add_interaction("user", message)

        # Format conversation history for context
        conversation = self.memory.get_conversation_history(as_string=True)

        # Process with LLaMA model
        response = await self.function_caller.run(message, execute_functions=True)

        # Add assistant response to memory
        if response["type"] == "function_call":
            self.memory.add_interaction(
                "assistant",
                f"I'll help by using the {response['function']} function.",
                {"function_call": True, "function": response["function"]},
            )

            # Add function result to memory if available
            if "function_output" in response:
                self.memory.add_interaction(
                    "function",
                    str(response["function_output"]),
                    {"name": response["function"]},
                )
        else:
            self.memory.add_interaction("assistant", response["content"])

        return response

    async def run_task(self, task_id: str) -> Dict[str, Any]:
        """
        Run a specific task.

        Args:
            task_id: ID of the task to run

        Returns:
            Task result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        task.status = "in_progress"
        task.updated_at = time.time()

        try:
            # Clear memory for new task
            self.memory.clear()
            self.memory.add_interaction("system", self.system_prompt)

            # Add task description as user message
            response = await self.process_message(task.description)

            # Update task with result
            task.result = response
            task.status = "completed"
            task.updated_at = time.time()

            return {"task_id": task_id, "status": "completed", "result": response}

        except Exception as e:
            logger.error(f"Error running task {task_id}: {e}")
            task.status = "failed"
            task.error = str(e)
            task.updated_at = time.time()

            return {"task_id": task_id, "status": "failed", "error": str(e)}

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a task.

        Args:
            task_id: ID of the task

        Returns:
            Task information or None if not found
        """
        if task_id not in self.tasks:
            return None

        task = self.tasks[task_id]
        return task.dict()

    def get_capabilities(self) -> List[str]:
        """Get the list of capabilities (functions) the agent can use."""
        return list(self.capabilities)


# Create a search agent class that extends the base Agent
class SearchAgent(Agent):
    """Specialized agent for search operations."""

    def __init__(
        self,
        name: str = "SearchAgent",
        description: str = "Specialized in search operations using various search engines",
        model_path: Optional[str] = None,
        use_mlx: bool = True,
        system_prompt: Optional[str] = None,
    ):
        if system_prompt is None:
            system_prompt = """You are a helpful search agent. Your primary role is to help users find 
            information using various search engines and tools. When asked a question, think about 
            which search engine or capability would be most appropriate, and use it to provide
            the most accurate and relevant information."""

        super().__init__(name, description, model_path, use_mlx, system_prompt)

        try:
            # Register search capabilities
            from llamafind.search import search

            self.register_capability("search", search, "Search the web")

            # Register common capabilities
            self.register_capability(
                "get_current_time", self.get_current_time, "Gets the current time"
            )
            self.register_capability(
                "system_info",
                self.get_system_info,
                "Returns information about the system",
            )
            self.register_capability("calculate", self.calculate, "Perform a calculation")
            self.register_capability(
                "summarize_text", self.summarize_text, "Summarize a piece of text"
            )
        except Exception as e:
            logger.error(f"Failed to register search capabilities: {e}")

    async def get_current_time(self) -> Dict[str, Any]:
        """Returns the current time."""
        now = datetime.now()
        return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}

    async def get_system_info(self) -> Dict[str, Any]:
        """Returns basic information about the system."""
        import platform

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
        }

    async def calculate(self, expression: str) -> Dict[str, Any]:
        """Perform a simple calculation."""
        try:
            # Use a safe eval
            import ast
            import operator

            # Define safe operators
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.BitXor: operator.xor,
                ast.USub: operator.neg,
            }

            def eval_expr(expr):
                return eval_(ast.parse(expr, mode="eval").body)

            def eval_(node):
                if isinstance(node, ast.Constant):
                    return node.value
                elif isinstance(node, ast.BinOp):
                    return operators[type(node.op)](eval_(node.left), eval_(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return operators[type(node.op)](eval_(node.operand))
                else:
                    raise TypeError(f"Unsupported operation: {node}")

            result = eval_expr(expression)
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"expression": expression, "error": str(e)}

    async def summarize_text(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Simple text summarization by extracting key sentences."""
        # Very basic summarization - in a real system, this would use more sophisticated methods
        sentences = text.split(".")

        if len(sentences) <= 3:
            return {"summary": text, "original_length": len(text)}

        # Take first, middle and last sentence as a very basic summary
        summary = ". ".join(
            [
                sentences[0].strip(),
                sentences[len(sentences) // 2].strip(),
                sentences[-2].strip() if len(sentences) > 2 else "",
            ]
        )

        # Truncate if still too long
        if len(summary) > max_length and len(summary) > 20:
            summary = summary[: max_length - 3] + "..."

        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
        }


# Add ChatAgent after SearchAgent
class ChatAgent(Agent):
    """Specialized agent for chat and conversational interactions."""

    def __init__(
        self,
        name: str = "ChatAgent",
        description: str = "General purpose conversational agent",
        model_path: Optional[str] = None,
        use_mlx: bool = True,
        system_prompt: Optional[str] = None,
    ):
        if system_prompt is None:
            system_prompt = """You are a helpful, accurate, and friendly conversational AI assistant.
            Answer user questions truthfully based on the information available to you.
            If you don't know the answer, admit it and avoid making up information.
            Be helpful but concise in your responses."""

        super().__init__(name, description, model_path, use_mlx, system_prompt)

        # Register chat-specific capabilities
        self.register_capability("get_current_time", self.get_current_time, "Gets the current time")
        self.register_capability(
            "system_info", self.get_system_info, "Returns information about the system"
        )
        self.register_capability("calculate", self.calculate, "Perform a calculation")
        self.register_capability("summarize_text", self.summarize_text, "Summarize a piece of text")

    async def get_current_time(self) -> Dict[str, Any]:
        """Returns the current time."""
        now = datetime.now()
        return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}

    async def get_system_info(self) -> Dict[str, Any]:
        """Returns basic information about the system."""
        import platform

        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
        }

    async def calculate(self, expression: str) -> Dict[str, Any]:
        """Perform a simple calculation."""
        try:
            # Use a safe eval
            import ast
            import operator

            # Define safe operators
            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.BitXor: operator.xor,
                ast.USub: operator.neg,
            }

            def eval_expr(expr):
                return eval_(ast.parse(expr, mode="eval").body)

            def eval_(node):
                if isinstance(node, ast.Constant):
                    return node.value
                elif isinstance(node, ast.BinOp):
                    return operators[type(node.op)](eval_(node.left), eval_(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return operators[type(node.op)](eval_(node.operand))
                else:
                    raise TypeError(f"Unsupported operation: {node}")

            result = eval_expr(expression)
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"expression": expression, "error": str(e)}

    async def summarize_text(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Simple text summarization by extracting key sentences."""
        # Very basic summarization - in a real system, this would use more sophisticated methods
        sentences = text.split(".")

        if len(sentences) <= 3:
            return {"summary": text, "original_length": len(text)}

        # Take first, middle and last sentence as a very basic summary
        summary = ". ".join(
            [
                sentences[0].strip(),
                sentences[len(sentences) // 2].strip(),
                sentences[-2].strip() if len(sentences) > 2 else "",
            ]
        )

        # Truncate if still too long
        if len(summary) > max_length and len(summary) > 20:
            summary = summary[: max_length - 3] + "..."

        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
        }


# Create an agent factory for easier creation of agents
class AgentFactory:
    """Factory for creating different types of agents."""

    @staticmethod
    def create_agent(
        agent_type: str,
        model_path: Optional[str] = None,
        system_prompt: Optional[str] = None,
        use_mlx: bool = True,
    ) -> Agent:
        """Create an agent of the specified type.

        Args:
            agent_type: The type of agent to create ('search' or 'chat')
            model_path: Path to the model to use for the agent
            system_prompt: System prompt to use for the agent
            use_mlx: Whether to use MLX for inference

        Returns:
            An instance of the specified agent type
        """
        if agent_type.lower() == "search":
            return SearchAgent(model_path=model_path, system_prompt=system_prompt, use_mlx=use_mlx)
        elif agent_type.lower() == "chat":
            return ChatAgent(model_path=model_path, system_prompt=system_prompt, use_mlx=use_mlx)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
