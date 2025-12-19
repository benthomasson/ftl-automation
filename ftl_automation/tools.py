"""
Tool loading and execution without AI dependencies.
"""

import os
import importlib.util
import inspect
from typing import Dict, Any, List, Callable, Optional
from .context import AutomationContext


def load_tools_by_name(
    tool_names: List[str], context: AutomationContext
) -> Dict[str, Callable]:
    """
    Load tools by importing them from ftl_tools or other packages.

    Args:
        tool_names: List of tool names to load

    Returns:
        Dictionary of loaded tool functions
    """
    tools = {}

    for tool_name in tool_names:
        try:
            # Try to import from ftl_tools
            module_path = f"ftl_tools.tools.{tool_name}"
            module = importlib.import_module(module_path)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and getattr(obj, 'name', None) == tool_name:
                    tools[f"{tool_name}"] = obj(context)

        except ImportError as e:
            print(e)
            # Try to find the tool elsewhere
            pass

    return tools
