"""
Built-in tools for ftl-automation.

These tools provide essential functionality like user input, completion signaling,
and other common automation tasks.
"""

import os
import sys
import yaml
from typing import Dict, Any, Optional
from rich.prompt import Prompt


def user_input_tool(question: str, default: Optional[str] = None, **kwargs) -> str:
    """
    Prompt user for input during automation execution.
    
    Args:
        question: Question to ask the user
        default: Default value if user provides no input
        **kwargs: Additional context (unused but kept for compatibility)
        
    Returns:
        User's input as string
    """
    return Prompt.ask(question, default=default)


def input_tool(prompt: str = "Enter value", **kwargs) -> str:
    """
    Simple input tool for user interaction.
    
    Args:
        prompt: Prompt to show user
        **kwargs: Additional context
        
    Returns:
        User input
    """
    return input(f"{prompt}: ")


class CompletionException(Exception):
    """Exception raised to signal task completion."""
    pass


class ImpossibleException(Exception):
    """Exception raised to signal task is impossible."""
    pass


def complete(message: str = "Task completed successfully", **kwargs) -> None:
    """
    Signal that the automation task has completed successfully.
    
    Args:
        message: Completion message
        **kwargs: Additional context
        
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
    Signal that the automation task is impossible with current tools.
    
    Args:
        reason: Reason why task is impossible
        **kwargs: Additional context
        
    Raises:
        ImpossibleException: Always raised to signal impossibility
    """
    console = kwargs.get('console')
    if console:
        console.print(f"[red]✗ {reason}[/red]")
    else:
        print(f"✗ {reason}")
    
    raise ImpossibleException(reason)


def load_user_input(file_path: str, **kwargs) -> Dict[str, Any]:
    """
    Load user input from YAML file.
    
    Args:
        file_path: Path to YAML file containing user input
        **kwargs: Additional context
        
    Returns:
        Dictionary of loaded user input data
    """
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r') as f:
        return yaml.safe_load(f) or {}


def save_user_input(file_path: str, data: Dict[str, Any], **kwargs) -> None:
    """
    Save user input to YAML file.
    
    Args:
        file_path: Path to save YAML file
        data: Data to save
        **kwargs: Additional context
    """
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def get_secret(secret_name: str, **kwargs) -> Optional[str]:
    """
    Get secret value from environment or context.
    
    Args:
        secret_name: Name of secret to retrieve
        **kwargs: Additional context, may contain 'secrets' dict
        
    Returns:
        Secret value or None if not found
    """
    # First try from context secrets
    secrets = kwargs.get('secrets', {})
    if secret_name in secrets:
        return secrets[secret_name]
    
    # Fall back to environment
    return os.environ.get(secret_name)


def debug_tool(message: str, **kwargs) -> None:
    """
    Print debug message during automation.
    
    Args:
        message: Debug message
        **kwargs: Additional context
    """
    console = kwargs.get('console')
    if console:
        console.print(f"[dim]DEBUG: {message}[/dim]")
    else:
        print(f"DEBUG: {message}")


def get_builtin_tools() -> Dict[str, callable]:
    """
    Get dictionary of all built-in tools.
    
    Returns:
        Dictionary mapping tool names to tool functions
    """
    return {
        'user_input_tool': user_input_tool,
        'input_tool': input_tool,
        'complete': complete,
        'impossible': impossible,
        'load_user_input': load_user_input,
        'save_user_input': save_user_input,
        'get_secret': get_secret,
        'debug_tool': debug_tool,
    }