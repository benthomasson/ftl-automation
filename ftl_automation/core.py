"""
Core automation functions and context management.
"""

import os
import asyncio
from threading import Thread
from typing import Dict, Any, List, Optional
from contextlib import contextmanager
import faster_than_light as ftl
from .exceptions import CompletionException


def load_inventory(inventory_path: str) -> Dict[str, Any]:
    """Load FTL inventory from file.

    If the inventory file doesn't exist, create an empty one.

    Args:
        inventory_path: Path to inventory file

    Returns:
        Loaded inventory dictionary
    """
    if not os.path.exists(inventory_path):
        # Create an empty inventory file
        dir_path = os.path.dirname(inventory_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(inventory_path, 'w') as f:
            f.write('{}\n')
    
    return ftl.load_inventory(inventory_path)


def load_modules(module_paths: List[str]) -> List[str]:
    """Load FTL modules from paths.

    Args:
        module_paths: List of paths containing modules

    Returns:
        List of module paths (FTL expects module paths, not loaded modules)
    """
    # FTL expects module paths as strings, not loaded module objects
    # Filter to only existing paths
    existing_paths = []
    for path in module_paths:
        if os.path.exists(path):
            existing_paths.append(path)
    return existing_paths


@contextmanager
def automation(
    inventory: Optional[str] = None,
    modules: Optional[List[str]] = None,
    tools: Optional[List[str]] = None,
    tool_packages: Optional[List[str]] = None,
    extra_vars: Optional[Dict[str, Any]] = None,
    secrets: Optional[List[str]] = None,
    user_input: Optional[str] = None,
    dry_run: bool = False,
    auto_discover_modules: bool = False,
    **kwargs
):
    """
    Automation context manager that provides a configured environment.

    Args:
        inventory: Path to inventory file or inventory dict
        modules: List of module paths
        tools: List of tool names to load
        tool_packages: List of package names to search for tools (defaults to ["ftl_tools.tools"])
        extra_vars: Additional variables
        secrets: List of secret names to load from environment
        dry_run: Enable dry run mode (preview changes without executing)
        auto_discover_modules: Automatically discover module directories in common locations
        user_input: Path to user input file
        **kwargs: Additional context variables

    Yields:
        AutomationContext object with loaded resources
    """
    from .context import AutomationContext
    from .tools import load_tools_by_name
    from .builtin_tools import get_builtin_tools
    import os

    print(f"{inventory=}")

    # Load inventory
    if isinstance(inventory, str):
        inventory_file_path = inventory
        inv = load_inventory(inventory)
    elif inventory is None:
        # No inventory needed for local AWS modules
        inventory_file_path = None
        inv = None
    else:
        inventory_file_path = None
        inv = inventory

    # Note: Modules will be handled in AutomationContext with auto-discovery
    # We pass modules to the context which will handle discovery and resolution

    # Load secrets from environment
    secrets_dict = {}
    if secrets:
        for secret_name in secrets:
            secrets_dict[secret_name] = os.environ.get(secret_name)

    # Set default tool packages if none provided
    if tool_packages is None:
        tool_packages = ["ftl_tools.tools"]

    # Set up asyncio event loop for FTL gate cache
    gate_cache = {}
    loop = asyncio.new_event_loop()
    thread = Thread(target=loop.run_forever, daemon=True)
    thread.start()

    # Create context first (without tools) - it will handle module discovery
    context = AutomationContext(
        inventory=inv,
        modules=modules or ["modules"],
        tools={},  # Start empty, will add tools after context creation
        localhost=ftl.localhost,
        extra_vars=extra_vars or {},
        secrets=secrets_dict,
        user_input_file=user_input,
        inventory_file=inventory_file_path,
        tool_packages=tool_packages,
        dry_run=dry_run,
        auto_discover_modules=auto_discover_modules,
        gate_cache=gate_cache,
        loop=loop,
        **kwargs
    )

    # Load tools
    tool_instances = {}
    
    # Add builtin tools (instantiate classes with context)
    builtin_tool_classes = get_builtin_tools()
    for name, tool_class in builtin_tool_classes.items():
        tool_instances[name] = tool_class(context)

    # Load additional tools
    if tools:
        tool_instances.update(load_tools_by_name(tools, context, tool_packages))
    
    # Update context with all loaded tools
    context._tools_dict.update(tool_instances)

    try:
        yield context
    except CompletionException:
        # This is expected - the automation completed successfully
        pass
    finally:
        # Cleanup event loop
        try:
            loop.call_soon_threadsafe(loop.stop)
            thread.join(timeout=1.0)  # Give thread time to stop gracefully
        except:
            pass  # Ignore cleanup errors
        
        # Cleanup if needed
        if hasattr(context, "cleanup"):
            context.cleanup()


def run_module(
    inventory: Dict[str, Any],
    modules: List[str],
    module_name: str,
    module_args: Dict[str, Any],
    gate_cache: Optional[Dict] = None,
    use_gate: bool = False,
    dry_run: bool = False,
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
        dry_run: Enable dry run mode (converted to check_mode for Ansible modules)
        **kwargs: Additional arguments passed to FTL

    Returns:
        Module execution results
    """
    # Convert dry_run to check_mode for Ansible modules
    if dry_run:
        # Create a copy to avoid modifying the original
        module_args = module_args.copy()
        module_args['_ansible_check_mode'] = True
    
    return ftl.run_module_sync(
        inventory,
        modules,
        module_name,
        gate_cache,
        module_args=module_args,
        use_gate=use_gate,
        **kwargs
    )
