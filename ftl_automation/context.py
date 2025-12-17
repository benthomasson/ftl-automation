"""
Automation context and state management.
"""

from typing import Dict, Any, Optional
from rich.console import Console


class ToolsProxy:
    """Proxy object that allows tool access via attribute notation."""
    
    def __init__(self, tools_dict):
        self._tools = tools_dict
    
    def __getattr__(self, name):
        if name in self._tools:
            return self._tools[name]
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
        **kwargs
    ):
        self.inventory = inventory
        self.modules = modules 
        self._tools_dict = tools
        self.tools = ToolsProxy(tools)  # Enable ftl.tools.tool_name syntax
        self.localhost = localhost
        self.extra_vars = extra_vars or {}
        self.console = console or Console()
        self.secrets = secrets or {}
        self.gate_cache = {}
        self.use_gate = kwargs.get('use_gate', False)
        
        # Store additional context variables
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def get_tool(self, name: str):
        """Get a tool by name."""
        return self.tools.get(name)
    
    def execute_tool(self, name: str, **kwargs):
        """Execute a tool with given arguments."""
        tool = self.get_tool(name)
        if tool is None:
            raise ValueError(f"Tool '{name}' not found")
        
        # Execute tool function with context
        return tool(
            inventory=self.inventory,
            modules=self.modules,
            console=self.console,
            gate_cache=self.gate_cache,
            use_gate=self.use_gate,
            **kwargs
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
            use_gate=self.use_gate
        )
    
    def print(self, *args, **kwargs):
        """Print to the console."""
        self.console.print(*args, **kwargs)
        
    def cleanup(self):
        """Cleanup resources."""
        # Close any open gates
        if hasattr(self, 'gate_cache'):
            # Add cleanup logic for gates if needed
            pass