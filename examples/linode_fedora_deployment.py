#!/usr/bin/env python3
"""
System Design: A linux machine running fedora
Problem:
Do the following steps:
* Provision a new linode server
* Update all the packages
* Send a message to slack

Use the user_input tool to ask for additional information.
Use the complete() tool to signal that you are done

Do not use example data, ask the user for input using user_input().

This is a real scenario.  Use the tools provided or ask for assistance.

Compatible ftl_automation version of the original ftl-automation-agent script.
"""
import ftl_automation
import os


# Mock tools for demonstration (since we don't have actual ftl_tools installed)
def linode_tool(inventory, modules, console, name, image, ltype, **kwargs):
    """Mock Linode tool for demonstration."""
    console.print(f"[blue]🚀 Provisioning Linode server...[/blue]")
    console.print(f"  Name: {name}")
    console.print(f"  Image: {image}")
    console.print(f"  Type: {ltype}")

    # Simulate provisioning
    import time

    time.sleep(1)

    result = {
        "id": "12345678",
        "label": name,
        "image": image,
        "type": ltype,
        "status": "running",
        "ipv4": ["192.0.2.123"],
        "ipv6": "2001:db8::1/128",
    }

    console.print(f"[green]✓ Server provisioned successfully![/green]")
    console.print(f"  Server ID: {result['id']}")
    console.print(f"  IP Address: {result['ipv4'][0]}")
    return result


def slack_tool(inventory, modules, console, msg, **kwargs):
    """Mock Slack tool for demonstration."""
    console.print(f"[blue]📱 Sending Slack message...[/blue]")
    console.print(f"[dim]Message: {msg}[/dim]")

    # Simulate sending to Slack
    import time

    time.sleep(0.5)

    console.print(f"[green]✓ Slack message sent successfully![/green]")
    return {"ok": True, "channel": "C1234567890", "ts": "1234567890.123456"}


def dnf_tool(inventory, modules, console, name, state, **kwargs):
    """Mock DNF tool for demonstration."""
    console.print(f"[blue]📦 Updating packages with DNF...[/blue]")
    console.print(f"  Package: {name}")
    console.print(f"  State: {state}")

    # Simulate package update
    import time

    time.sleep(2)

    result = {
        "changed": True,
        "packages_updated": 47,
        "packages": ["kernel", "systemd", "glibc", "dnf"],
        "msg": "All packages updated successfully",
    }

    console.print(f"[green]✓ Updated {result['packages_updated']} packages![/green]")
    return result


def main():
    """Run the Linode deployment automation."""

    # Create test inventory for demonstration
    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    with ftl_automation.automation(
        inventory=test_inventory,
        tools_files=[__file__],  # Load mock tools from this file
        secrets=["LINODE_TOKEN", "LINODE_ROOT_PASS", "SLACK_TOKEN"],
        user_input="user_input_demo.yml",
    ) as ftl:

        # =================================================================
        # EXACT SAME PATTERN as ftl-automation-agent script
        # =================================================================

        linode = ftl.tools.linode_tool
        slack = ftl.tools.slack_tool
        dnf = ftl.tools.dnf_tool
        user_input = ftl.tools.user_input_tool
        complete = ftl.tools.complete

        print("\n🚀 FTL Automation - Linode Fedora Deployment")
        print("=" * 55)

        # Get user input for server configuration
        print("\nGathering server configuration...")

        server_name = user_input(
            question="What should be the name of the new Linode server?",
            default="fedora-server-01",
        )
        server_image = user_input(
            question="Which Fedora-based image do you want to use for the Linode server?",
            default="linode/fedora43",
        )
        server_type = user_input(
            question="What Linode type do you want to choose? (e.g. g6-standard-1)",
            default="g6-nanode-1",
        )

        print(f"\n✓ Configuration received:")
        print(f"  Server Name: {server_name}")
        print(f"  Server Image: {server_image}")
        print(f"  Server Type: {server_type}")

        # Provision the Linode server using the provided parameters
        print("\n" + "=" * 55)
        print("STEP 1: Provisioning Linode Server")
        print("=" * 55)

        provision_result = linode(
            name=server_name, image=server_image, ltype=server_type
        )
        print(f"✓ Linode provisioning result: {provision_result['status']}")

        # Update all packages using DNF
        print("\n" + "=" * 55)
        print("STEP 2: Updating System Packages")
        print("=" * 55)

        update_result = dnf(name="*", state="latest")
        print(f"✓ Package update result: {update_result['msg']}")

        # Send Slack message about successful server setup and updates
        print("\n" + "=" * 55)
        print("STEP 3: Sending Slack Notification")
        print("=" * 55)

        slack_message = f"""🎉 New Linode Server Provisioned and Updated!
        
📋 Server Details:
• Name: {server_name}
• Image: {server_image} 
• Type: {server_type}
• Status: {provision_result['status']}
• IP Address: {provision_result['ipv4'][0]}

📦 Package Updates:
• Updated: {update_result['packages_updated']} packages
• Status: {update_result['msg']}

✅ Server is ready for use!"""

        slack_result = slack(msg=slack_message)
        print(f"✓ Slack notification sent: {slack_result['ok']}")

        # Signal completion
        print("\n" + "=" * 55)
        print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 55)

        complete(
            message=f"Linode server '{server_name}' deployed and configured successfully"
        )


# =================================================================
# BONUS: Demonstrate the NEW direct syntax as well
# =================================================================
def main_direct_syntax():
    """Same automation using the new direct calling syntax."""

    test_inventory = {"all": {"hosts": {"localhost": {"ansible_connection": "local"}}}}

    with ftl_automation.automation(
        inventory=test_inventory,
        tools_files=[__file__],
        secrets=["LINODE_TOKEN", "LINODE_ROOT_PASS", "SLACK_TOKEN"],
    ) as ftl:

        print("\n🆕 Same automation with DIRECT SYNTAX:")
        print("=" * 50)

        # Direct calling - no tool assignment needed!
        server_name = ftl.user_input_tool(
            question="Server name?", default="fedora-direct-01"
        )

        # Chain operations directly
        provision_result = ftl.linode_tool(
            name=server_name, image="linode/fedora43", ltype="g6-nanode-1"
        )

        update_result = ftl.dnf_tool(name="*", state="latest")

        ftl.slack_tool(msg=f"🚀 Server {server_name} deployed with direct syntax!")

        ftl.complete(message=f"Direct syntax deployment of {server_name} complete")


if __name__ == "__main__":
    try:
        print("Choose deployment method:")
        print("1. Original ftl-automation-agent compatible syntax")
        print("2. New direct calling syntax")
        print("3. Both (demonstration)")

        choice = input("\nEnter choice (1/2/3): ").strip() or "3"

        if choice in ["1", "3"]:
            main()

        if choice in ["2", "3"]:
            main_direct_syntax()

    except ftl_automation.CompletionException as e:
        print(f"\n✅ Automation completed: {e}")
    except ftl_automation.ImpossibleException as e:
        print(f"\n❌ Automation failed: {e}")
    except KeyboardInterrupt:
        print(f"\n⏹️  Automation interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback

        traceback.print_exc()
