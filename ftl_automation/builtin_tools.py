"""
Built-in tools for ftl-automation.

These tools provide essential functionality like user input, completion signaling,
and other common automation tasks.
"""

import yaml
from typing import Dict, Any, Optional
from rich.prompt import Prompt

from .tool_base import AutomationTool


def user_input_tool(question: str, default: Optional[str] = None, **kwargs) -> str:
    """
    Prompt user for input during automation execution.
    
    Args:
        question: Question to ask the user
        default: Default value if user provides no input
        **kwargs: Additional context (unused by this tool)
    
    Returns:
        User's response as string
    """
    return Prompt.ask(question, default=default)


# Alias for backward compatibility
def input_tool(question: str, default: Optional[str] = None, **kwargs) -> str:
    """
    Alias for user_input_tool for backward compatibility.
    
    Args:
        question: Question to ask the user
        default: Default value if user provides no input
        **kwargs: Additional context (unused by this tool)
    
    Returns:
        User's response as string
    """
    return user_input_tool(question, default, **kwargs)


class CompletionException(Exception):
    """Exception raised to signal successful task completion."""
    pass


class ImpossibleException(Exception):
    """Exception raised to signal that a task is impossible to complete."""
    pass


def complete(message: str = "Task completed successfully", **kwargs) -> None:
    """
    Signal that the automation task has completed successfully.
    
    Args:
        message: Completion message to display
        **kwargs: Additional context including 'console'
    
    Raises:
        CompletionException: Always raised to signal completion
    """
    console = kwargs.get('console')
    if console:
        console.print(f"[green]✓ {message}[/green]")
    else:
        print(f"✓ {message}")
    
    raise CompletionException(message)


def impossible(reason: str = "Task cannot be completed", **kwargs) -> None:
    """
    Signal that the automation task is impossible to complete.
    
    Args:
        reason: Reason why the task is impossible
        **kwargs: Additional context including 'console'
    
    Raises:
        ImpossibleException: Always raised to signal impossibility
    """
    console = kwargs.get('console')
    if console:
        console.print(f"[red]✗ {reason}[/red]")
    else:
        print(f"✗ {reason}")
    
    raise ImpossibleException(reason)


def save_user_input(key: str, value: str, file_path: str = "user_inputs.yaml", **kwargs) -> None:
    """
    Save user input to a YAML file for reuse.
    
    Args:
        key: Key to store the input under
        value: Value to save
        file_path: Path to the YAML file
        **kwargs: Additional context (unused by this tool)
    """
    try:
        # Try to load existing data
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            data = {}
        
        # Add new input
        data[key] = value
        
        # Save back to file
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
            
    except Exception as e:
        print(f"Warning: Could not save user input: {e}")


def load_user_input(key: str, file_path: str = "user_inputs.yaml", **kwargs) -> Optional[str]:
    """
    Load previously saved user input from a YAML file.
    
    Args:
        key: Key to look up
        file_path: Path to the YAML file
        **kwargs: Additional context (unused by this tool)
    
    Returns:
        The saved value, or None if not found
    """
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f) or {}
        return data.get(key)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Warning: Could not load user input: {e}")
        return None


def get_secret(name: str, **kwargs) -> Optional[str]:
    """
    Get a secret value from the automation context.
    
    Args:
        name: Name of the secret
        **kwargs: Additional context including 'secrets'
    
    Returns:
        Secret value or None if not found
    """
    secrets = kwargs.get('secrets', {})
    return secrets.get(name)


def debug_tool(message: str, **kwargs) -> None:
    """
    Print debug message during automation.
    
    Args:
        message: Debug message to print
        **kwargs: Additional context including 'console'
    """
    console = kwargs.get('console')
    if console:
        console.print(f"[dim]DEBUG: {message}[/dim]")
    else:
        print(f"DEBUG: {message}")


# ==============================================================================
# AutomationTool-based classes for advanced use cases
# ==============================================================================

class UserInputTool(AutomationTool):
    """AutomationTool class for user input prompts."""
    
    name = "user_input_tool"
    description = "Prompt user for input during automation execution"
    
    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, question: str, default: Optional[str] = None):
        """Prompt user for input during automation execution."""
        return Prompt.ask(question, default=default)


class CompleteTool(AutomationTool):
    """AutomationTool class for signaling task completion."""
    
    name = "complete"
    description = "Signal that the automation task has completed successfully"
    
    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, message: str = "Task completed successfully"):
        """Signal that the automation task has completed successfully."""
        if self.state["console"]:
            self.state["console"].print(f"[green]✓ {message}[/green]")
        else:
            print(f"✓ {message}")
        
        raise CompletionException(message)


class ImpossibleTool(AutomationTool):
    """AutomationTool class for signaling task impossibility."""
    
    name = "impossible"
    description = "Signal that the automation task is impossible"
    
    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, reason: str = "Task cannot be completed"):
        """Signal that the automation task is impossible."""
        if self.state["console"]:
            self.state["console"].print(f"[red]✗ {reason}[/red]")
        else:
            print(f"✗ {reason}")
        
        raise ImpossibleException(reason)


class DebugTool(AutomationTool):
    """AutomationTool class for debug output."""
    
    name = "debug_tool"
    description = "Print debug message during automation"
    
    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, message: str):
        """Print debug message during automation."""
        if self.state["console"]:
            self.state["console"].print(f"[dim]DEBUG: {message}[/dim]")
        else:
            print(f"DEBUG: {message}")


def get_builtin_tools() -> Dict[str, callable]:
    """
    Get dictionary of all built-in tools.
    
    Returns:
        Dictionary mapping tool names to functions
    """
    return {
        'user_input_tool': user_input_tool,
        'input_tool': input_tool,  # alias
        'complete': complete,
        'impossible': impossible,
        'save_user_input': save_user_input,
        'load_user_input': load_user_input,
        'get_secret': get_secret,
        'debug_tool': debug_tool,
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