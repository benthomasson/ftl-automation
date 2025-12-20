"""
FTL Automation - Pure Python automation library built on Faster Than Light.

Provides simple, function-based automation capabilities without AI dependencies.
"""

from .core import automation, load_inventory, load_modules, run_module
from .tools import load_tools_by_name
from .context import AutomationContext
from .tool_base import AutomationTool
from .builtin_tools import (
    user_input_tool, input_tool, complete, impossible,
    CompletionException, ImpossibleException,
    UserInputTool, CompleteTool, ImpossibleTool, DebugTool,
    get_builtin_tools, get_builtin_tool_classes,
    save_user_input, load_user_input, get_secret, debug_tool
)

__version__ = "0.1.0"

__all__ = [
    "automation",
    "load_inventory",
    "load_modules",
    "run_module",
    "load_tools_by_name",
    "AutomationContext",
    "AutomationTool",
    "user_input_tool",
    "input_tool",
    "complete",
    "impossible",
    "CompletionException",
    "ImpossibleException",
    "UserInputTool",
    "CompleteTool",
    "ImpossibleTool",
    "DebugTool",
    "get_builtin_tools",
    "get_builtin_tool_classes",
    "save_user_input",
    "load_user_input",
    "get_secret",
    "debug_tool",
]
