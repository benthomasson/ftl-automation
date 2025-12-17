"""
Simple CLI for FTL automation without AI dependencies.
"""

import click
from typing import List
from .core import automation, run_module


@click.command()
@click.option("--inventory", "-i", default="inventory.yml", help="Inventory file path")
@click.option("--modules", "-m", multiple=True, default=["modules"], help="Module directories")
@click.option("--tools", "-t", multiple=True, help="Tools to load")
@click.option("--tools-files", "-f", multiple=True, help="Tool files to load")
@click.option("--module-name", "-n", help="Module name to execute")
@click.option("--module-args", "-a", help="Module arguments as key=value pairs")
@click.option("--extra-vars", "-e", multiple=True, help="Extra variables as key=value")
def main(
    inventory: str,
    modules: List[str], 
    tools: List[str],
    tools_files: List[str],
    module_name: str,
    module_args: str,
    extra_vars: List[str]
):
    """Simple FTL automation CLI."""
    
    # Parse extra vars
    parsed_extra_vars = {}
    for var in extra_vars:
        if '=' in var:
            key, value = var.split('=', 1)
            parsed_extra_vars[key] = value
    
    # Parse module args
    parsed_module_args = {}
    if module_args:
        for arg in module_args.split(','):
            if '=' in arg:
                key, value = arg.split('=', 1)
                parsed_module_args[key] = value
    
    with automation(
        inventory=inventory,
        modules=list(modules),
        tools=list(tools),
        tools_files=list(tools_files),
        extra_vars=parsed_extra_vars
    ) as ftl:
        
        if module_name:
            # Execute a specific module
            result = ftl.run_module(module_name, **parsed_module_args)
            ftl.print(f"Module execution result: {result}")
        else:
            # Interactive mode
            ftl.print("[green]FTL Automation ready![/green]")
            ftl.print(f"Available tools: {list(ftl.tools.keys())}")
            ftl.print(f"Inventory loaded: {len(ftl.inventory)} groups")


if __name__ == "__main__":
    main()