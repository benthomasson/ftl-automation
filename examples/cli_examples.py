#!/usr/bin/env python3
"""
CLI usage examples for ftl-automation library.

This file contains example command lines and scripts showing
how to use the ftl-automation CLI tool.
"""

import subprocess
import sys
import yaml
import os


def create_test_files():
    """Create test files for CLI examples."""

    # Create simple inventory
    inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    with open("test_inventory.yml", "w") as f:
        yaml.dump(inventory, f)

    # Create a simple tool file
    tool_code = '''
def hello_world(inventory, modules, console, message="Hello World", **kwargs):
    """Simple hello world tool."""
    console.print(f"[green]{message}[/green]")
    return {"message": message}

def system_info(inventory, modules, console, **kwargs):
    """Get basic system info."""
    import platform
    info = {
        "system": platform.system(),
        "node": platform.node(), 
        "release": platform.release()
    }
    console.print(f"[blue]System Info: {info}[/blue]")
    return info
'''

    with open("example_tools.py", "w") as f:
        f.write(tool_code)

    print("Created test files: test_inventory.yml, example_tools.py")


def run_cli_example(cmd, description):
    """Run a CLI example and show output."""
    print(f"\n=== {description} ===")
    print(f"Command: {cmd}")
    print("Output:")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"Exit code: {result.returncode}")
    except Exception as e:
        print(f"Error running command: {e}")


def main():
    """CLI examples demonstration."""

    # Create test files
    create_test_files()

    try:
        print("FTL Automation CLI Examples")
        print("=" * 50)

        # Example 1: Basic module execution
        run_cli_example(
            "ftl-automation --inventory test_inventory.yml --module-name command --module-args 'cmd=echo Hello FTL'",
            "Basic Module Execution",
        )

        # Example 2: Load tools from file
        run_cli_example(
            "ftl-automation --inventory test_inventory.yml --tools-files example_tools.py",
            "Loading Custom Tools",
        )

        # Example 3: Multiple modules directory
        run_cli_example(
            "ftl-automation --inventory test_inventory.yml --modules modules --modules /usr/share/ansible/modules",
            "Multiple Module Directories",
        )

        # Example 4: With extra variables
        run_cli_example(
            "ftl-automation --inventory test_inventory.yml --extra-vars 'greeting=Hello' --extra-vars 'target=World'",
            "With Extra Variables",
        )

        # Example 5: System info gathering
        run_cli_example(
            "ftl-automation --inventory test_inventory.yml --module-name setup --module-args 'gather_subset=min'",
            "System Information Gathering",
        )

        print("\n" + "=" * 50)
        print("Additional CLI usage patterns:")
        print()
        print("# Run a specific command on all hosts:")
        print("ftl-automation -i hosts.yml -n command -a 'cmd=uptime'")
        print()
        print("# Load multiple tool files:")
        print("ftl-automation -i hosts.yml -f tools1.py -f tools2.py")
        print()
        print("# Interactive mode with loaded tools:")
        print("ftl-automation -i hosts.yml -t bash,copy,service")
        print()
        print("# Complex module arguments:")
        print(
            "ftl-automation -i hosts.yml -n service -a 'name=nginx,state=restarted,enabled=yes'"
        )
        print()
        print("# With environment variables:")
        print("MY_VAR=value ftl-automation -i hosts.yml -e MY_VAR=default_value")

    finally:
        # Cleanup
        for file in ["test_inventory.yml", "example_tools.py"]:
            if os.path.exists(file):
                os.remove(file)
        print(f"\nCleaned up test files")


if __name__ == "__main__":
    main()
