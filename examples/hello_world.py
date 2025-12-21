#!/usr/bin/env python3
"""
Hello World Example

The simplest possible ftl-automation example.
This shows the basic pattern of using the automation context manager
with builtin tools on localhost.
"""

import ftl_automation


def main():
    print("👋 Hello World - FTL Automation")
    print("=" * 40)
    
    # Create a simple localhost inventory
    localhost = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local"
                }
            }
        }
    }
    
    # Use the automation context manager
    with ftl_automation.automation(inventory=localhost) as ftl:
        
        # Use the builtin debug tool
        ftl.debug(message="Hello from ftl-automation!")
        
        # Show completion
        ftl.complete(message="Hello world example completed successfully!")


if __name__ == "__main__":
    main()
