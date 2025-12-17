"""
Core automation functions and context management.
"""

import os
from typing import Dict, Any, List, Optional
from contextlib import contextmanager
import faster_than_light as ftl


def load_inventory(inventory_path: str) -> Dict[str, Any]:
    """Load FTL inventory from file.
    
    Args:
        inventory_path: Path to inventory file
        
    Returns:
        Loaded inventory dictionary
    """
    return ftl.load_inventory(inventory_path)


def load_modules(module_paths: List[str]) -> Dict[str, Any]:
    """Load FTL modules from paths.
    
    Args:
        module_paths: List of paths containing modules
        
    Returns:
        Dictionary of loaded modules
    """
    modules = {}
    for path in module_paths:
        if os.path.exists(path):
            # Add logic to load modules from path
            # This would need to be implemented based on FTL's module loading
            pass
    return modules


@contextmanager
def automation(
    inventory: str,
    modules: Optional[List[str]] = None,
    tools: Optional[List[str]] = None,
    tools_files: Optional[List[str]] = None,
    extra_vars: Optional[Dict[str, Any]] = None,
    **kwargs
):
    """
    Automation context manager that provides a configured environment.
    
    Args:
        inventory: Path to inventory file or inventory dict
        modules: List of module paths
        tools: List of tool names to load
        tools_files: List of tool files to load
        extra_vars: Additional variables
        **kwargs: Additional context variables
        
    Yields:
        AutomationContext object with loaded resources
    """
    from .context import AutomationContext
    from .tools import load_tools_from_files, load_tools_by_name
    
    # Load inventory
    if isinstance(inventory, str):
        inv = load_inventory(inventory)
    else:
        inv = inventory
        
    # Load modules
    mods = load_modules(modules or ['modules'])
    
    # Load tools
    tool_instances = {}
    if tools_files:
        tool_instances.update(load_tools_from_files(tools_files))
    if tools:
        tool_instances.update(load_tools_by_name(tools))
    
    # Create context
    context = AutomationContext(
        inventory=inv,
        modules=mods,
        tools=tool_instances,
        localhost=ftl.localhost,
        extra_vars=extra_vars or {},
        **kwargs
    )
    
    try:
        yield context
    finally:
        # Cleanup if needed
        if hasattr(context, 'cleanup'):
            context.cleanup()


def run_module(
    inventory: Dict[str, Any],
    modules: Dict[str, Any], 
    module_name: str,
    module_args: Dict[str, Any],
    gate_cache: Optional[Dict] = None,
    use_gate: bool = False,
    **kwargs
) -> Any:
    """
    Execute an FTL module with given parameters.
    
    Args:
        inventory: FTL inventory
        modules: Available modules
        module_name: Name of module to run
        module_args: Arguments for the module
        gate_cache: Optional gate cache for connection reuse
        use_gate: Whether to use FTL gates
        **kwargs: Additional arguments passed to FTL
        
    Returns:
        Module execution results
    """
    return ftl.run_module_sync(
        inventory,
        modules,
        module_name,
        gate_cache,
        module_args=module_args,
        use_gate=use_gate,
        **kwargs
    )