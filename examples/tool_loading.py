#!/usr/bin/env python3
"""
Tool loading example for ftl-automation library.

This example demonstrates how to load and use custom tools
with the automation framework.
"""

import ftl_automation


# Example custom tool function
def check_service_status(inventory, modules, console, service_name, **kwargs):
    """Custom tool to check service status."""
    console.print(f"[blue]Checking status of service: {service_name}[/blue]")
    
    # Use FTL to check service status
    result = ftl_automation.run_module(
        inventory=inventory,
        modules=modules,
        module_name="service",
        module_args={"name": service_name, "state": "started"}
    )
    
    console.print(f"[green]Service {service_name} status: {result}[/green]")
    return result


def restart_service(inventory, modules, console, service_name, **kwargs):
    """Custom tool to restart a service."""
    console.print(f"[yellow]Restarting service: {service_name}[/yellow]")
    
    # Stop service
    stop_result = ftl_automation.run_module(
        inventory=inventory,
        modules=modules, 
        module_name="service",
        module_args={"name": service_name, "state": "stopped"}
    )
    
    # Start service
    start_result = ftl_automation.run_module(
        inventory=inventory,
        modules=modules,
        module_name="service", 
        module_args={"name": service_name, "state": "started"}
    )
    
    console.print(f"[green]Service {service_name} restarted[/green]")
    return {"stop": stop_result, "start": start_result}


def main():
    """Tool loading example."""
    
    # Example 1: Load tools from this file
    print("=== Loading Tools from File ===")
    
    tools = ftl_automation.load_tools_from_files([__file__])
    print(f"Loaded tools: {list(tools.keys())}")
    
    
    # Example 2: Use tools in automation context
    print("\n=== Using Custom Tools ===")
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        modules=["modules"],
        tools_files=[__file__]  # Load tools from this file
    ) as ftl:
        
        # Execute custom tool
        ftl.execute_tool("check_service_status", service_name="nginx")
        
        # Execute another custom tool  
        ftl.execute_tool("restart_service", service_name="apache2")
        
        # Access tool directly
        check_tool = ftl.get_tool("check_service_status")
        if check_tool:
            result = check_tool(
                inventory=ftl.inventory,
                modules=ftl.modules,
                console=ftl.console,
                service_name="ssh"
            )
    
    
    # Example 3: Load tools by name (if available in ftl_tools)
    print("\n=== Loading Tools by Name ===")
    
    try:
        tools = ftl_automation.load_tools_by_name(["bash", "copy", "service"])
        print(f"Loaded standard tools: {list(tools.keys())}")
    except Exception as e:
        print(f"Could not load standard tools: {e}")


if __name__ == "__main__":
    main()