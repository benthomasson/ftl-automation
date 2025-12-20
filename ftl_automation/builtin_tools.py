"""
Built-in tools for ftl-automation.

These tools provide essential functionality like user input, completion signaling,
and other common automation tasks.
"""

import yaml
from typing import Dict, Any, Optional
from rich.prompt import Prompt

from .tool_base import AutomationTool


class CompletionException(Exception):
    """Exception raised to signal successful task completion."""
    pass


class ImpossibleException(Exception):
    """Exception raised to signal that a task is impossible to complete."""
    pass


# ==============================================================================
# AutomationTool-based classes
# ==============================================================================

class UserInputTool(AutomationTool):
    """AutomationTool class for user input prompts."""
    
    name = "user_input_tool"
    description = "Prompt user for input during automation execution"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, question: str, default: Optional[str] = None):
        """Prompt user for input during automation execution."""
        return Prompt.ask(question, default=default)


class CompleteTool(AutomationTool):
    """AutomationTool class for signaling task completion."""
    
    name = "complete"
    description = "Signal that the automation task has completed successfully"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, message: str = "Task completed successfully"):
        """Signal that the automation task has completed successfully."""
        if self.context.console:
            self.context.console.print(f"[green]✓ {message}[/green]")
        else:
            print(f"✓ {message}")
        
        raise CompletionException(message)


class ImpossibleTool(AutomationTool):
    """AutomationTool class for signaling task impossibility."""
    
    name = "impossible"
    description = "Signal that the automation task is impossible"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, reason: str = "Task cannot be completed"):
        """Signal that the automation task is impossible."""
        if self.context.console:
            self.context.console.print(f"[red]✗ {reason}[/red]")
        else:
            print(f"✗ {reason}")
        
        raise ImpossibleException(reason)


class DebugTool(AutomationTool):
    """AutomationTool class for debug output."""
    
    name = "debug_tool"
    description = "Print debug message during automation"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def __call__(self, message: str):
        """Print debug message during automation."""
        if self.context.console:
            self.context.console.print(f"[dim]DEBUG: {message}[/dim]")
        else:
            print(f"DEBUG: {message}")


def get_builtin_tools() -> Dict[str, callable]:
    """
    Get dictionary of all built-in tools.
    
    Returns:
        Dictionary mapping tool names to AutomationTool classes
    """
    # Return the tool classes that will be instantiated with context
    return {
        'user_input_tool': UserInputTool,
        'complete': CompleteTool,
        'impossible': ImpossibleTool, 
        'debug_tool': DebugTool,
    }


def get_builtin_tool_classes() -> Dict[str, type]:
    """
    Get dictionary of all built-in tool classes.
    
    Returns:
        Dictionary mapping tool names to AutomationTool classes
    """
    return {
        'user_input_tool': UserInputTool,
        'complete': CompleteTool,
        'impossible': ImpossibleTool,
        'debug_tool': DebugTool,
    }
