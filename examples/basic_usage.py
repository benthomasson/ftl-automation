#!/usr/bin/env python3
"""
Basic usage example for ftl-automation library.

This example shows how to use the automation context manager to run
basic FTL modules and execute automation tasks.
"""

import ftl_automation


def main():
    """Basic automation example."""
    
    # Example 1: Using automation context manager
    print("=== Basic Automation Context ===")
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        modules=["modules"]
    ) as ftl:
        
        # Print available resources
        ftl.print(f"[green]Inventory loaded: {len(ftl.inventory)} groups[/green]")
        ftl.print(f"[blue]Available modules: {len(ftl.modules)}[/blue]")
        
        # Run a simple command module
        result = ftl.run_module("command", cmd="uptime")
        ftl.print(f"[yellow]Uptime result: {result}[/yellow]")
        
        # Run another command to check disk space
        result = ftl.run_module("command", cmd="df -h")
        ftl.print(f"[cyan]Disk space: {result}[/cyan]")


    # Example 2: Loading inventory and modules directly
    print("\n=== Direct Module Execution ===")
    
    inventory = ftl_automation.load_inventory("inventory.yml")
    modules = ftl_automation.load_modules(["modules"])
    
    # Execute module directly without context
    result = ftl_automation.run_module(
        inventory=inventory,
        modules=modules,
        module_name="setup",
        module_args={"gather_subset": "network"}
    )
    print(f"Setup module result: {result}")


if __name__ == "__main__":
    main()