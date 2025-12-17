#!/usr/bin/env python3
"""
Demonstration of improved syntax in ftl-automation.

Shows both the original Linode script pattern and the new direct calling syntax.
"""

import ftl_automation


def deploy_service(inventory, modules, console, service_name, **kwargs):
    """Example deployment tool."""
    console.print(f"[blue]Deploying service: {service_name}[/blue]")
    
    # Simulate deployment steps
    steps = [
        "Installing packages",
        "Configuring service", 
        "Starting service",
        "Verifying deployment"
    ]
    
    for step in steps:
        console.print(f"  • {step}...")
    
    console.print(f"[green]✓ Service {service_name} deployed successfully[/green]")
    return {"service": service_name, "status": "deployed"}


def main():
    """Compare syntax patterns."""
    
    test_inventory = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local"
                }
            }
        }
    }
    
    with ftl_automation.automation(
        inventory=test_inventory,
        tools_files=[__file__]
    ) as ftl:
        
        print("🚀 FTL Automation Syntax Demonstration")
        print("=" * 50)
        
        # ========================================
        # ORIGINAL LINODE PATTERN (Still Supported)
        # ========================================
        print("\n📜 ORIGINAL LINODE PATTERN:")
        print("(Exactly like ftl-automation-agent generated scripts)")
        print()
        
        # Assign tools to variables
        user_input_tool = ftl.tools.user_input_tool
        debug_tool = ftl.tools.debug_tool
        deploy_service = ftl.tools.deploy_service
        complete = ftl.tools.complete
        
        # Use the tools
        debug_tool(message="Starting deployment using original pattern")
        
        result = deploy_service(service_name="nginx-original")
        print(f"Result: {result}")
        
        print("✓ Original pattern works perfectly")
        
        # ========================================
        # NEW DIRECT CALLING PATTERN
        # ========================================
        print("\n🆕 IMPROVED DIRECT PATTERN:")
        print("(Cleaner syntax for new scripts)")
        print()
        
        # Direct tool calls - much cleaner!
        ftl.debug_tool(message="Starting deployment using direct pattern")
        
        result = ftl.deploy_service(service_name="nginx-direct")
        print(f"Result: {result}")
        
        print("✓ Direct pattern is more concise")
        
        # ========================================
        # SIDE-BY-SIDE COMPARISON  
        # ========================================
        print("\n⚖️  SYNTAX COMPARISON:")
        print()
        
        print("Original (Linode script style):")
        print("  user_input_tool = ftl.tools.user_input_tool")
        print("  server_name = user_input_tool(question='Enter name:')")
        print("  debug_tool('Deploying...')")
        print()
        
        print("Improved (Direct calling):")
        print("  server_name = ftl.user_input_tool(question='Enter name:')")
        print("  ftl.debug_tool(message='Deploying...')")
        print()
        
        # ========================================
        # MIXED USAGE (Best of Both Worlds)
        # ========================================
        print("🔀 MIXED USAGE EXAMPLE:")
        print("(Use whichever style fits your needs)")
        print()
        
        # Assign frequently used tools
        debug = ftl.tools.debug_tool
        
        # Use direct calls for one-off operations
        ftl.debug_tool(message="Starting mixed usage demo")
        
        # Use variables for tools called multiple times
        debug(message="Step 1 complete")
        debug(message="Step 2 complete") 
        debug(message="Step 3 complete")
        
        # Direct calls for final operations
        result = ftl.deploy_service(service_name="nginx-mixed")
        
        print(f"✓ Mixed usage result: {result['status']}")
        
        # ========================================
        # MIGRATION GUIDE
        # ========================================
        print("\n📖 MIGRATION GUIDE:")
        print()
        print("Existing ftl-automation-agent scripts work unchanged!")
        print("New scripts can use cleaner direct syntax:")
        print()
        print("Before: ftl.execute_tool('tool_name', param=value)")
        print("After:  ftl.tool_name(param=value)")
        print()
        print("Before: tool = ftl.tools.tool_name; tool(param=value)")  
        print("After:  ftl.tool_name(param=value)")
        print()
        
        # Final completion
        print("\n🎉 Demonstration complete!")
        ftl.debug_tool(message="All syntax patterns demonstrated successfully")


if __name__ == "__main__":
    try:
        main()
    except ftl_automation.CompletionException as e:
        print(f"\n✅ Completed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")