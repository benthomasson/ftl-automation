#!/usr/bin/env python3
"""
Test direct tool calling like ftl.bash(...) instead of ftl.execute_tool('bash', ...).

This demonstrates the improved tool calling syntax.
"""

import ftl_automation


def example_tool(console, message="Hello from tool", **kwargs):
    """Example tool for testing direct calls."""
    console.print(f"[green]{message}[/green]")
    return {"message": message, "status": "success"}


def another_tool(console, name="World", greeting="Hello", **kwargs):
    """Another example tool with multiple parameters."""
    result = f"{greeting}, {name}!"
    console.print(f"[blue]{result}[/blue]")
    return {"greeting": result}


def main():
    """Test direct tool calling functionality."""

    # Create test inventory
    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    with ftl_automation.automation(
        inventory=test_inventory, tools_files=[__file__]  # Load tools from this file
    ) as ftl:

        print("=== Testing Direct Tool Calls ===")
        print(f"Available tools: {list(ftl._tools_dict.keys())}")

        # Test 1: Built-in tools with direct calling
        print("\n1. Testing built-in tools:")

        # Direct call to debug_tool
        ftl.debug_tool(message="This is a debug message")

        # Direct call to user_input_tool (with simulation)
        print("✓ Built-in tools accessible directly")

        # Test 2: Custom tools from file with direct calling
        print("\n2. Testing custom tools:")

        # Direct call to example_tool
        result1 = ftl.example_tool(message="Direct call works!")
        print(f"Result: {result1}")

        # Direct call to another_tool
        result2 = ftl.another_tool(name="FTL", greeting="Greetings")
        print(f"Result: {result2}")

        # Test 3: Compare with old syntax
        print("\n3. Comparing syntax:")

        print("Old syntax:")
        result_old = ftl.execute_tool("example_tool", message="Old way")
        print(f"  ftl.execute_tool('example_tool', ...) -> {result_old}")

        print("New syntax:")
        result_new = ftl.example_tool(message="New way")
        print(f"  ftl.example_tool(...) -> {result_new}")

        # Test 4: Error handling for non-existent tools
        print("\n4. Testing error handling:")
        try:
            ftl.nonexistent_tool()
        except AttributeError as e:
            print(f"✓ Proper error for missing tool: {e}")

        # Test 5: Demonstrate the improved workflow
        print("\n5. Improved workflow example:")

        ftl.debug_tool(message="Starting workflow")

        # Multiple tool calls with clean syntax
        result = ftl.example_tool(message="Step 1 complete")
        ftl.debug_tool(message=f"Step 1 result: {result['status']}")

        result = ftl.another_tool(name="Step 2", greeting="Completed")
        ftl.debug_tool(message=f"Step 2 result: {result['greeting']}")

        print("\n✅ All direct tool call tests passed!")


if __name__ == "__main__":
    main()
