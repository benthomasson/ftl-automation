"""
Automation context and state management.
"""

from typing import Dict, Any, Optional
from rich.console import Console


class ToolsProxy:
    """Proxy object that allows tool access via attribute notation."""

    def __init__(self, tools_dict, context):
        self._tools = tools_dict
        self._context = context

    def __getattr__(self, name):
        if name in self._tools:
            return self.tools[name]
        raise AttributeError(f"Tool '{name}' not found")

    def __contains__(self, name):
        return name in self._tools

    def __iter__(self):
        return iter(self._tools)

    def keys(self):
        return self._tools.keys()


class AutomationContext:
    """
    Context object that holds automation state and resources.

    Provides access to inventory, modules, tools, and execution environment.
    """

    def __init__(
        self,
        inventory: Dict[str, Any],
        modules: Dict[str, Any],
        tools: Dict[str, Any],
        localhost: Any,
        extra_vars: Optional[Dict[str, Any]] = None,
        console: Optional[Console] = None,
        secrets: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        self.inventory = inventory
        self.modules = modules
        self._tools_dict = tools
        self.tools = ToolsProxy(tools, self)  # Enable ftl.tools.tool_name syntax
        self.localhost = localhost
        self.extra_vars = extra_vars or {}
        self.console = console or Console()
        self.secrets = secrets or {}
        self.gate_cache = {}
        self.use_gate = kwargs.get("use_gate", False)

        # Store additional context variables
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_tool(self, name: str):
        """Get a tool by name."""
        return self._tools_dict.get(name)

    def __getattr__(self, name: str):
        """Allow direct tool calls like ftl.bash(...)"""
        if name in self._tools_dict:
            return self._tools_dict[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def run_module(self, module_name: str, **module_args):
        """Execute an FTL module."""
        from .core import run_module

        return run_module(
            self.inventory,
            self.modules,
            module_name,
            module_args,
            gate_cache=self.gate_cache,
            use_gate=self.use_gate,
        )

    def print(self, *args, **kwargs):
        """Print to the console."""
        self.console.print(*args, **kwargs)

    def cleanup(self):
        """Cleanup resources."""
        # Close any open gates
        if hasattr(self, "gate_cache"):
            # Add cleanup logic for gates if needed
            pass
