#!/usr/bin/env python3
"""
Advanced usage example for ftl-automation library.

This example shows more complex scenarios including error handling,
parallel execution, custom context management, and integration patterns.
"""

import ftl_automation
import asyncio
import yaml
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import tempfile
import os


def deploy_web_server(inventory, modules, console, server_name, **kwargs):
    """Complex deployment tool example."""
    console.print(f"[blue]Starting deployment of {server_name}[/blue]")
    
    steps = [
        ("Updating package cache", "command", {"cmd": "apt update"}),
        ("Installing nginx", "package", {"name": "nginx", "state": "present"}),
        ("Starting nginx service", "service", {"name": "nginx", "state": "started", "enabled": True}),
        ("Creating web directory", "file", {"path": f"/var/www/{server_name}", "state": "directory"}),
        ("Setting permissions", "file", {"path": f"/var/www/{server_name}", "mode": "0755"})
    ]
    
    results = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for step_name, module, args in steps:
            task = progress.add_task(step_name, total=1)
            
            try:
                result = ftl_automation.run_module(
                    inventory=inventory,
                    modules=modules,
                    module_name=module,
                    module_args=args
                )
                results[step_name] = result
                progress.update(task, completed=1)
                console.print(f"[green]✓ {step_name}[/green]")
                
            except Exception as e:
                console.print(f"[red]✗ {step_name}: {e}[/red]")
                results[step_name] = {"error": str(e)}
                progress.update(task, completed=1)
    
    return results


def backup_and_update(inventory, modules, console, service_name, **kwargs):
    """Backup service before updating."""
    console.print(f"[yellow]Backing up and updating {service_name}[/yellow]")
    
    try:
        # Create backup
        backup_result = ftl_automation.run_module(
            inventory=inventory,
            modules=modules,
            module_name="command",
            module_args={"cmd": f"systemctl stop {service_name} && tar -czf /tmp/{service_name}_backup.tar.gz /etc/{service_name}"}
        )
        
        # Update package
        update_result = ftl_automation.run_module(
            inventory=inventory,
            modules=modules,
            module_name="package",
            module_args={"name": service_name, "state": "latest"}
        )
        
        # Restart service
        restart_result = ftl_automation.run_module(
            inventory=inventory,
            modules=modules,
            module_name="service",
            module_args={"name": service_name, "state": "restarted"}
        )
        
        return {
            "backup": backup_result,
            "update": update_result,
            "restart": restart_result
        }
        
    except Exception as e:
        console.print(f"[red]Error during backup/update: {e}[/red]")
        # Attempt rollback
        console.print("[yellow]Attempting rollback...[/yellow]")
        try:
            ftl_automation.run_module(
                inventory=inventory,
                modules=modules,
                module_name="command",
                module_args={"cmd": f"tar -xzf /tmp/{service_name}_backup.tar.gz -C / && systemctl start {service_name}"}
            )
            console.print("[green]Rollback successful[/green]")
        except:
            console.print("[red]Rollback failed![/red]")
        
        raise


def main():
    """Advanced usage examples."""
    
    # Create temporary inventory for demo
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        inventory_data = {
            "all": {
                "hosts": {
                    "localhost": {
                        "ansible_connection": "local"
                    }
                }
            }
        }
        yaml.dump(inventory_data, f)
        inventory_file = f.name
    
    try:
        # Example 1: Complex deployment with progress tracking
        print("=== Complex Deployment Example ===")
        
        with ftl_automation.automation(
            inventory=inventory_file,
            modules=["modules"],
            tools_files=[__file__]
        ) as ftl:
            
            ftl.print("[blue]Starting complex deployment...[/blue]")
            
            result = ftl.execute_tool("deploy_web_server", server_name="myapp")
            ftl.print(f"[green]Deployment result: {len(result)} steps completed[/green]")
        
        
        # Example 2: Error handling and rollback
        print("\n=== Error Handling Example ===")
        
        with ftl_automation.automation(
            inventory=inventory_file,
            modules=["modules"],
            tools_files=[__file__]
        ) as ftl:
            
            try:
                # This might fail on some systems
                result = ftl.execute_tool("backup_and_update", service_name="nonexistent-service")
                ftl.print("[green]Update completed successfully[/green]")
            except Exception as e:
                ftl.print(f"[red]Update failed: {e}[/red]")
        
        
        # Example 3: Custom context with enhanced features
        print("\n=== Custom Context Example ===")
        
        custom_console = Console()
        custom_console.print("[magenta]Using custom console![/magenta]")
        
        with ftl_automation.automation(
            inventory=inventory_file,
            modules=["modules"],
            extra_vars={"environment": "production", "debug": False}
        ) as ftl:
            
            # Override console
            ftl.console = custom_console
            
            # Access extra vars
            ftl.print(f"[cyan]Environment: {ftl.extra_vars.get('environment')}[/cyan]")
            ftl.print(f"[cyan]Debug mode: {ftl.extra_vars.get('debug')}[/cyan]")
            
            # Run commands with custom settings
            result = ftl.run_module("command", cmd="echo 'Custom context working'")
            ftl.print(f"[green]Result: {result}[/green]")
        
        
        # Example 4: Multiple automation contexts
        print("\n=== Multiple Contexts Example ===")
        
        # Production context
        with ftl_automation.automation(
            inventory=inventory_file,
            extra_vars={"env": "prod"}
        ) as prod_ftl:
            
            prod_ftl.print("[red]Production environment[/red]")
            prod_result = prod_ftl.run_module("command", cmd="echo 'prod environment'")
        
        # Development context  
        with ftl_automation.automation(
            inventory=inventory_file,
            extra_vars={"env": "dev"}
        ) as dev_ftl:
            
            dev_ftl.print("[yellow]Development environment[/yellow]") 
            dev_result = dev_ftl.run_module("command", cmd="echo 'dev environment'")
        
        print(f"Prod result: {prod_result}")
        print(f"Dev result: {dev_result}")
        
        
        # Example 5: Resource management and cleanup
        print("\n=== Resource Management Example ===")
        
        class ManagedAutomation:
            """Wrapper class for automation with resource management."""
            
            def __init__(self, **kwargs):
                self.context = None
                self.kwargs = kwargs
                self.resources = []
            
            def __enter__(self):
                self.context = ftl_automation.automation(**self.kwargs).__enter__()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                # Custom cleanup
                for resource in self.resources:
                    try:
                        self.context.run_module("file", path=resource, state="absent")
                        print(f"Cleaned up: {resource}")
                    except:
                        pass
                
                # Close automation context
                if self.context:
                    self.context.__exit__(exc_type, exc_val, exc_tb)
            
            def create_temp_file(self, path):
                """Create a temporary file that will be cleaned up."""
                result = self.context.run_module("file", path=path, state="touch")
                self.resources.append(path)
                return result
            
            def __getattr__(self, name):
                # Delegate to automation context
                return getattr(self.context, name)
        
        with ManagedAutomation(inventory=inventory_file) as managed:
            managed.print("[blue]Using managed automation context[/blue]")
            
            # Create some temp files that will be auto-cleaned
            managed.create_temp_file("/tmp/ftl_test1")
            managed.create_temp_file("/tmp/ftl_test2")
            
            managed.print("[green]Created temporary files[/green]")
            # Files will be automatically cleaned up on exit
    
    finally:
        # Cleanup inventory file
        if os.path.exists(inventory_file):
            os.remove(inventory_file)


if __name__ == "__main__":
    main()