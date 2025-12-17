#!/usr/bin/env python3
"""
Inventory management example for ftl-automation library.

This example shows how to work with inventories, manage hosts,
and execute tasks across different host groups.
"""

import ftl_automation
import yaml
import os


def create_example_inventory():
    """Create an example inventory file."""
    inventory = {
        "all": {
            "children": {
                "webservers": {
                    "hosts": {
                        "web1": {
                            "ansible_host": "192.168.1.10",
                            "ansible_user": "ubuntu"
                        },
                        "web2": {
                            "ansible_host": "192.168.1.11", 
                            "ansible_user": "ubuntu"
                        }
                    },
                    "vars": {
                        "http_port": 80,
                        "server_role": "frontend"
                    }
                },
                "databases": {
                    "hosts": {
                        "db1": {
                            "ansible_host": "192.168.1.20",
                            "ansible_user": "root",
                            "mysql_port": 3306
                        }
                    },
                    "vars": {
                        "server_role": "backend"
                    }
                }
            }
        }
    }
    
    with open("example_inventory.yml", "w") as f:
        yaml.dump(inventory, f, default_flow_style=False)
    
    print("Created example_inventory.yml")
    return "example_inventory.yml"


def main():
    """Inventory management example."""
    
    # Create example inventory
    inventory_file = create_example_inventory()
    
    try:
        # Example 1: Load and inspect inventory
        print("=== Inventory Loading ===")
        
        inventory = ftl_automation.load_inventory(inventory_file)
        print(f"Loaded inventory with {len(inventory)} top-level groups")
        
        # Print inventory structure
        for group_name, group_data in inventory.items():
            print(f"Group: {group_name}")
            if isinstance(group_data, dict) and "children" in group_data:
                for child_name, child_data in group_data["children"].items():
                    print(f"  Child group: {child_name}")
                    if "hosts" in child_data:
                        for host_name in child_data["hosts"]:
                            print(f"    Host: {host_name}")
        
        
        # Example 2: Use inventory in automation context
        print("\n=== Running Tasks on Inventory ===")
        
        with ftl_automation.automation(
            inventory=inventory_file,
            modules=["modules"]
        ) as ftl:
            
            ftl.print("[green]Automation context loaded[/green]")
            ftl.print(f"[blue]Inventory groups: {list(ftl.inventory.keys())}[/blue]")
            
            # Run command on all hosts
            result = ftl.run_module("command", cmd="hostname")
            ftl.print(f"[yellow]Hostname results: {result}[/yellow]")
            
            # Run setup to gather facts
            result = ftl.run_module("setup", gather_subset="min")
            ftl.print("[cyan]Gathered system facts[/cyan]")
            
            # Install package (example)
            result = ftl.run_module("package", name="htop", state="present")
            ftl.print(f"[magenta]Package installation: {result}[/magenta]")
        
        
        # Example 3: Working with localhost
        print("\n=== Localhost Operations ===")
        
        with ftl_automation.automation(inventory="localhost,") as ftl:
            
            # Use localhost inventory
            result = ftl.run_module("command", cmd="whoami")
            ftl.print(f"[green]Current user: {result}[/green]")
            
            # Check system info
            result = ftl.run_module("command", cmd="uname -a")
            ftl.print(f"[blue]System info: {result}[/blue]")
            
            # Create a temporary file
            result = ftl.run_module("file", 
                path="/tmp/ftl_test",
                state="touch"
            )
            ftl.print(f"[yellow]File creation: {result}[/yellow]")
    
    finally:
        # Cleanup
        if os.path.exists(inventory_file):
            os.remove(inventory_file)
            print(f"Cleaned up {inventory_file}")


if __name__ == "__main__":
    main()