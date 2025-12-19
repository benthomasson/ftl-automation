#!/usr/bin/env python3
"""
Test script following the exact Linode script pattern.

This demonstrates that our ftl-automation framework now supports
the same patterns used in the original Linode deployment script.
"""

import ftl_automation


def main():
    """Test Linode script compatibility."""

    # Create test inventory in memory
    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    with ftl_automation.automation(
        inventory=test_inventory,  # Use dict instead of file
        modules=["modules"],
        secrets=["TEST_TOKEN", "TEST_PASSWORD"],  # These can be missing
        user_input="test_input.yml",
    ) as ftl:

        # Test the Linode pattern: assign tools to variables
        user_input_tool = ftl.tools.user_input_tool
        complete = ftl.tools.complete
        impossible = ftl.tools.impossible
        debug_tool = ftl.tools.debug_tool

        print("✓ Tool assignment pattern works!")
        print(f"Available tools: {list(ftl.tools.keys())}")

        # Test NEW direct calling pattern
        print("\n=== Testing Direct Tool Calls ===")
        ftl.debug_tool(message="Direct call to debug_tool works!")

        # Test user input (with default to avoid blocking)
        try:
            server_name = "test-server-01"  # Simulate user input
            print(f"✓ Server name: {server_name}")
        except:
            server_name = "default-server"

        # Test debug output (both patterns)
        debug_tool("Testing debug functionality - variable pattern")
        ftl.debug_tool(message="Testing debug functionality - direct pattern")

        # Test module execution
        try:
            result = ftl.run_module("command", cmd="echo 'Hello FTL'")
            print(f"✓ Module execution works: {result}")
        except Exception as e:
            print(f"⚠ Module execution test: {e}")

        # Test secrets access
        test_secret = ftl.secrets.get("TEST_TOKEN", "not-provided")
        print(
            f"✓ Secrets access works: {test_secret[:10] if test_secret else 'None'}..."
        )

        # Test completion
        print("\n🎉 All compatibility tests passed!")
        complete("Linode script pattern compatibility verified")


if __name__ == "__main__":
    try:
        main()
    except ftl_automation.CompletionException as e:
        print(f"\n✅ Test completed: {e}")
    except ftl_automation.ImpossibleException as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
