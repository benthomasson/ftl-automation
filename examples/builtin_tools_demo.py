#!/usr/bin/env python3
"""
Demonstration of builtin tools using both function and AutomationTool interfaces.
"""

import ftl_automation


def demo_function_based_tools():
    """Demo the original function-based builtin tools."""

    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    print("🔧 Function-Based Builtin Tools Demo")
    print("=" * 50)

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


def demo_class_based_tools():
    """Demo the new AutomationTool-based builtin tools."""

    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    print("\n🏗️  AutomationTool-Based Builtin Tools Demo")
    print("=" * 55)

    with ftl_automation.automation(inventory=test_inventory) as ftl:

        # Create tool class instances with AutomationContext
        debug_tool = ftl_automation.DebugTool(ftl)
        user_input_tool = ftl_automation.UserInputTool(ftl)
        complete_tool = ftl_automation.CompleteTool(ftl)

        print("\n1. Debug Tool (Class-based):")
        debug_tool(message="Starting class-based demo")

        print("\n2. User Input Tool (Class-based):")
        location = user_input_tool(question="Where are you from?", default="Earth")

        debug_tool(message=f"Got location: {location}")

        print(f"\nGreetings from {location}!")

        print("\n3. Completion (Class-based):")
        complete_tool(message="Class-based demo completed successfully")


def demo_mixed_usage():
    """Demo mixing function and class approaches."""

    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    print("\n🔀 Mixed Usage Demo")
    print("=" * 30)

    with ftl_automation.automation(inventory=test_inventory) as ftl:

        # Mix function-based and class-based tools
        ftl.debug_tool(message="Using function-based debug")

        # Create a class instance for repeated use
        user_input = ftl_automation.UserInputTool(ftl)

        print("\nGathering information...")
        hobby = user_input(
            question="What's your favorite hobby?", default="Programming"
        )
        food = user_input(question="What's your favorite food?", default="Pizza")

        ftl.debug_tool(message=f"Hobby: {hobby}, Food: {food}")

        print(f"\nNice! {hobby} and {food} are great choices!")

        ftl.complete(message="Mixed usage demo completed")


if __name__ == "__main__":
    try:
        print("🎯 FTL Automation Builtin Tools Demonstration")
        print("=" * 55)

        demo_function_based_tools()

    except ftl_automation.CompletionException as e:
        print(f"✅ Demo 1 completed: {e}")

    try:
        demo_class_based_tools()

    except ftl_automation.CompletionException as e:
        print(f"✅ Demo 2 completed: {e}")

    try:
        demo_mixed_usage()

    except ftl_automation.CompletionException as e:
        print(f"✅ Demo 3 completed: {e}")

    print("\n🎉 All demos completed successfully!")
    print("\nKey Benefits:")
    print("• Function-based: Simple, direct usage")
    print("• Class-based: Reusable instances, state management")
    print("• Mixed: Best of both worlds for different use cases")
