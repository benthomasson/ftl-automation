#!/usr/bin/env python3
"""
Module Auto-Discovery Example

Demonstrates the automatic module discovery feature that finds 
module directories in common locations without manual specification.
"""

import ftl_automation


def basic_auto_discovery():
    """Basic example of auto-discovery."""
    print("=== Basic Auto-Discovery ===")
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        auto_discover_modules=True,  # Enable auto-discovery
        tools=["debug", "user_input"]
    ) as ftl:
        print(f"\nAuto-discovered {len(ftl.modules)} module directories:")
        for module_path in ftl.modules:
            print(f"  - {module_path}")
        
        ftl.debug(message="Auto-discovery found these modules automatically!")


def manual_plus_discovery():
    """Combine manual modules with auto-discovery."""
    print("\n=== Manual + Auto-Discovery ===")
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        modules=["./custom_modules"],  # Manual modules
        auto_discover_modules=True,    # Plus auto-discovery
        tools=["debug"]
    ) as ftl:
        print(f"\nTotal modules (manual + discovered): {len(ftl.modules)}")
        for module_path in ftl.modules:
            print(f"  - {module_path}")
        
        ftl.debug(message="Combined manual and auto-discovered modules!")


def discovery_for_multi_project_environments():
    """Show how discovery helps in multi-project environments."""
    print("\n=== Multi-Project Environment Discovery ===")
    
    # This is particularly useful when working with multiple related projects
    # like ftl-automation, ftl-tools, ftl-aws-tools, minecraft servers, etc.
    
    with ftl_automation.automation(
        inventory="inventory.yml",
        auto_discover_modules=True,
        tools=["debug"]
    ) as ftl:
        print("\nDiscovered module search patterns:")
        print("  ./modules           - Current directory")
        print("  ../*/modules        - Sibling projects") 
        print("  ../../*/modules     - Parent level projects")
        print("  ~/.ftl/modules      - User modules")
        
        print(f"\nFound modules in these locations:")
        for module_path in ftl.modules:
            print(f"  - {module_path}")
        
        # Now you can use modules from any of these projects without
        # manually specifying paths!
        ftl.debug(message="Multi-project module discovery complete!")


if __name__ == "__main__":
    print("FTL-Automation Module Auto-Discovery Examples")
    print("=" * 50)
    
    print("\nModule auto-discovery automatically finds module directories in:")
    print("- Current project: ./modules")
    print("- Sibling projects: ../*/modules")  
    print("- Parent projects: ../../*/modules")
    print("- User modules: ~/.ftl/modules")
    print("\nThis eliminates hardcoded relative paths and fragile module loading!")
    
    try:
        basic_auto_discovery()
        manual_plus_discovery() 
        discovery_for_multi_project_environments()
        
        print(f"\n✅ Module auto-discovery examples completed!")
        print("\nKey benefits:")
        print("- No more hardcoded '../project/modules' paths")
        print("- Automatically finds modules from related projects")
        print("- Works from any directory in your project structure")
        print("- Combines well with manual module specification")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("\nNote: This example requires an inventory.yml file to run")
        print("Create a basic inventory file or use an existing project")