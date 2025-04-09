"""
Function Calling Implementation for MLX LLaMA Models

This module implements function calling capabilities for LLaMA models using MLX acceleration.
"""

import inspect
import json
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

# Check for MLX and LLaMA compatibility
from ..mlx_compat import is_mlx_available, should_use_mlx

logger = logging.getLogger(__name__)

# Initialize MLX components if available
MLX_AVAILABLE = is_mlx_available() and should_use_mlx()

if MLX_AVAILABLE:
    try:
        import mlx
        import mlx.core as mx

        logger.info("MLX is available for function calling acceleration")
    except ImportError:
        logger.warning("MLX is marked as available but cannot be imported")
        MLX_AVAILABLE = False
else:
    logger.warning("MLX is not available, using CPU fallback for function calling")


class FunctionRegistry:
    """Registry for functions that can be called by LLaMA models."""

    def __init__(self):
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.function_schemas: Dict[str, Dict[str, Any]] = {}
        logger.info("Function registry initialized")

    def register(self, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to register a function for agent use."""

        def decorator(func):
            nonlocal name
            func_name = name or func.__name__
            func_desc = description or inspect.getdoc(func) or "No description available"

            # Get function signature
            sig = inspect.signature(func)
            parameters = {}

            for param_name, param in sig.parameters.items():
                # Skip self for methods
                if param_name == "self":
                    continue

                param_type = Any
                if param.annotation != inspect.Parameter.empty:
                    param_type = param.annotation

                param_default = None
                param_required = True
                if param.default != inspect.Parameter.empty:
                    param_default = param.default
                    param_required = False

                parameters[param_name] = {
                    "type": self._get_type_str(param_type),
                    "description": f"Parameter {param_name}",
                    "required": param_required,
                }

                if param_default is not None:
                    parameters[param_name]["default"] = param_default

            # Create function schema
            schema = {
                "name": func_name,
                "description": func_desc,
                "parameters": parameters,
                "return_type": (
                    self._get_type_str(sig.return_annotation)
                    if sig.return_annotation != inspect.Signature.empty
                    else "Any"
                ),
            }

            self.functions[func_name] = func
            self.function_schemas[func_name] = schema
            logger.debug(f"Registered function: {func_name}")

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        # Handle case where decorator is used without parentheses
        if callable(name):
            func = name
            name = None
            return decorator(func)

        return decorator

    def _get_type_str(self, type_hint) -> str:
        """Convert Python type hints to string representations for JSON schema."""
        import typing

        if type_hint is Any or type_hint == typing.Any:
            return "any"
        elif type_hint is str or type_hint == str:
            return "string"
        elif type_hint is int or type_hint == int:
            return "integer"
        elif type_hint is float or type_hint == float:
            return "number"
        elif type_hint is bool or type_hint == bool:
            return "boolean"
        elif (
            type_hint is list
            or type_hint == list
            or hasattr(type_hint, "__origin__")
            and type_hint.__origin__ is list
        ):
            return "array"
        elif (
            type_hint is dict
            or type_hint == dict
            or hasattr(type_hint, "__origin__")
            and type_hint.__origin__ is dict
        ):
            return "object"
        else:
            return "any"

    def get_function(self, name: str) -> Optional[Callable]:
        """Get a registered function by name."""
        return self.functions.get(name)

    def get_all_functions(self) -> Dict[str, Callable]:
        """Get all registered functions."""
        return self.functions

    def get_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a registered function."""
        return self.function_schemas.get(name)

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all registered functions."""
        return list(self.function_schemas.values())

    def call_function(self, name: str, args: Dict[str, Any] = None) -> Any:
        """
        Call a registered function with the provided arguments.

        Args:
            name: The name of the function to call
            args: A dictionary of arguments to pass to the function

        Returns:
            The result of the function call
        """
        func = self.get_function(name)
        if not func:
            raise ValueError(f"Function {name} not found in registry")

        try:
            if args is None:
                args = {}
            return func(**args)
        except Exception as e:
            logger.error(f"Error calling function {name}: {e}")
            raise


class LlamaFunctionCaller:
    """Handler for function calling with LLaMA models."""

    def __init__(self, model_path: Optional[str] = None, use_mlx: bool = True):
        """
        Initialize the function caller with a LLaMA model.

        Args:
            model_path: Path to the LLaMA model
            use_mlx: Whether to use MLX acceleration
        """
        self.registry = FunctionRegistry()
        self.use_mlx = use_mlx and MLX_AVAILABLE
        self.model = None
        self.tokenizer = None

        # Auto-load model if path provided
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path: str) -> bool:
        """
        Load a LLaMA model for function calling.

        Args:
            model_path: Path to the LLaMA model

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_mlx:
                logger.info(f"Loading LLaMA model with MLX acceleration: {model_path}")
                import mlx_lm
                from mlx_lm.utils import get_model_path

                # Process model path
                model_dir = get_model_path(model_path)
                self.model, self.tokenizer = mlx_lm.load(model_dir)
                logger.info(f"Successfully loaded MLX LLaMA model from {model_path}")
            else:
                logger.info(f"Loading LLaMA model without MLX acceleration: {model_path}")
                # Use a CPU fallback like transformers
                from transformers import AutoModelForCausalLM, AutoTokenizer

                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path, device_map="auto", load_in_4bit=True
                )
                logger.info(f"Successfully loaded CPU LLaMA model from {model_path}")

            return True
        except Exception as e:
            logger.error(f"Error loading LLaMA model: {e}")
            return False

    def register_function(self, func=None, *, name=None, description=None):
        """Register a function with the registry."""
        return (
            self.registry.register(name=name, description=description)(func)
            if func
            else self.registry.register(name=name, description=description)
        )

    async def _process_with_mlx(
        self, prompt: str, functions: List[Dict[str, Any]], system_prompt: str = None
    ) -> Dict[str, Any]:
        """Process a prompt with MLX and generate function calls."""
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model first.")

        # Prepare prompt with system instructions and functions
        system_message = system_prompt or "You are a helpful assistant that can call functions."
        function_descriptions = json.dumps(functions, indent=2)

        full_prompt = f"""
{system_message}

Available functions:
{function_descriptions}

User: {prompt}
Assistant:"""

        # Generate response with MLX
        import mlx_lm.utils as utils

        tokens = []
        for token, _ in utils.generate(
            self.model,
            self.tokenizer,
            prompt=full_prompt,
            max_tokens=512,
            temperature=0.1,  # Lower temp for more deterministic function calls
        ):
            tokens.append(token)

        response = "".join(tokens)

        # Parse response to extract function calls
        try:
            # Try to find and parse JSON function call pattern
            import re

            function_pattern = r"```json\s*({[^`]*})\s*```"
            match = re.search(function_pattern, response)

            if match:
                function_json = match.group(1)
                function_data = json.loads(function_json)
                return function_data

            # If no JSON block found, try to parse the whole response as JSON
            try:
                return self._parse_json_response(response)
            except:
                # If all parsing fails, return the raw response
                return {"content": response.strip(), "functionCalls": []}
        except Exception as e:
            logger.error(f"Error parsing function call response: {e}")
            return {"content": response.strip(), "functionCalls": []}

    async def _process_with_transformers(
        self, prompt: str, functions: List[Dict[str, Any]], system_prompt: str = None
    ) -> Dict[str, Any]:
        """Process a prompt with Transformers and generate function calls."""
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model first.")

        # Prepare prompt with system instructions and functions
        system_message = system_prompt or "You are a helpful assistant that can call functions."
        function_descriptions = json.dumps(functions, indent=2)

        full_prompt = f"""
{system_message}

Available functions:
{function_descriptions}

User: {prompt}
Assistant:"""

        # Generate response using transformers
        import threading

        from transformers import TextIteratorStreamer

        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        generation_kwargs = {
            "input_ids": inputs.input_ids,
            "streamer": streamer,
            "max_new_tokens": 512,
            "temperature": 0.1,  # Lower temp for more deterministic function calls
            "do_sample": True,
        }

        # Start generation in a separate thread
        thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        # Collect the generated text
        response = ""
        for text in streamer:
            response += text

        thread.join()

        # Parse response to extract function calls
        try:
            # Try to find and parse JSON function call pattern
            import re

            function_pattern = r"```json\s*({[^`]*})\s*```"
            match = re.search(function_pattern, response)

            if match:
                function_json = match.group(1)
                function_data = json.loads(function_json)
                return function_data

            # If no JSON block found, try to parse the whole response as JSON
            try:
                return self._parse_json_response(response)
            except:
                # If all parsing fails, return the raw response
                return {"content": response.strip(), "functionCalls": []}
        except Exception as e:
            logger.error(f"Error parsing function call response: {e}")
            return {"content": response.strip(), "functionCalls": []}

    async def process(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Process a prompt and generate function calls if appropriate.

        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt to use

        Returns:
            Dict with results including function calls if detected
        """
        if not self.model or not self.tokenizer:
            raise ValueError("Model not loaded. Call load_model first.")

        # Get all function schemas
        functions = self.registry.get_all_schemas()

        # Process with appropriate backend
        if self.use_mlx:
            return await self._process_with_mlx(prompt, functions, system_prompt)
        else:
            return await self._process_with_transformers(prompt, functions, system_prompt)

    async def run(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Run the full function calling pipeline including execution.

        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt to use

        Returns:
            Dict with results and function outputs
        """
        # Process prompt to detect function calls
        result = await self.process(prompt=prompt, system_prompt=system_prompt)

        # If function calls detected, execute them
        if "functionCalls" in result and result["functionCalls"]:
            function_results = []

            for func_call in result["functionCalls"]:
                try:
                    # Get function name and arguments
                    function_name = func_call["name"]
                    arguments = func_call["arguments"]

                    # Call the function
                    function_output = self.registry.call_function(function_name, args=arguments)

                    # Add function output to result
                    function_results.append({"name": function_name, "result": function_output})
                except Exception as e:
                    logger.error(f"Error executing function {function_name}: {e}")
                    function_results.append({"name": function_name, "error": str(e)})

            # Add function results to the response
            result["functionResults"] = function_results

        return result

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        Parse a JSON response from the model.

        Args:
            text: The text to parse

        Returns:
            Parsed JSON as a dictionary
        """
        # Try to find JSON in the response
        import re

        json_pattern = r"{.*}"
        match = re.search(json_pattern, text, re.DOTALL)

        if match:
            try:
                json_str = match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # If no valid JSON found, return a basic response
        return {"content": text.strip(), "functionCalls": []}


# Create global instances for easier usage
function_registry = FunctionRegistry()
register_function = function_registry.register
