"""
FTL Automation - Pure Python automation library built on Faster Than Light.

Provides simple, function-based automation capabilities without AI dependencies.
"""

from .core import automation, load_inventory, load_modules, run_module
from .tools import load_tool, execute_tool, load_tools_from_files, load_tools_by_name
from .context import AutomationContext
from .builtin_tools import (
    user_input_tool, input_tool, complete, impossible,
    CompletionException, ImpossibleException
)

__version__ = "0.1.0"

__all__ = [
    "automation",
    "load_inventory", 
    "load_modules",
    "run_module",
    "load_tool",
    "execute_tool",
    "load_tools_from_files",
    "load_tools_by_name", 
    "AutomationContext",
    "user_input_tool",
    "input_tool", 
    "complete",
    "impossible",
    "CompletionException",
    "ImpossibleException"
]