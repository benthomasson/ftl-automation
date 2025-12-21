#!/usr/bin/env python3
"""
Server Provisioning Example

Demonstrates how to use ftl-automation for cloud server provisioning.
This example shows:
- Creating cloud instances using API tools
- Dynamic inventory generation
- Basic server configuration
- User and SSH key management
"""

import ftl_automation
import os


def create_test_inventory():
    """Create a test inventory for local demonstration"""
    return {
        "all": {
            "hosts": {
                "test-server": {
                    "ansible_connection": "local",
                    "ansible_host": "127.0.0.1",
                    "ansible_user": "root",
                    "host_name": "test-server-1"
                }
            }
        }
    }


def main():
    print("🚀 Server Provisioning Example")
    print("=" * 50)
    
    # For this example, we'll use a test inventory
    # In production, you would use actual cloud provider APIs
    test_inventory = create_test_inventory()
    
    with ftl_automation.automation(
        inventory=test_inventory,
        tools=[
            "hostname",
            "user", 
            "authorized_key",
            "service",
            "lineinfile",
            "dnf"
        ],
        tool_packages=["ftl_tools.tools"],
        modules=("modules",),
        secrets=["SSH_PUBLIC_KEY"]  # Would contain actual secrets in production
    ) as ftl:
        
        print("\n📋 Step 1: System Information")
        print("-" * 30)
        
        # Check current system info
        result = ftl.run_module("setup", {})
        if result.get("changed"):
            print("✅ System facts gathered")
        
        print("\n🏷️  Step 2: Set Hostname") 
        print("-" * 30)
        
        # Set hostname (demonstration only for local)
        hostname_result = ftl.hostname(name="test-server-1")
        if hostname_result.get("changed"):
            print("✅ Hostname updated")
        else:
            print("ℹ️  Hostname already correct")
        
        print("\n👤 Step 3: Create User Account")
        print("-" * 30)
        
        # Create a user account with sudo access
        user_result = ftl.user(
            name="deployuser",
            shell="/bin/bash",
            groups="wheel",
            create_home=True
        )
        if user_result.get("changed"):
            print("✅ User 'deployuser' created")
        else:
            print("ℹ️  User 'deployuser' already exists")
        
        print("\n🔐 Step 4: SSH Key Setup")
        print("-" * 30)
        
        # Add SSH public key (in production, use actual key file)
        try:
            auth_result = ftl.authorized_key(
                user="deployuser",
                key="ssh-rsa AAAAB3NzaC1yc2EXAMPLE... demo@example.com",
                state="present"
            )
            if auth_result.get("changed"):
                print("✅ SSH key added for deployuser")
            else:
                print("ℹ️  SSH key already present")
        except Exception as e:
            print(f"⚠️  SSH key setup skipped: {e}")
        
        print("\n🔒 Step 5: SSH Security Configuration")
        print("-" * 30)
        
        # Disable password authentication
        try:
            ssh_config_result = ftl.lineinfile(
                path="/etc/ssh/sshd_config",
                line="PasswordAuthentication no",
                regexp=r"^#?PasswordAuthentication",
                backup=True
            )
            if ssh_config_result.get("changed"):
                print("✅ Password authentication disabled")
            else:
                print("ℹ️  Password authentication already disabled")
        except Exception as e:
            print(f"⚠️  SSH config update skipped: {e}")
        
        print("\n🔄 Step 6: Update System Packages")
        print("-" * 30)
        
        # Update system packages
        try:
            update_result = ftl.dnf(name="*", state="latest")
            if update_result.get("changed"):
                print("✅ System packages updated")
            else:
                print("ℹ️  System packages already up to date")
        except Exception as e:
            print(f"⚠️  Package update skipped: {e}")
        
        print("\n✨ Server provisioning completed!")
        print("=" * 50)
        
        # In a real scenario, you might:
        # - Install monitoring agents
        # - Configure firewalls
        # - Set up log forwarding
        # - Install security updates
        # - Configure backup schedules


if __name__ == "__main__":
    main()