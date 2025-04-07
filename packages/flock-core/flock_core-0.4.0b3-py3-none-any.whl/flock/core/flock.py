# src/flock/core/flock.py
"""High-level orchestrator for creating and executing agents."""

from __future__ import annotations  # Ensure forward references work

import asyncio
import os
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, TypeVar

from box import Box
from opentelemetry import trace
from opentelemetry.baggage import get_baggage, set_baggage

# Pydantic and OpenTelemetry
from pydantic import BaseModel, Field  # Using Pydantic directly now

# Flock core components & utilities
from flock.config import TELEMETRY
from flock.core.context.context import FlockContext
from flock.core.context.context_manager import initialize_context
from flock.core.execution.local_executor import run_local_workflow
from flock.core.execution.temporal_executor import run_temporal_workflow
from flock.core.logging.logging import LOGGERS, get_logger, get_module_loggers
from flock.core.serialization.serialization_utils import (
    extract_pydantic_models_from_type_string,
)
from flock.core.util.input_resolver import split_top_level

# Import FlockAgent using TYPE_CHECKING to avoid circular import at runtime
if TYPE_CHECKING:
    from flock.core.flock_agent import FlockAgent
else:
    # Provide a forward reference string or Any for runtime if FlockAgent is used in hints here
    FlockAgent = "FlockAgent"  # Forward reference string for Pydantic/runtime

# Registry and Serialization
from flock.core.flock_registry import (
    get_registry,  # Use the unified registry
)
from flock.core.serialization.serializable import (
    Serializable,  # Import Serializable base
)

# NOTE: Flock.to_dict/from_dict primarily orchestrates agent serialization.
# It doesn't usually need serialize_item/deserialize_item directly,
# relying on FlockAgent's implementation instead.
# from flock.core.serialization.serialization_utils import serialize_item, deserialize_item
# CLI Helper (if still used directly, otherwise can be removed)
from flock.core.util.cli_helper import init_console

# Cloudpickle for fallback/direct serialization if needed
try:
    import cloudpickle

    PICKLE_AVAILABLE = True
except ImportError:
    PICKLE_AVAILABLE = False


logger = get_logger("flock")
TELEMETRY.setup_tracing()  # Setup OpenTelemetry
tracer = trace.get_tracer(__name__)
FlockRegistry = get_registry()  # Get the registry instance

# Define TypeVar for generic methods like from_dict
T = TypeVar("T", bound="Flock")


# Inherit from Serializable for YAML/JSON/etc. methods
# Use BaseModel directly for Pydantic features
class Flock(BaseModel, Serializable):
    """High-level orchestrator for creating and executing agent systems.

    Flock manages agent definitions, context, and execution flow, supporting
    both local debugging and robust distributed execution via Temporal.
    It is serializable to various formats like YAML and JSON.
    """

    name: str | None = Field(
        default_factory=lambda: f"flock_{uuid.uuid4().hex[:8]}",
        description="A unique identifier for this Flock instance.",
    )
    model: str | None = Field(
        default="openai/gpt-4o",
        description="Default model identifier to be used for agents if not specified otherwise.",
    )
    description: str | None = Field(
        default=None,
        description="A brief description of the purpose of this Flock configuration.",
    )
    enable_temporal: bool = Field(
        default=False,
        description="If True, execute workflows via Temporal; otherwise, run locally.",
    )
    enable_logging: bool = Field(
        default=False,
        description="If True, enable logging for the Flock instance.",
    )
    show_flock_banner: bool = Field(
        default=True,
        description="If True, show the Flock banner.",
    )
    # --- Runtime Attributes (Excluded from Serialization) ---
    # Store agents internally but don't make it part of the Pydantic model definition
    # Use a regular attribute, initialized in __init__
    # Pydantic V2 handles __init__ and attributes not in Field correctly
    _agents: dict[str, FlockAgent]
    _start_agent_name: str | None
    _start_input: dict

    # Pydantic v2 model config
    model_config = {
        "arbitrary_types_allowed": True,
        "ignored_types": (
            type(FlockRegistry),
        ),  # Prevent validation issues with registry
        # No need to exclude fields here, handled in to_dict
    }

    def __init__(
        self,
        name: str | None = None,
        model: str | None = "openai/gpt-4o",
        description: str | None = None,
        show_flock_banner: bool = True,
        enable_temporal: bool = False,
        enable_logging: bool
        | list[str] = False,  # Keep logging control at init
        agents: list[FlockAgent] | None = None,  # Allow passing agents at init
        **kwargs,  # Allow extra fields during init if needed, Pydantic handles it
    ):
        """Initialize the Flock orchestrator."""
        # Initialize Pydantic fields
        super().__init__(
            name=name,
            model=model,
            description=description,
            enable_temporal=enable_temporal,
            enable_logging=enable_logging,
            show_flock_banner=show_flock_banner,
            **kwargs,  # Pass extra kwargs to Pydantic BaseModel
        )

        # Initialize runtime attributes AFTER super().__init__()
        self._agents = {}
        self._start_agent_name = None
        self._start_input = {}

        # Set up logging
        self._configure_logging(enable_logging)

        # Register passed agents
        if agents:
            # Ensure FlockAgent type is available for isinstance check
            # This import might need to be deferred or handled carefully if it causes issues
            from flock.core.flock_agent import FlockAgent as ConcreteFlockAgent

            for agent in agents:
                if isinstance(agent, ConcreteFlockAgent):
                    self.add_agent(agent)
                else:
                    logger.warning(
                        f"Item provided in 'agents' list is not a FlockAgent: {type(agent)}"
                    )

        # Initialize console if needed
        if show_flock_banner:
            init_console()

        # Set Temporal debug environment variable
        self._set_temporal_debug_flag()

        # Ensure session ID exists in baggage
        self._ensure_session_id()

        logger.info(
            "Flock instance initialized",
            model=self.model,
            enable_temporal=self.enable_temporal,
        )

    # --- Keep _configure_logging, _set_temporal_debug_flag, _ensure_session_id ---
    # ... (implementation as before) ...
    def _configure_logging(self, enable_logging: bool | list[str]):
        """Configure logging levels based on the enable_logging flag."""
        # logger.debug(f"Configuring logging, enable_logging={enable_logging}")
        is_enabled_globally = False
        enabled_loggers = []

        if isinstance(enable_logging, bool):
            is_enabled_globally = enable_logging
        elif isinstance(enable_logging, list):
            is_enabled_globally = bool(
                enable_logging
            )  # Enable if list is not empty
            enabled_loggers = enable_logging

        # Configure core loggers
        for log_name in LOGGERS:
            log_instance = get_logger(log_name)
            if is_enabled_globally or log_name in enabled_loggers:
                log_instance.enable_logging = True
            else:
                log_instance.enable_logging = False

        # Configure module loggers (existing ones)
        module_loggers = get_module_loggers()
        for mod_log in module_loggers:
            if is_enabled_globally or mod_log.name in enabled_loggers:
                mod_log.enable_logging = True
            else:
                mod_log.enable_logging = False

    def _set_temporal_debug_flag(self):
        """Set or remove LOCAL_DEBUG env var based on enable_temporal."""
        if not self.enable_temporal:
            if "LOCAL_DEBUG" not in os.environ:
                os.environ["LOCAL_DEBUG"] = "1"
                logger.debug(
                    "Set LOCAL_DEBUG environment variable for local execution."
                )
        elif "LOCAL_DEBUG" in os.environ:
            del os.environ["LOCAL_DEBUG"]
            logger.debug(
                "Removed LOCAL_DEBUG environment variable for Temporal execution."
            )

    def _ensure_session_id(self):
        """Ensure a session_id exists in the OpenTelemetry baggage."""
        session_id = get_baggage("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            set_baggage("session_id", session_id)
            logger.debug(f"Generated new session_id: {session_id}")

    # --- Keep add_agent, agents property, run, run_async ---
    # ... (implementation as before, ensuring FlockAgent type hint is handled) ...
    def add_agent(self, agent: FlockAgent) -> FlockAgent:
        """Adds an agent instance to this Flock configuration."""
        # Ensure FlockAgent type is available for isinstance check
        from flock.core.flock_agent import FlockAgent as ConcreteFlockAgent

        if not isinstance(agent, ConcreteFlockAgent):
            raise TypeError("Provided object is not a FlockAgent instance.")
        if not agent.name:
            raise ValueError("Agent must have a name.")

        if agent.name in self._agents:
            logger.warning(
                f"Agent '{agent.name}' already exists in this Flock instance. Overwriting."
            )
        self._agents[agent.name] = agent
        FlockRegistry.register_agent(agent)  # Also register globally

        # Set default model if agent doesn't have one
        if agent.model is None:
            # agent.set_model(self.model) # Use Flock's default model
            if self.model:  # Ensure Flock has a model defined
                agent.set_model(self.model)
                logger.debug(
                    f"Agent '{agent.name}' using Flock default model: {self.model}"
                )
            else:
                logger.warning(
                    f"Agent '{agent.name}' has no model and Flock default model is not set."
                )

        logger.info(f"Agent '{agent.name}' added to Flock.")
        return agent

    @property
    def agents(self) -> dict[str, FlockAgent]:
        """Returns the dictionary of agents managed by this Flock instance."""
        return self._agents

    def run(
        self,
        start_agent: FlockAgent | str | None = None,
        input: dict = {},
        context: FlockContext
        | None = None,  # Allow passing initial context state
        run_id: str = "",
        box_result: bool = True,  # Changed default to False for raw dict
        agents: list[FlockAgent] | None = None,  # Allow adding agents via run
    ) -> Box:
        """Entry point for running an agent system synchronously."""
        # Check if an event loop is already running
        try:
            loop = asyncio.get_running_loop()
        except (
            RuntimeError
        ):  # 'RuntimeError: There is no current event loop...'
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(
            self.run_async(
                start_agent=start_agent,
                input=input,
                context=context,
                run_id=run_id,
                box_result=box_result,
                agents=agents,
            )
        )

    async def run_async(
        self,
        start_agent: FlockAgent | str | None = None,
        input: dict | None = None,
        context: FlockContext | None = None,
        run_id: str = "",
        box_result: bool = True,  # Changed default
        agents: list[FlockAgent] | None = None,  # Allow adding agents via run
    ) -> Box:
        """Entry point for running an agent system asynchronously."""
        # This import needs to be here or handled carefully due to potential cycles
        from flock.core.flock_agent import FlockAgent as ConcreteFlockAgent

        with tracer.start_as_current_span("flock.run_async") as span:
            # Add passed agents first
            if agents:
                for agent_obj in agents:
                    if isinstance(agent_obj, ConcreteFlockAgent):
                        self.add_agent(
                            agent_obj
                        )  # Adds to self._agents and registry
                    else:
                        logger.warning(
                            f"Item in 'agents' list is not a FlockAgent: {type(agent_obj)}"
                        )

            # Determine starting agent name
            start_agent_name: str | None = None
            if isinstance(start_agent, ConcreteFlockAgent):
                start_agent_name = start_agent.name
                if start_agent_name not in self._agents:
                    self.add_agent(
                        start_agent
                    )  # Add if instance was passed but not added
            elif isinstance(start_agent, str):
                start_agent_name = start_agent
            else:
                start_agent_name = (
                    self._start_agent_name
                )  # Use pre-configured if any

            # Default to first agent if only one exists and none specified
            if not start_agent_name and len(self._agents) == 1:
                start_agent_name = list(self._agents.keys())[0]
            elif not start_agent_name:
                raise ValueError(
                    "No start_agent specified and multiple agents exist or none are added."
                )

            # Get starting input
            run_input = input if input is not None else self._start_input

            # Log and trace start info
            span.set_attribute("start_agent", start_agent_name)
            span.set_attribute("input", str(run_input))
            span.set_attribute("run_id", run_id)
            span.set_attribute("enable_temporal", self.enable_temporal)
            logger.info(
                f"Initiating Flock run. Start Agent: '{start_agent_name}'. Temporal: {self.enable_temporal}."
            )

            try:
                # Resolve start agent instance from internal dict
                resolved_start_agent = self._agents.get(start_agent_name)
                if not resolved_start_agent:
                    # Maybe it's only in the global registry? (Less common)
                    resolved_start_agent = FlockRegistry.get_agent(
                        start_agent_name
                    )
                    if not resolved_start_agent:
                        raise ValueError(
                            f"Start agent '{start_agent_name}' not found in Flock instance or registry."
                        )
                    else:
                        # If found globally, add it to this instance for consistency during run
                        self.add_agent(resolved_start_agent)

                # Create or use provided context
                run_context = context if context else FlockContext()
                if not run_id:
                    run_id = f"flockrun_{uuid.uuid4().hex[:8]}"
                set_baggage("run_id", run_id)  # Ensure run_id is in baggage

                # Initialize context
                initialize_context(
                    run_context,
                    start_agent_name,
                    run_input,
                    run_id,
                    not self.enable_temporal,
                    self.model
                    or resolved_start_agent.model
                    or "default-model-missing",  # Pass effective model
                )

                # Execute workflow
                logger.info(
                    "Starting agent execution",
                    agent=start_agent_name,
                    enable_temporal=self.enable_temporal,
                )

                if not self.enable_temporal:
                    result = await run_local_workflow(
                        run_context, box_result=False
                    )  # Get raw dict
                else:
                    result = await run_temporal_workflow(
                        run_context, box_result=False
                    )  # Get raw dict

                span.set_attribute("result.type", str(type(result)))
                # Avoid overly large results in trace attributes
                result_str = str(result)
                if len(result_str) > 1000:
                    result_str = result_str[:1000] + "... (truncated)"
                span.set_attribute("result.preview", result_str)

                # Optionally box result before returning
                if box_result:
                    try:
                        from box import Box

                        logger.debug("Boxing final result.")
                        return Box(result)
                    except ImportError:
                        logger.warning(
                            "Box library not installed, returning raw dict. Install with 'pip install python-box'"
                        )
                        return result
                else:
                    return result

            except Exception as e:
                logger.error(f"Flock run failed: {e}", exc_info=True)
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                # Depending on desired behavior, either raise or return an error dict
                # raise # Option 1: Let the exception propagate
                return {
                    "error": str(e),
                    "details": "Flock run failed.",
                }  # Option 2: Return error dict

    # --- ADDED Serialization Methods ---

    def to_dict(
        self, path_type: Literal["absolute", "relative"] = "absolute"
    ) -> dict[str, Any]:
        """Convert Flock instance to dictionary representation.

        Args:
            path_type: How file paths should be formatted ('absolute' or 'relative')
        """
        logger.debug("Serializing Flock instance to dict.")
        # Use Pydantic's dump for base fields
        data = self.model_dump(mode="json", exclude_none=True)
        logger.info(
            f"Serializing Flock '{self.name}' with {len(self._agents)} agents"
        )

        # Manually add serialized agents
        data["agents"] = {}

        # Track custom types used across all agents
        custom_types = {}
        # Track components used across all agents
        components = {}

        for name, agent_instance in self._agents.items():
            try:
                logger.debug(f"Serializing agent '{name}'")
                # Agents handle their own serialization via their to_dict
                agent_data = agent_instance.to_dict()
                data["agents"][name] = agent_data

                if agent_instance.input:
                    logger.debug(
                        f"Extracting type information from agent '{name}' input: {agent_instance.input}"
                    )
                    input_types = self._extract_types_from_signature(
                        agent_instance.input
                    )
                    if input_types:
                        logger.debug(
                            f"Found input types in agent '{name}': {input_types}"
                        )
                        custom_types.update(
                            self._get_type_definitions(input_types)
                        )

                # Extract type information from agent outputs
                if agent_instance.output:
                    logger.debug(
                        f"Extracting type information from agent '{name}' output: {agent_instance.output}"
                    )
                    output_types = self._extract_types_from_signature(
                        agent_instance.output
                    )
                    if output_types:
                        logger.debug(
                            f"Found output types in agent '{name}': {output_types}"
                        )
                        custom_types.update(
                            self._get_type_definitions(output_types)
                        )

                # Extract component information
                if (
                    "evaluator" in agent_data
                    and "type" in agent_data["evaluator"]
                ):
                    component_type = agent_data["evaluator"]["type"]
                    logger.debug(
                        f"Adding evaluator component '{component_type}' from agent '{name}'"
                    )
                    components[component_type] = self._get_component_definition(
                        component_type, path_type
                    )

                # Extract module component information
                if "modules" in agent_data:
                    for module_name, module_data in agent_data[
                        "modules"
                    ].items():
                        if "type" in module_data:
                            component_type = module_data["type"]
                            logger.debug(
                                f"Adding module component '{component_type}' from module '{module_name}' in agent '{name}'"
                            )
                            components[component_type] = (
                                self._get_component_definition(
                                    component_type, path_type
                                )
                            )

                # Extract tool (callable) information
                if agent_data.get("tools"):
                    logger.debug(
                        f"Extracting tool information from agent '{name}': {agent_data['tools']}"
                    )
                    # Get references to the actual tool objects
                    tool_objs = (
                        agent_instance.tools if agent_instance.tools else []
                    )
                    for i, tool_name in enumerate(agent_data["tools"]):
                        if i < len(tool_objs):
                            tool = tool_objs[i]
                            if callable(tool) and not isinstance(tool, type):
                                # Get the fully qualified name for registry lookup
                                path_str = (
                                    get_registry().get_callable_path_string(
                                        tool
                                    )
                                )
                                if path_str:
                                    logger.debug(
                                        f"Adding tool '{tool_name}' (from path '{path_str}') to components"
                                    )
                                    # Add definition using just the function name as the key
                                    components[tool_name] = (
                                        self._get_callable_definition(
                                            path_str, tool_name, path_type
                                        )
                                    )

            except Exception as e:
                logger.error(
                    f"Failed to serialize agent '{name}' within Flock: {e}",
                    exc_info=True,
                )
                # Optionally skip problematic agents or raise error
                # data["agents"][name] = {"error": f"Serialization failed: {e}"}

        # Add type definitions to the serialized output if any were found
        if custom_types:
            logger.info(
                f"Adding {len(custom_types)} custom type definitions to serialized output"
            )
            data["types"] = custom_types

        # Add component definitions to the serialized output if any were found
        if components:
            logger.info(
                f"Adding {len(components)} component definitions to serialized output"
            )
            data["components"] = components

        # Add dependencies section
        data["dependencies"] = self._get_dependencies()

        # Add serialization settings
        data["metadata"] = {"path_type": path_type}

        logger.debug(
            f"Flock serialization complete with {len(data['agents'])} agents, {len(custom_types)} types, {len(components)} components"
        )

        return data

    def _extract_types_from_signature(self, signature: str) -> list[str]:
        """Extract type names from an input/output signature string."""
        if not signature:
            return []

        signature_parts = split_top_level(signature)

        # Basic type extraction - handles simple cases like "result: TypeName" or "list[TypeName]"
        custom_types = []

        # Look for type annotations (everything after ":")
        for part in signature_parts:
            parts = part.split(":")
            if len(parts) > 1:
                type_part = parts[1].strip()

            pydantic_models = extract_pydantic_models_from_type_string(
                type_part
            )
            if pydantic_models:
                for model in pydantic_models:
                    custom_types.append(model.__name__)

            # # Extract from list[Type]
            # if "list[" in type_part:
            #     inner_type = type_part.split("list[")[1].split("]")[0].strip()
            #     if inner_type and inner_type.lower() not in [
            #         "str",
            #         "int",
            #         "float",
            #         "bool",
            #         "dict",
            #         "list",
            #     ]:
            #         custom_types.append(inner_type)

            # # Extract direct type references
            # elif type_part and type_part.lower() not in [
            #     "str",
            #     "int",
            #     "float",
            #     "bool",
            #     "dict",
            #     "list",
            # ]:
            #     custom_types.append(
            #         type_part.split()[0]
            #     )  # Take the first word in case there's a description

        return custom_types

    def _get_type_definitions(self, type_names: list[str]) -> dict[str, Any]:
        """Get definitions for the specified custom types."""
        from flock.core.flock_registry import get_registry

        type_definitions = {}
        registry = get_registry()

        for type_name in type_names:
            try:
                # Try to get the type from registry
                type_obj = registry._types.get(type_name)
                if type_obj:
                    type_def = self._extract_type_definition(
                        type_name, type_obj
                    )
                    if type_def:
                        type_definitions[type_name] = type_def
            except Exception as e:
                logger.warning(
                    f"Could not extract definition for type {type_name}: {e}"
                )

        return type_definitions

    def _extract_type_definition(
        self, type_name: str, type_obj: type
    ) -> dict[str, Any]:
        """Extract a definition for a custom type."""
        import inspect
        from dataclasses import is_dataclass

        type_def = {
            "module_path": type_obj.__module__,
        }

        # Handle Pydantic models
        if hasattr(type_obj, "model_json_schema") and callable(
            getattr(type_obj, "model_json_schema")
        ):
            type_def["type"] = "pydantic.BaseModel"
            try:
                schema = type_obj.model_json_schema()
                # Clean up schema to remove unnecessary fields
                if "title" in schema and schema["title"] == type_name:
                    del schema["title"]
                type_def["schema"] = schema
            except Exception as e:
                logger.warning(
                    f"Could not extract schema for Pydantic model {type_name}: {e}"
                )

        # Handle dataclasses
        elif is_dataclass(type_obj):
            type_def["type"] = "dataclass"
            fields = {}
            for field_name, field in type_obj.__dataclass_fields__.items():
                fields[field_name] = {
                    "type": str(field.type),
                    "default": str(field.default)
                    if field.default is not inspect.Parameter.empty
                    else None,
                }
            type_def["fields"] = fields

        # Handle other types - just store basic information
        else:
            type_def["type"] = "custom"

        # Extract import statement (simplified version)
        type_def["imports"] = [f"from {type_obj.__module__} import {type_name}"]

        return type_def

    def _get_component_definition(
        self, component_type: str, path_type: Literal["absolute", "relative"]
    ) -> dict[str, Any]:
        """Get definition for a component type."""
        import os
        import sys

        from flock.core.flock_registry import get_registry

        registry = get_registry()
        component_def = {}

        try:
            # Try to get the component class from registry
            component_class = registry._components.get(component_type)
            if component_class:
                # Get the standard module path
                module_path = component_class.__module__

                # Get the actual file system path if possible
                file_path = None
                try:
                    if (
                        hasattr(component_class, "__module__")
                        and component_class.__module__
                    ):
                        module = sys.modules.get(component_class.__module__)
                        if module and hasattr(module, "__file__"):
                            file_path = os.path.abspath(module.__file__)
                            # Convert to relative path if needed
                            if path_type == "relative" and file_path:
                                try:
                                    file_path = os.path.relpath(file_path)
                                except ValueError:
                                    # Keep as absolute if can't make relative
                                    logger.warning(
                                        f"Could not convert path to relative: {file_path}"
                                    )
                except Exception as e:
                    # If we can't get the file path, we'll just use the module path
                    logger.warning(
                        f"Error getting file path for component {component_type}: {e}"
                    )
                    pass

                component_def = {
                    "type": "flock_component",
                    "module_path": module_path,
                    "file_path": file_path,  # Include actual file system path
                    "description": getattr(
                        component_class, "__doc__", ""
                    ).strip()
                    or f"{component_type} component",
                }
        except Exception as e:
            logger.warning(
                f"Could not extract definition for component {component_type}: {e}"
            )
            # Provide minimal information if we can't extract details
            component_def = {
                "type": "flock_component",
                "module_path": "unknown",
                "file_path": None,
                "description": f"{component_type} component (definition incomplete)",
            }

        return component_def

    def _get_callable_definition(
        self,
        callable_ref: str,
        func_name: str,
        path_type: Literal["absolute", "relative"],
    ) -> dict[str, Any]:
        """Get definition for a callable reference.

        Args:
            callable_ref: The fully qualified path to the callable
            func_name: The simple function name (for display purposes)
            path_type: How file paths should be formatted ('absolute' or 'relative')
        """
        import inspect
        import os
        import sys

        from flock.core.flock_registry import get_registry

        registry = get_registry()
        callable_def = {}

        try:
            # Try to get the callable from registry
            logger.debug(
                f"Getting callable definition for '{callable_ref}' (display name: '{func_name}')"
            )
            func = registry.get_callable(callable_ref)
            if func:
                # Get the standard module path
                module_path = func.__module__

                # Get the actual file system path if possible
                file_path = None
                try:
                    if func.__module__ and func.__module__ != "builtins":
                        module = sys.modules.get(func.__module__)
                        if module and hasattr(module, "__file__"):
                            file_path = os.path.abspath(module.__file__)
                            # Convert to relative path if needed
                            if path_type == "relative" and file_path:
                                try:
                                    file_path = os.path.relpath(file_path)
                                except ValueError:
                                    # Keep as absolute if can't make relative
                                    logger.warning(
                                        f"Could not convert path to relative: {file_path}"
                                    )
                except Exception as e:
                    # If we can't get the file path, just use the module path
                    logger.warning(
                        f"Error getting file path for callable {callable_ref}: {e}"
                    )
                    pass

                # Get the docstring for description
                docstring = (
                    inspect.getdoc(func) or f"Callable function {func_name}"
                )

                callable_def = {
                    "type": "flock_callable",
                    "module_path": module_path,
                    "file_path": file_path,
                    "description": docstring.strip(),
                }
                logger.debug(
                    f"Created callable definition for '{func_name}': module={module_path}, file={file_path}"
                )
        except Exception as e:
            logger.warning(
                f"Could not extract definition for callable {callable_ref}: {e}"
            )
            # Provide minimal information
            callable_def = {
                "type": "flock_callable",
                "module_path": callable_ref.split(".")[0]
                if "." in callable_ref
                else "unknown",
                "file_path": None,
                "description": f"Callable {func_name} (definition incomplete)",
            }

        return callable_def

    def _get_dependencies(self) -> list[str]:
        """Get list of dependencies required by this Flock."""
        # This is a simplified version - in production, you might want to detect
        # actual versions of installed packages
        return [
            "pydantic>=2.0.0",
            "flock>=0.3.41",  # Assuming this is the package name
        ]

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Create Flock instance from dictionary representation."""
        logger.debug(
            f"Deserializing Flock from dict. Provided keys: {list(data.keys())}"
        )

        # Check for serialization settings
        serialization_settings = data.pop("serialization_settings", {})
        path_type = serialization_settings.get("path_type", "absolute")
        logger.debug(
            f"Using path_type '{path_type}' from serialization settings"
        )

        # First, handle type definitions if present
        if "types" in data:
            logger.info(f"Processing {len(data['types'])} type definitions")
            cls._register_type_definitions(data["types"])

        # Then, handle component definitions if present
        if "components" in data:
            logger.info(
                f"Processing {len(data['components'])} component definitions"
            )
            cls._register_component_definitions(data["components"], path_type)

        # Check dependencies if present
        if "dependencies" in data:
            logger.debug(f"Checking {len(data['dependencies'])} dependencies")
            cls._check_dependencies(data["dependencies"])

        # Ensure FlockAgent is importable for type checking later
        try:
            from flock.core.flock_agent import FlockAgent as ConcreteFlockAgent
        except ImportError:
            logger.error(
                "Cannot import FlockAgent, deserialization may fail for agents."
            )
            ConcreteFlockAgent = Any  # Fallback

        # Extract agent data before initializing Flock base model
        agents_data = data.pop("agents", {})
        logger.info(f"Found {len(agents_data)} agents to deserialize")

        # Remove types, components, and dependencies sections as they're not part of Flock fields
        data.pop("types", None)
        data.pop("components", None)
        data.pop("dependencies", None)
        # Remove metadata if present
        data.pop("metadata", None)

        # Create Flock instance using Pydantic constructor for basic fields
        try:
            # Pass only fields defined in Flock's Pydantic model
            init_data = {k: v for k, v in data.items() if k in cls.model_fields}
            logger.debug(
                f"Creating Flock instance with fields: {list(init_data.keys())}"
            )
            flock_instance = cls(**init_data)
        except Exception as e:
            logger.error(
                f"Pydantic validation/init failed for Flock: {e}", exc_info=True
            )
            raise ValueError(
                f"Failed to initialize Flock from dict: {e}"
            ) from e

        # Deserialize and add agents AFTER Flock instance exists
        for name, agent_data in agents_data.items():
            try:
                logger.debug(f"Deserializing agent '{name}'")
                # Ensure agent_data has the name, or add it from the key
                agent_data.setdefault("name", name)
                # Use FlockAgent's from_dict method
                agent_instance = ConcreteFlockAgent.from_dict(agent_data)
                flock_instance.add_agent(
                    agent_instance
                )  # Adds to _agents and registers
                logger.debug(f"Successfully added agent '{name}' to Flock")
            except Exception as e:
                logger.error(
                    f"Failed to deserialize or add agent '{name}' during Flock deserialization: {e}",
                    exc_info=True,
                )
                # Decide: skip agent or raise error?

        logger.info(
            f"Successfully deserialized Flock instance '{flock_instance.name}' with {len(flock_instance._agents)} agents"
        )
        return flock_instance

    @classmethod
    def _register_type_definitions(cls, type_defs: dict[str, Any]) -> None:
        """Register type definitions from serialized data."""
        import importlib

        from flock.core.flock_registry import get_registry

        registry = get_registry()

        for type_name, type_def in type_defs.items():
            logger.debug(f"Registering type: {type_name}")

            try:
                # First try to import the type directly
                module_path = type_def.get("module_path")
                if module_path:
                    try:
                        module = importlib.import_module(module_path)
                        if hasattr(module, type_name):
                            type_obj = getattr(module, type_name)
                            registry.register_type(type_obj, type_name)
                            logger.info(
                                f"Registered type {type_name} from module {module_path}"
                            )
                            continue
                    except ImportError:
                        logger.debug(
                            f"Could not import {module_path}, trying dynamic type creation"
                        )

                # If direct import fails, try to create the type dynamically
                if (
                    type_def.get("type") == "pydantic.BaseModel"
                    and "schema" in type_def
                ):
                    cls._create_pydantic_model(type_name, type_def)
                elif (
                    type_def.get("type") == "dataclass" and "fields" in type_def
                ):
                    cls._create_dataclass(type_name, type_def)
                else:
                    logger.warning(
                        f"Unsupported type definition for {type_name}, type: {type_def.get('type')}"
                    )

            except Exception as e:
                logger.error(f"Failed to register type {type_name}: {e}")

    @classmethod
    def _create_pydantic_model(
        cls, type_name: str, type_def: dict[str, Any]
    ) -> None:
        """Dynamically create a Pydantic model from a schema definition."""
        from pydantic import create_model

        from flock.core.flock_registry import get_registry

        registry = get_registry()
        schema = type_def.get("schema", {})

        try:
            # Extract field definitions from schema
            fields = {}
            properties = schema.get("properties", {})
            required = schema.get("required", [])

            for field_name, field_schema in properties.items():
                # Determine the field type based on schema
                field_type = cls._get_type_from_schema(field_schema)

                # Determine if field is required
                default = ... if field_name in required else None

                # Add to fields dict
                fields[field_name] = (field_type, default)

            # Create the model
            DynamicModel = create_model(type_name, **fields)

            # Register it
            registry.register_type(DynamicModel, type_name)
            logger.info(f"Created and registered Pydantic model: {type_name}")

        except Exception as e:
            logger.error(f"Failed to create Pydantic model {type_name}: {e}")

    @classmethod
    def _get_type_from_schema(cls, field_schema: dict[str, Any]) -> Any:
        """Convert JSON schema type to Python type."""
        schema_type = field_schema.get("type")

        # Basic type mapping
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        # Handle basic types
        if schema_type in type_mapping:
            return type_mapping[schema_type]

        # Handle enums
        if "enum" in field_schema:
            from typing import Literal

            return Literal[tuple(field_schema["enum"])]

        # Default
        return Any

    @classmethod
    def _create_dataclass(
        cls, type_name: str, type_def: dict[str, Any]
    ) -> None:
        """Dynamically create a dataclass from a field definition."""
        from dataclasses import make_dataclass

        from flock.core.flock_registry import get_registry

        registry = get_registry()
        fields_def = type_def.get("fields", {})

        try:
            fields = []
            for field_name, field_props in fields_def.items():
                field_type = eval(
                    field_props.get("type", "str")
                )  # Note: eval is used here for simplicity
                fields.append((field_name, field_type))

            # Create the dataclass
            DynamicDataclass = make_dataclass(type_name, fields)

            # Register it
            registry.register_type(DynamicDataclass, type_name)
            logger.info(f"Created and registered dataclass: {type_name}")

        except Exception as e:
            logger.error(f"Failed to create dataclass {type_name}: {e}")

    @classmethod
    def _register_component_definitions(
        cls,
        component_defs: dict[str, Any],
        path_type: Literal["absolute", "relative"],
    ) -> None:
        """Register component definitions from serialized data."""
        import importlib
        import importlib.util
        import os
        import sys

        from flock.core.flock_registry import get_registry

        registry = get_registry()

        for component_name, component_def in component_defs.items():
            logger.debug(f"Registering component: {component_name}")
            component_type = component_def.get("type", "flock_component")

            try:
                # Handle callables differently than components
                if component_type == "flock_callable":
                    # For callables, component_name is just the function name
                    func_name = component_name
                    module_path = component_def.get("module_path")
                    file_path = component_def.get("file_path")

                    # Convert relative path to absolute if needed
                    if (
                        path_type == "relative"
                        and file_path
                        and not os.path.isabs(file_path)
                    ):
                        try:
                            # Make absolute based on current directory
                            file_path = os.path.abspath(file_path)
                            logger.debug(
                                f"Converted relative path '{component_def.get('file_path')}' to absolute: '{file_path}'"
                            )
                        except Exception as e:
                            logger.warning(
                                f"Could not convert relative path to absolute: {e}"
                            )

                    logger.debug(
                        f"Processing callable '{func_name}' from module '{module_path}', file: {file_path}"
                    )

                    # Try direct import first
                    if module_path:
                        try:
                            logger.debug(
                                f"Attempting to import module: {module_path}"
                            )
                            module = importlib.import_module(module_path)
                            if hasattr(module, func_name):
                                callable_obj = getattr(module, func_name)
                                # Register with just the name for easier lookup
                                registry.register_callable(
                                    callable_obj, func_name
                                )
                                logger.info(
                                    f"Registered callable with name: {func_name}"
                                )
                                # Also register with fully qualified path for compatibility
                                if module_path != "__main__":
                                    full_path = f"{module_path}.{func_name}"
                                    registry.register_callable(
                                        callable_obj, full_path
                                    )
                                    logger.info(
                                        f"Also registered callable with full path: {full_path}"
                                    )
                                logger.info(
                                    f"Successfully registered callable {func_name} from module {module_path}"
                                )
                                continue
                            else:
                                logger.warning(
                                    f"Function '{func_name}' not found in module {module_path}"
                                )
                        except ImportError:
                            logger.debug(
                                f"Could not import module {module_path}, trying file path"
                            )

                    # Try file path if module import fails
                    if file_path and os.path.exists(file_path):
                        try:
                            logger.debug(
                                f"Attempting to load file: {file_path}"
                            )
                            # Create a module name from file path
                            mod_name = f"{func_name}_module"
                            spec = importlib.util.spec_from_file_location(
                                mod_name, file_path
                            )
                            if spec and spec.loader:
                                module = importlib.util.module_from_spec(spec)
                                sys.modules[spec.name] = module
                                spec.loader.exec_module(module)
                                logger.debug(
                                    f"Successfully loaded module from file, searching for function '{func_name}'"
                                )

                                # Look for the function in the loaded module
                                if hasattr(module, func_name):
                                    callable_obj = getattr(module, func_name)
                                    registry.register_callable(
                                        callable_obj, func_name
                                    )
                                    logger.info(
                                        f"Successfully registered callable {func_name} from file {file_path}"
                                    )
                                else:
                                    logger.warning(
                                        f"Function {func_name} not found in file {file_path}"
                                    )
                            else:
                                logger.warning(
                                    f"Could not create import spec for {file_path}"
                                )
                        except Exception as e:
                            logger.error(
                                f"Error loading callable {func_name} from file {file_path}: {e}",
                                exc_info=True,
                            )

                # Handle regular components (existing code)
                else:
                    # First try using the module path (Python import)
                    module_path = component_def.get("module_path")
                    if module_path and module_path != "unknown":
                        try:
                            logger.debug(
                                f"Attempting to import module '{module_path}' for component '{component_name}'"
                            )
                            module = importlib.import_module(module_path)
                            # Find the component class in the module
                            for attr_name in dir(module):
                                if attr_name == component_name:
                                    component_class = getattr(module, attr_name)
                                    registry.register_component(
                                        component_class, component_name
                                    )
                                    logger.info(
                                        f"Registered component {component_name} from {module_path}"
                                    )
                                    break
                            else:
                                logger.warning(
                                    f"Component {component_name} not found in module {module_path}"
                                )
                                # If we didn't find the component, try using file_path next
                                raise ImportError(
                                    f"Component {component_name} not found in module {module_path}"
                                )
                        except ImportError:
                            # If module import fails, try file_path approach
                            file_path = component_def.get("file_path")

                            # Convert relative path to absolute if needed
                            if (
                                path_type == "relative"
                                and file_path
                                and not os.path.isabs(file_path)
                            ):
                                try:
                                    # Make absolute based on current directory
                                    file_path = os.path.abspath(file_path)
                                    logger.debug(
                                        f"Converted relative path '{component_def.get('file_path')}' to absolute: '{file_path}'"
                                    )
                                except Exception as e:
                                    logger.warning(
                                        f"Could not convert relative path to absolute: {e}"
                                    )

                            if file_path and os.path.exists(file_path):
                                logger.debug(
                                    f"Attempting to load {component_name} from file: {file_path}"
                                )
                                try:
                                    # Load the module from file path
                                    spec = (
                                        importlib.util.spec_from_file_location(
                                            f"{component_name}_module",
                                            file_path,
                                        )
                                    )
                                    if spec and spec.loader:
                                        module = (
                                            importlib.util.module_from_spec(
                                                spec
                                            )
                                        )
                                        sys.modules[spec.name] = module
                                        spec.loader.exec_module(module)
                                        logger.debug(
                                            f"Successfully loaded module from file, searching for component class '{component_name}'"
                                        )

                                        # Find the component class in the loaded module
                                        for attr_name in dir(module):
                                            if attr_name == component_name:
                                                component_class = getattr(
                                                    module, attr_name
                                                )
                                                registry.register_component(
                                                    component_class,
                                                    component_name,
                                                )
                                                logger.info(
                                                    f"Registered component {component_name} from file {file_path}"
                                                )
                                                break
                                        else:
                                            logger.warning(
                                                f"Component {component_name} not found in file {file_path}"
                                            )
                                except Exception as e:
                                    logger.error(
                                        f"Error loading component {component_name} from file {file_path}: {e}",
                                        exc_info=True,
                                    )
                            else:
                                logger.warning(
                                    f"No valid file path found for component {component_name}"
                                )
                    else:
                        logger.warning(
                            f"Missing or unknown module path for component {component_name}"
                        )
            except Exception as e:
                logger.error(
                    f"Failed to register component {component_name}: {e}",
                    exc_info=True,
                )

    @classmethod
    def _check_dependencies(cls, dependencies: list[str]) -> None:
        """Check if required dependencies are available."""
        import importlib
        import re

        for dependency in dependencies:
            # Extract package name and version
            match = re.match(r"([^>=<]+)([>=<].+)?", dependency)
            if match:
                package_name = match.group(1)
                try:
                    importlib.import_module(package_name.replace("-", "_"))
                    logger.debug(f"Dependency {package_name} is available")
                except ImportError:
                    logger.warning(f"Dependency {dependency} is not installed")

    # --- API Start Method ---
    def start_api(
        self,
        host: str = "127.0.0.1",
        port: int = 8344,
        server_name: str = "Flock API",
        create_ui: bool = False,
    ) -> None:
        """Start a REST API server for this Flock instance."""
        # Import locally to avoid making API components a hard dependency
        try:
            from flock.core.api import FlockAPI
        except ImportError:
            logger.error(
                "API components not found. Cannot start API. "
                "Ensure 'fastapi' and 'uvicorn' are installed."
            )
            return

        logger.info(
            f"Preparing to start API server on {host}:{port} {'with UI' if create_ui else 'without UI'}"
        )
        api_instance = FlockAPI(self)  # Pass the current Flock instance
        # Use the start method of FlockAPI
        api_instance.start(
            host=host, port=port, server_name=server_name, create_ui=create_ui
        )

    # --- CLI Start Method ---
    def start_cli(
        self,
        server_name: str = "Flock CLI",
        show_results: bool = False,
        edit_mode: bool = False,
    ) -> None:
        """Start a CLI interface for this Flock instance.

        This method loads the CLI with the current Flock instance already available,
        allowing users to execute, edit, or manage agents from the existing configuration.

        Args:
            server_name: Optional name for the CLI interface
            show_results: Whether to initially show results of previous runs
            edit_mode: Whether to open directly in edit mode
        """
        # Import locally to avoid circular imports
        try:
            from flock.cli.loaded_flock_cli import start_loaded_flock_cli
        except ImportError:
            logger.error(
                "CLI components not found. Cannot start CLI. "
                "Ensure the CLI modules are properly installed."
            )
            return

        logger.info(
            f"Starting CLI interface with loaded Flock instance ({len(self._agents)} agents)"
        )

        # Pass the current Flock instance to the CLI
        start_loaded_flock_cli(
            flock=self,
            server_name=server_name,
            show_results=show_results,
            edit_mode=edit_mode,
        )

    # --- Static Method Loaders (Keep for convenience) ---
    @staticmethod
    def load_from_file(file_path: str) -> Flock:
        """Load a Flock instance from various file formats (detects type)."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Flock file not found: {file_path}")

        try:
            if p.suffix in [".yaml", ".yml"]:
                return Flock.from_yaml_file(p)
            elif p.suffix == ".json":
                return Flock.from_json(p.read_text())
            elif p.suffix == ".msgpack":
                return Flock.from_msgpack_file(p)
            elif p.suffix == ".pkl":
                if PICKLE_AVAILABLE:
                    return Flock.from_pickle_file(p)
                else:
                    raise RuntimeError(
                        "Cannot load Pickle file: cloudpickle not installed."
                    )
            else:
                raise ValueError(
                    f"Unsupported file extension: {p.suffix}. Use .yaml, .json, .msgpack, or .pkl."
                )
        except Exception as e:
            # Check if it's an exception about missing types
            if "Could not get registered type name" in str(e):
                logger.error(
                    f"Failed to load Flock from {file_path}: Missing type definition. "
                    "This may happen if the YAML was created on a system with different types registered. "
                    "Check if the file includes 'types' section with necessary type definitions."
                )
            logger.error(f"Error loading Flock from {file_path}: {e}")
            raise
