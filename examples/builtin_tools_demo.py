#!/usr/bin/env python3
"""
Demonstration of builtin tools using both function and AutomationTool interfaces.
"""

import ftl_automation

test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

with ftl_automation.automation(inventory=test_inventory) as ftl:

    # Use built-in tools through the original function interface
    print("\n1. Debug Tool:")
    ftl.debug_tool(message="Starting function-based demo")

    print("\n2. User Input Tool:")
    name = ftl.user_input_tool(question="What's your name?", default="World")

    ftl.debug_tool(message=f"Got name: {name}")

    print(f"\nHello, {name}!")

    print("\n3. Completion:")
    ftl.complete(message="Function-based demo completed successfully")
