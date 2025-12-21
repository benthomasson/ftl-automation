#!/usr/bin/env python3
"""
System Setup Example

Demonstrates common system administration tasks using ftl-automation.
This example shows:
- User management and group assignment
- SSH configuration and security hardening
- Package installation and management
- Service management
- File system operations
"""

import ftl_automation


def main():
    print("⚙️  System Setup Example")
    print("=" * 50)
    
    # Use localhost for demonstration
    localhost_inventory = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local",
                    "ansible_host": "127.0.0.1"
                }
            }
        }
    }
    
    with ftl_automation.automation(
        inventory=localhost_inventory,
        tools=[
            "user",
            "authorized_key", 
            "lineinfile",
            "service",
            "dnf",
            "file",
            "copy",
            "command"
        ],
        tool_packages=["ftl_tools.tools"],
        modules=("modules",)
    ) as ftl:
        
        print("\n👥 Step 1: User Management")
        print("-" * 30)
        
        # Create system users
        users_to_create = [
            {"name": "webuser", "group": "nginx", "shell": "/bin/bash"},
            {"name": "dbuser", "group": "mysql", "shell": "/bin/bash"},
            {"name": "admin", "groups": "wheel", "shell": "/bin/bash"}
        ]
        
        for user_config in users_to_create:
            try:
                result = ftl.user(**user_config)
                status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
                print(f"{status}: {user_config['name']}")
            except Exception as e:
                print(f"⚠️  Failed to create {user_config['name']}: {e}")
        
        print("\n📦 Step 2: Package Management")
        print("-" * 30)
        
        # Install essential packages
        essential_packages = [
            "git", "htop", "tmux", "vim", "wget", "curl"
        ]
        
        for package in essential_packages:
            try:
                result = ftl.dnf(name=package, state="present")
                status = "✅ Installed" if result.get("changed") else "ℹ️  Already installed"
                print(f"{status}: {package}")
            except Exception as e:
                print(f"⚠️  Failed to install {package}: {e}")
        
        print("\n🔐 Step 3: SSH Security Configuration")
        print("-" * 30)
        
        # SSH hardening configurations
        ssh_configs = [
            {
                "line": "PasswordAuthentication no",
                "regexp": r"^#?PasswordAuthentication",
                "description": "Disable password authentication"
            },
            {
                "line": "PermitRootLogin no", 
                "regexp": r"^#?PermitRootLogin",
                "description": "Disable root login"
            },
            {
                "line": "Protocol 2",
                "regexp": r"^#?Protocol",
                "description": "Use SSH Protocol 2"
            },
            {
                "line": "MaxAuthTries 3",
                "regexp": r"^#?MaxAuthTries",
                "description": "Limit authentication attempts"
            }
        ]
        
        for config in ssh_configs:
            try:
                result = ftl.lineinfile(
                    path="/etc/ssh/sshd_config",
                    line=config["line"],
                    regexp=config["regexp"],
                    backup=True
                )
                status = "✅ Applied" if result.get("changed") else "ℹ️  Already set"
                print(f"{status}: {config['description']}")
            except Exception as e:
                print(f"⚠️  Failed to configure {config['description']}: {e}")
        
        print("\n📁 Step 4: Directory Structure Setup")
        print("-" * 30)
        
        # Create standard directory structure
        directories = [
            "/opt/applications",
            "/var/log/applications", 
            "/etc/applications",
            "/home/shared"
        ]
        
        for directory in directories:
            try:
                result = ftl.file(
                    path=directory,
                    state="directory",
                    mode="0755",
                    owner="root",
                    group="root"
                )
                status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
                print(f"{status}: {directory}")
            except Exception as e:
                print(f"⚠️  Failed to create {directory}: {e}")
        
        print("\n🔧 Step 5: Service Management")
        print("-" * 30)
        
        # Manage system services
        services_config = [
            {"name": "firewalld", "state": "started", "enabled": True},
            {"name": "chronyd", "state": "started", "enabled": True}
        ]
        
        for service in services_config:
            try:
                # Start/stop service
                result = ftl.service(
                    name=service["name"],
                    state=service["state"]
                )
                status = "✅ Started" if result.get("changed") else "ℹ️  Already running"
                print(f"{status}: {service['name']}")
                
                # Enable/disable service
                if service.get("enabled"):
                    enable_result = ftl.service(
                        name=service["name"],
                        enabled=True
                    )
                    enable_status = "✅ Enabled" if enable_result.get("changed") else "ℹ️  Already enabled"
                    print(f"{enable_status}: {service['name']} (startup)")
                    
            except Exception as e:
                print(f"⚠️  Service management failed for {service['name']}: {e}")
        
        print("\n📝 Step 6: Configuration Files")
        print("-" * 30)
        
        # Create basic configuration files
        configs = [
            {
                "path": "/etc/motd",
                "content": "Welcome to this managed server\nManaged by ftl-automation\n"
            },
            {
                "path": "/etc/profile.d/custom.sh", 
                "content": "# Custom environment settings\nexport EDITOR=vim\n"
            }
        ]
        
        for config in configs:
            try:
                result = ftl.copy(
                    content=config["content"],
                    dest=config["path"],
                    owner="root",
                    group="root",
                    mode="0644"
                )
                status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
                print(f"{status}: {config['path']}")
            except Exception as e:
                print(f"⚠️  Failed to create {config['path']}: {e}")
        
        print("\n🔄 Step 7: System Updates")
        print("-" * 30)
        
        # Update system packages
        try:
            result = ftl.dnf(name="*", state="latest")
            if result.get("changed"):
                print("✅ System packages updated")
                packages_updated = result.get("results", [])
                if packages_updated:
                    print(f"   Updated {len(packages_updated)} packages")
            else:
                print("ℹ️  System packages already up to date")
        except Exception as e:
            print(f"⚠️  System update failed: {e}")
        
        print("\n✨ System setup completed!")
        print("=" * 50)
        print("\nNext steps you might consider:")
        print("- Configure monitoring (e.g., Prometheus, Grafana)")
        print("- Set up log aggregation (e.g., ELK stack)")
        print("- Configure backup schedules")
        print("- Install security scanning tools")
        print("- Set up configuration management")


if __name__ == "__main__":
    main()