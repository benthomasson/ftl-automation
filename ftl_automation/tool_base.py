"""
Base tool class for ftl-automation.

Provides a simple, function-based interface for automation tools that can replace
smolagents.Tool while maintaining compatibility with existing tool patterns.
"""

import inspect
from typing import Any, Dict, Optional, Callable


class AutomationTool:
    """
    Base class for ftl-automation compatible tools.
    
    Tools are simple functions that can be called with automation context.
    This replaces smolagents.Tool with a lightweight, dependency-free alternative.
    """
    
    name: str = None
    module: Optional[str] = None
    description: str = ""
    
    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        """
        Initialize tool with automation context.
        
        Args:
            inventory: Target systems/hosts configuration
            modules: Available automation modules  
            console: Rich console for formatted output
            secrets: Secure credential storage
            **kwargs: Additional context (gate_cache, gate, workspace, etc.)
        """
        self.inventory = inventory
        self.modules = modules
        self.console = console
        self.secrets = secrets or {}
        self.context = kwargs
    
    def __call__(self, **kwargs) -> Any:
        """
        Execute the tool with the provided arguments.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Tool execution result
        """
        # Add automation context to tool call
        kwargs.update({
            'inventory': self.inventory,
            'modules': self.modules, 
            'console': self.console,
            'secrets': self.secrets,
            **self.context
        })
        
        return self.forward(**kwargs)
    
    def forward(self, **kwargs) -> Any:
        """
        Tool implementation - override this method in subclasses.
        
        Args:
            **kwargs: Tool parameters plus automation context
            
        Returns:
            Tool execution result
        """
        raise NotImplementedError("Tools must implement forward() method")


def create_tool_function(tool_class: type) -> Callable:
    """
    Convert an AutomationTool class into a simple function for ftl-automation.
    
    Args:
        tool_class: AutomationTool subclass
        
    Returns:
        Function that can be loaded by ftl-automation
    """
    def tool_function(inventory, modules, console, **kwargs):
        """Tool function compatible with ftl-automation."""
        tool = tool_class(inventory, modules, console, **kwargs)
        
        # Get the original forward method signature to extract parameters
        sig = inspect.signature(tool.forward)
        tool_params = {}
        
        for param_name, param in sig.parameters.items():
            if param_name in ['inventory', 'modules', 'console', 'secrets']:
                continue  # Skip context parameters
            if param_name in kwargs:
                tool_params[param_name] = kwargs[param_name]
        
        # Call the tool with just its specific parameters
        return tool(**tool_params)
    
    # Copy metadata from the tool class
    tool_function.__name__ = tool_class.name or tool_class.__name__.lower() + '_tool'
    tool_function.__doc__ = tool_class.description or tool_class.__doc__
    
    return tool_function