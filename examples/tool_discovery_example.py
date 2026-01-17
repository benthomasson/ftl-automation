#!/usr/bin/env python3
"""
Example demonstrating the tool discovery functionality in ftl-automation.

This script shows how to list available tools, filter by category, and get
detailed parameter information to help with automation development.
"""

import ftl_automation

def main():
    """Demonstrate tool discovery capabilities."""
    
    print("🔧 Tool Discovery Example")
    print("=" * 50)
    
    # Use a minimal set of tools for this example
    tools_to_load = ["hostname", "user", "mkdir", "dnf", "slack"]
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load
    ) as ftl:
        
        # 1. Show all available tools in a table
        print("\n1. All Available Tools:")
        print("-" * 30)
        ftl.show_tools()
        
        # 2. Show detailed tool information with parameters
        print("\n2. Detailed Tool Information:")
        print("-" * 35)
        ftl.show_tools(detailed=True)
        
        # 3. Filter by category
        print("\n3. File Management Tools Only:")
        print("-" * 35)
        ftl.show_tools(category='file')
        
        print("\n4. System Administration Tools Only:")
        print("-" * 42)
        ftl.show_tools(category='system')
        
        # 4. Get programmatic access to tool information
        print("\n5. Programmatic Tool Information:")
        print("-" * 38)
        tools_info = ftl.list_available_tools()
        
        print(f"Total tools available: {len(tools_info)}")
        print("Categories found:", set(info['category'] for info in tools_info.values()))
        
        # Show specific tool info
        if 'user' in tools_info:
            user_tool = tools_info['user']
            print(f"\nUser tool details:")
            print(f"  Description: {user_tool['description']}")
            print(f"  Required parameters: {[p['name'] for p in user_tool['parameters'] if p['required']]}")
            print(f"  Optional parameters: {[p['name'] for p in user_tool['parameters'] if not p['required']]}")
        
        # 5. Show available categories
        print("\n6. Available Tool Categories:")
        print("-" * 33)
        categories = set(info['category'] for info in tools_info.values())
        for category in sorted(categories):
            category_tools = ftl.list_available_tools(category=category)
            tool_names = sorted(category_tools.keys())
            print(f"  {category:12} ({len(tool_names):2d} tools): {', '.join(tool_names)}")

if __name__ == "__main__":
    main()