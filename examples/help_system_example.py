#!/usr/bin/env python3
"""
Example demonstrating the integrated help system in ftl-automation.

This script shows how to use the help() function to get detailed information
about tools, parameters, and usage examples during runtime.
"""

import ftl_automation

def main():
    """Demonstrate the help system capabilities."""
    
    print("📚 Help System Example")
    print("=" * 50)
    
    # Load a diverse set of tools to demonstrate help functionality
    tools_to_load = ["mkdir", "user", "service", "dnf", "slack", "get_url", "firewalld"]
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load
    ) as ftl:
        
        # 1. General help - overview of all available tools
        print("\n1. General Help (ftl.help()):")
        print("-" * 40)
        ftl.help()
        
        # 2. Specific tool help with detailed parameters and examples
        print("\n\n2. Specific Tool Help (ftl.help('mkdir')):")
        print("-" * 50)
        ftl.help('mkdir')
        
        print("\n3. Complex Tool Help (ftl.help('user')):")
        print("-" * 45)
        ftl.help('user')
        
        print("\n4. Tool with Optional Parameters (ftl.help('slack')):")
        print("-" * 58)
        ftl.help('slack')
        
        # 3. Category help - show all tools in a specific category
        print("\n\n5. Category Help (ftl.help(category='file')):")
        print("-" * 52)
        ftl.help(category='file')
        
        print("\n6. System Tools Category (ftl.help(category='system')):")
        print("-" * 60)
        ftl.help(category='system')
        
        # 4. Error handling - tool not found
        print("\n\n7. Tool Not Found Error Handling:")
        print("-" * 40)
        ftl.help('nonexistent_tool')
        
        # 5. Similar tool suggestions
        print("\n8. Similar Tool Suggestions:")
        print("-" * 35)
        ftl.help('mkdir_dir')  # Should suggest 'mkdir'
        
        # 6. Invalid category
        print("\n9. Invalid Category Error Handling:")
        print("-" * 42)
        ftl.help(category='nonexistent_category')
        
        print("\n" + "=" * 50)
        print("💡 Help System Features Demonstrated:")
        print("   ✓ General help overview")
        print("   ✓ Specific tool help with parameters table")
        print("   ✓ Realistic usage examples")
        print("   ✓ Category-based help")
        print("   ✓ Error handling with suggestions")
        print("   ✓ Tool discovery and navigation")

if __name__ == "__main__":
    main()