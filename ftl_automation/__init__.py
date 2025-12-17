"""
FTL Automation - Pure Python automation library built on Faster Than Light.

Provides simple, function-based automation capabilities without AI dependencies.
"""

from .core import automation, load_inventory, load_modules, run_module
from .tools import load_tool, execute_tool, load_tools_from_files, load_tools_by_name
from .context import AutomationContext

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
    "AutomationContext"
]