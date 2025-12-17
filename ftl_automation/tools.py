"""
Tool loading and execution without AI dependencies.
"""

import os
import importlib.util
import inspect
from typing import Dict, Any, List, Callable, Optional


def load_tool_from_file(file_path: str) -> Dict[str, Callable]:
    """
    Load tool functions from a Python file.
    
    Args:
        file_path: Path to Python file containing tool functions
        
    Returns:
        Dictionary mapping tool names to functions
    """
    tools = {}
    
    # Load module from file
    spec = importlib.util.spec_from_file_location("tool_module", file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find all functions in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith('_'):
                tools[name] = obj
    
    return tools


def load_tools_from_files(file_paths: List[str]) -> Dict[str, Callable]:
    """
    Load tools from multiple files.
    
    Args:
        file_paths: List of paths to Python files
        
    Returns:
        Dictionary of all loaded tools
    """
    all_tools = {}
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            tools = load_tool_from_file(file_path)
            all_tools.update(tools)
    
    return all_tools


def load_tools_by_name(tool_names: List[str]) -> Dict[str, Callable]:
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
            
            # Look for functions in the module
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    tools[f"{tool_name}_{name}"] = obj
                    
        except ImportError:
            # Try to find the tool elsewhere
            pass
    
    return tools


def get_function_signature(func: Callable) -> Dict[str, Any]:
    """
    Get the signature information for a function.
    
    Args:
        func: Function to analyze
        
    Returns:
        Dictionary with signature information
    """
    sig = inspect.signature(func)
    
    parameters = {}
    for name, param in sig.parameters.items():
        param_info = {
            'name': name,
            'required': param.default == inspect.Parameter.empty,
            'default': param.default if param.default != inspect.Parameter.empty else None
        }
        
        # Try to get type annotation
        if param.annotation != inspect.Parameter.empty:
            param_info['type'] = param.annotation
            
        parameters[name] = param_info
    
    return {
        'parameters': parameters,
        'doc': func.__doc__,
        'name': func.__name__
    }


def execute_tool(
    tool_func: Callable,
    inventory: Dict[str, Any],
    modules: Dict[str, Any],
    console: Optional[Any] = None,
    **kwargs
) -> Any:
    """
    Execute a tool function with the automation context.
    
    Args:
        tool_func: The tool function to execute
        inventory: FTL inventory
        modules: Available modules  
        console: Rich console for output
        **kwargs: Arguments to pass to the tool
        
    Returns:
        Tool execution result
    """
    if console:
        console.print(f"[blue]Executing tool: {tool_func.__name__}[/blue]")
    
    # Execute the tool function
    result = tool_func(
        inventory=inventory,
        modules=modules, 
        console=console,
        **kwargs
    )
    
    if console:
        console.print(f"[green]Tool completed: {tool_func.__name__}[/green]")
        
    return result


def load_tool(tool_identifier: str) -> Optional[Callable]:
    """
    Load a single tool by file path or name.
    
    Args:
        tool_identifier: Either file path or tool name
        
    Returns:
        Loaded tool function or None
    """
    if os.path.exists(tool_identifier):
        # Load from file
        tools = load_tool_from_file(tool_identifier)
        return list(tools.values())[0] if tools else None
    else:
        # Load by name
        tools = load_tools_by_name([tool_identifier])
        return list(tools.values())[0] if tools else None