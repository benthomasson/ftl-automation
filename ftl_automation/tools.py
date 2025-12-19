"""
Tool loading and execution without AI dependencies.
"""

import os
import importlib.util
import inspect
from typing import Dict, Any, List, Callable, Optional
from .context import AutomationContext


def load_tools_by_name(
    tool_names: List[str], 
    context: AutomationContext,
    tool_packages: Optional[List[str]] = None
) -> Dict[str, Callable]:
    """
    Load tools by importing them from specified packages.

    Args:
        tool_names: List of tool names to load
        context: AutomationContext instance
        tool_packages: List of package names to search for tools (defaults to ["ftl_tools.tools"])

    Returns:
        Dictionary of loaded tool functions
    """
    tools = {}
    
    # Set default tool packages if none provided
    if tool_packages is None:
        tool_packages = ["ftl_tools.tools"]

    for tool_name in tool_names:
        tool_found = False
        
        # Try each package until we find the tool
        for package in tool_packages:
            try:
                module_path = f"{package}.{tool_name}"
                module = importlib.import_module(module_path)

                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and getattr(obj, "name", None) == tool_name:
                        tools[f"{tool_name}"] = obj(context)
                        tool_found = True
                        break
                
                if tool_found:
                    break

            except ImportError as e:
                # Continue to next package
                continue
        
        if not tool_found:
            print(f"Warning: Tool '{tool_name}' not found in any of the specified packages: {tool_packages}")

    return tools
