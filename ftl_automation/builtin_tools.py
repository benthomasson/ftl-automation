"""
Built-in tools for ftl-automation.

These tools provide essential functionality like user input, completion signaling,
and other common automation tasks.
"""

import yaml
from typing import Dict, Any, Optional
from rich.prompt import Prompt

from .tool_base import AutomationTool
from .exceptions import CompletionException, ImpossibleException


# ==============================================================================
# AutomationTool-based classes
# ==============================================================================

class UserInputTool(AutomationTool):
    """AutomationTool class for user input prompts."""
    
    name = "user_input"
    description = "Prompt user for input during automation execution"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def _execute(self, question: str, default: Optional[str] = None):
        """Prompt user for input during automation execution."""
        return Prompt.ask(question, default=default)
    
    def _dry_run_preview(self, question: str, default: Optional[str] = None):
        """Generate dry run preview for user input."""
        preview = f"[DRY RUN] Would prompt: '{question}'"
        if default:
            preview += f" (default: {default})"
            simulated_response = default
        else:
            simulated_response = "<user input required>"
        
        self.context.console.print(f"[cyan]{preview}[/cyan]")
        
        return {
            'dry_run': True,
            'question': question,
            'default': default,
            'simulated_response': simulated_response,
            'preview': preview,
            'msg': 'Dry run preview for user input'
        }


class CompleteTool(AutomationTool):
    """AutomationTool class for signaling task completion."""
    
    name = "complete"
    description = "Signal that the automation task has completed successfully"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def _execute(self, message: str = "Task completed successfully"):
        """Signal that the automation task has completed successfully."""
        if self.context.console:
            self.context.console.print(f"[green]✓ {message}[/green]")
        else:
            print(f"✓ {message}")
        
        raise CompletionException(message)
    
    def _dry_run_preview(self, message: str = "Task completed successfully"):
        """Generate dry run preview for completion."""
        preview = f"[DRY RUN] Would complete with message: '{message}'"
        self.context.console.print(f"[green]{preview}[/green]")
        
        return {
            'dry_run': True,
            'message': message,
            'preview': preview,
            'would_complete': True,
            'msg': 'Dry run preview for completion'
        }


class ImpossibleTool(AutomationTool):
    """AutomationTool class for signaling task impossibility."""
    
    name = "impossible"
    description = "Signal that the automation task is impossible"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def _execute(self, reason: str = "Task cannot be completed"):
        """Signal that the automation task is impossible."""
        if self.context.console:
            self.context.console.print(f"[red]✗ {reason}[/red]")
        else:
            print(f"✗ {reason}")
        
        raise ImpossibleException(reason)
    
    def _dry_run_preview(self, reason: str = "Task cannot be completed"):
        """Generate dry run preview for impossibility."""
        preview = f"[DRY RUN] Would exit with error: '{reason}'"
        self.context.console.print(f"[red]{preview}[/red]")
        
        return {
            'dry_run': True,
            'reason': reason,
            'preview': preview,
            'would_exit': True,
            'msg': 'Dry run preview for impossibility'
        }


class DebugTool(AutomationTool):
    """AutomationTool class for debug output."""
    
    name = "debug"
    description = "Print debug message during automation"
    
    def __init__(self, context):
        """Initialize with AutomationContext."""
        self.context = context

    def _execute(self, message: str):
        """Print debug message during automation."""
        if self.context.console:
            self.context.console.print(f"[dim]DEBUG: {message}[/dim]")
        else:
            print(f"DEBUG: {message}")
        return {'msg': message, 'debug': True}
    
    def _dry_run_preview(self, message: str):
        """Generate dry run preview for debug message."""
        preview = f"[DRY RUN] Would print debug: '{message}'"
        self.context.console.print(f"[cyan]{preview}[/cyan]")
        
        return {
            'dry_run': True,
            'message': message,
            'preview': preview,
            'msg': 'Dry run preview for debug'
        }


def get_builtin_tools() -> Dict[str, callable]:
    """
    Get dictionary of all built-in tools.
    
    Returns:
        Dictionary mapping tool names to AutomationTool classes
    """
    # Return the tool classes that will be instantiated with context
    return {
        'user_input': UserInputTool,
        'complete': CompleteTool,
        'impossible': ImpossibleTool, 
        'debug': DebugTool,
    }


def get_builtin_tool_classes() -> Dict[str, type]:
    """
    Get dictionary of all built-in tool classes.
    
    Returns:
        Dictionary mapping tool names to AutomationTool classes
    """
    return {
        'user_input': UserInputTool,
        'complete': CompleteTool,
        'impossible': ImpossibleTool,
        'debug': DebugTool,
    }
