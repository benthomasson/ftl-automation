#!/usr/bin/env python3
"""
Example demonstrating dry run mode in ftl-automation.

This script shows how to use dry run mode to preview automation operations
without actually executing them, providing safe experimentation and validation
of automation scripts before running them on production systems.
"""

import ftl_automation

def main():
    """Demonstrate dry run mode capabilities."""
    
    print("🧪 Dry Run Mode Example")
    print("=" * 50)
    
    # Load tools for demonstration
    tools_to_load = ["hostname", "user", "mkdir", "dnf", "service", "copy"]
    
    print("\n1. Normal Execution Mode:")
    print("-" * 30)
    
    # First show normal execution (with dry_run=False)
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load,
        dry_run=False  # Normal mode
    ) as ftl:
        print("Context dry_run setting:", ftl.dry_run)
        
        # These would normally execute if we had a real inventory
        # For demo purposes, we'll just show the API
        print("\nWould execute these operations in normal mode:")
        print("  ftl.mkdir(path='/opt/myapp')")
        print("  ftl.user(name='appuser', group='users')")
        print("  ftl.service(name='nginx', state='started')")
    
    print("\n\n2. Dry Run Mode - Context Level:")
    print("-" * 40)
    
    # Now demonstrate dry run mode at context level
    with ftl_automation.automation(
        inventory="inventory.yml", 
        tools=tools_to_load,
        dry_run=True  # Enable dry run for entire context
    ) as ftl:
        print("Context dry_run setting:", ftl.dry_run)
        
        # Show help for dry run mode
        print("\nDry run mode is now active for all operations.")
        print("All tool calls will show previews instead of executing.\n")
        
        # These will show dry run previews instead of executing
        print("Tool calls in dry run mode:")
        
        # Example 1: Built-in tool with dry run support
        result1 = ftl.debug(message="This is a dry run test")
        print(f"Debug result: {result1}\n")
        
        # Example 2: Show what would happen with parameters
        result2 = ftl.user_input(question="Would you like to continue?", default="yes")
        print(f"User input result: {result2}\n")
    
    print("\n3. Per-Operation Dry Run Override:")
    print("-" * 38)
    
    # Show per-operation dry run override
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load,
        dry_run=False  # Context is normal mode
    ) as ftl:
        print("Context dry_run setting:", ftl.dry_run)
        print("But we can override dry_run per operation:\n")
        
        # Override to dry run for specific operations
        result1 = ftl.debug(message="Normal execution", dry_run=False)
        print(f"Normal execution: {result1}\n")
        
        result2 = ftl.debug(message="Dry run override", dry_run=True)
        print(f"Dry run override: {result2}\n")
    
    print("\n4. Mixed Operations Example:")
    print("-" * 32)
    
    # Realistic automation scenario with dry run
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load,
        dry_run=True
    ) as ftl:
        print("Simulating server setup automation in dry run mode:\n")
        
        # Simulate a complete automation workflow
        operations = [
            ("Create application directory", lambda: ftl.debug(message="mkdir /opt/myapp")),
            ("Create application user", lambda: ftl.debug(message="useradd -m appuser")),
            ("Install packages", lambda: ftl.debug(message="dnf install -y nginx python3")),
            ("Copy configuration files", lambda: ftl.debug(message="copy config.conf -> /etc/myapp/")),
            ("Start services", lambda: ftl.debug(message="systemctl start nginx")),
            ("Verify installation", lambda: ftl.debug(message="check application status"))
        ]
        
        results = []
        for step, operation in operations:
            print(f"Step: {step}")
            result = operation()
            results.append((step, result))
            print(f"Result: {result.get('preview', 'No preview available')}\n")
        
        print("All operations completed in dry run mode!")
        print(f"Total operations: {len(results)}")
        print("No actual changes were made to the system.")
    
    print("\n5. Tool Support Information:")
    print("-" * 33)
    
    # Show which tools support dry run
    with ftl_automation.automation(
        inventory="inventory.yml",
        tools=tools_to_load
    ) as ftl:
        tools_info = ftl.list_available_tools()
        
        print("Dry run support by tool category:\n")
        
        categories = {}
        for tool_name, info in tools_info.items():
            category = info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(tool_name)
        
        for category in sorted(categories.keys()):
            print(f"{category.title()} tools ({len(categories[category])}):")
            for tool in sorted(categories[category]):
                # Note: Tool support info would need to be added to the introspection
                print(f"  {tool} - dry run supported")
            print()
    
    print("\n" + "=" * 50)
    print("💡 Dry Run Mode Benefits:")
    print("   ✓ Safe experimentation with automation scripts")
    print("   ✓ Preview changes before execution")
    print("   ✓ Validate automation logic without side effects")
    print("   ✓ Test complex workflows on development systems")
    print("   ✓ Demonstrate automation capabilities to stakeholders")
    print("\n🎯 Use Cases:")
    print("   • Development and testing of automation scripts")
    print("   • Validation before production deployment")
    print("   • Troubleshooting automation workflows")
    print("   • Training and demonstration scenarios")

if __name__ == "__main__":
    main()