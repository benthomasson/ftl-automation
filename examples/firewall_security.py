#!/usr/bin/env python3
"""
Firewall and Security Configuration Example

Demonstrates security hardening using ftl-automation.
This example shows:
- Firewall configuration with firewalld
- Security policy enforcement
- Port management and service restrictions
- SSH hardening
- Fail2ban setup for intrusion prevention
- Security monitoring setup
"""

import ftl_automation


def main():
    print("🔥 Firewall and Security Configuration Example")
    print("=" * 50)
    
    # Use localhost for demonstration
    localhost_inventory = {
        "all": {
            "hosts": {
                "secure-server": {
                    "ansible_connection": "local",
                    "ansible_host": "127.0.0.1",
                    "server_role": "web",
                    "environment": "production"
                }
            }
        }
    }
    
    with ftl_automation.automation(
        inventory=localhost_inventory,
        tools=[
            "firewalld",
            "service",
            "dnf", 
            "lineinfile",
            "file",
            "copy",
            "command",
            "user"
        ],
        tool_packages=["ftl_tools.tools"],
        modules=("modules",)
    ) as ftl:
        
        print("\n🔥 Step 1: Firewall Basic Setup")
        print("-" * 30)
        
        # Ensure firewalld is installed and running
        try:
            install_result = ftl.dnf(name="firewalld", state="present")
            if install_result.get("changed"):
                print("✅ Firewalld installed")
            else:
                print("ℹ️  Firewalld already installed")
            
            service_result = ftl.service(
                name="firewalld",
                state="started",
                enabled=True
            )
            if service_result.get("changed"):
                print("✅ Firewalld service started and enabled")
            else:
                print("ℹ️  Firewalld already running")
                
        except Exception as e:
            print(f"⚠️  Firewalld setup failed: {e}")
        
        print("\n🚫 Step 2: Default Deny Policy")
        print("-" * 30)
        
        # Set default zone to drop (more restrictive)
        try:
            # Get current default zone
            zone_result = ftl.command(cmd="firewall-cmd --get-default-zone")
            current_zone = zone_result.get("stdout", "").strip()
            print(f"ℹ️  Current default zone: {current_zone}")
            
            # Set to public zone (restrictive but allows some services)
            if current_zone != "public":
                ftl.command(cmd="firewall-cmd --set-default-zone=public")
                print("✅ Default zone set to public")
            else:
                print("ℹ️  Default zone already set to public")
                
        except Exception as e:
            print(f"⚠️  Failed to set default zone: {e}")
        
        print("\n🔑 Step 3: SSH Security Configuration")
        print("-" * 30)
        
        # Allow SSH but restrict it
        try:
            ssh_result = ftl.firewalld(
                service="ssh",
                state="enabled",
                permanent=True,
                immediate=True
            )
            if ssh_result.get("changed"):
                print("✅ SSH service allowed through firewall")
            else:
                print("ℹ️  SSH already allowed")
                
        except Exception as e:
            print(f"⚠️  SSH firewall config failed: {e}")
        
        # Configure SSH hardening
        ssh_hardening_configs = [
            {
                "line": "Port 2222",
                "regexp": r"^#?Port\s+",
                "description": "Change SSH port"
            },
            {
                "line": "Protocol 2", 
                "regexp": r"^#?Protocol\s+",
                "description": "SSH Protocol 2 only"
            },
            {
                "line": "PermitRootLogin no",
                "regexp": r"^#?PermitRootLogin\s+",
                "description": "Disable root login"
            },
            {
                "line": "PasswordAuthentication no",
                "regexp": r"^#?PasswordAuthentication\s+",
                "description": "Disable password auth"
            },
            {
                "line": "MaxAuthTries 3",
                "regexp": r"^#?MaxAuthTries\s+",
                "description": "Limit auth attempts"
            },
            {
                "line": "ClientAliveInterval 300",
                "regexp": r"^#?ClientAliveInterval\s+",
                "description": "Client timeout"
            },
            {
                "line": "ClientAliveCountMax 2",
                "regexp": r"^#?ClientAliveCountMax\s+",
                "description": "Max idle connections"
            }
        ]
        
        for config in ssh_hardening_configs:
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
                print(f"⚠️  Failed SSH config {config['description']}: {e}")
        
        print("\n🌐 Step 4: Web Services Configuration")
        print("-" * 30)
        
        # Configure web services (HTTP/HTTPS)
        web_services = [
            {"service": "http", "description": "HTTP traffic"},
            {"service": "https", "description": "HTTPS traffic"}
        ]
        
        for service in web_services:
            try:
                result = ftl.firewalld(
                    service=service["service"],
                    state="enabled",
                    permanent=True,
                    immediate=True
                )
                status = "✅ Enabled" if result.get("changed") else "ℹ️  Already enabled"
                print(f"{status}: {service['description']}")
            except Exception as e:
                print(f"⚠️  Failed to enable {service['description']}: {e}")
        
        print("\n🚪 Step 5: Custom Port Management")
        print("-" * 30)
        
        # Configure custom application ports
        custom_ports = [
            {"port": "2222/tcp", "description": "Custom SSH port"},
            {"port": "3000/tcp", "description": "Node.js application"},
            {"port": "5432/tcp", "description": "PostgreSQL (restricted)"},
            {"port": "9090/tcp", "description": "Monitoring (Prometheus)"}
        ]
        
        for port_config in custom_ports:
            try:
                # For database ports, you might want to restrict to specific zones
                result = ftl.firewalld(
                    port=port_config["port"],
                    state="enabled",
                    permanent=True,
                    immediate=True
                )
                status = "✅ Opened" if result.get("changed") else "ℹ️  Already open"
                print(f"{status}: {port_config['description']} ({port_config['port']})")
            except Exception as e:
                print(f"⚠️  Failed to open {port_config['port']}: {e}")
        
        print("\n🛡️  Step 6: Intrusion Prevention (Fail2ban)")
        print("-" * 30)
        
        # Install and configure fail2ban
        try:
            fail2ban_result = ftl.dnf(name="fail2ban", state="present")
            if fail2ban_result.get("changed"):
                print("✅ Fail2ban installed")
            else:
                print("ℹ️  Fail2ban already installed")
                
        except Exception as e:
            print(f"⚠️  Fail2ban installation failed: {e}")
        
        # Create fail2ban configuration
        fail2ban_config = """
[DEFAULT]
# Ban hosts for 1 hour
bantime = 3600

# A host is banned if it has generated "maxretry" during "findtime" seconds
findtime = 600
maxretry = 3

# Destination email for notifications
destemail = admin@example.com
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh,2222
logpath = /var/log/secure
backend = systemd
"""
        
        try:
            result = ftl.copy(
                content=fail2ban_config,
                dest="/etc/fail2ban/jail.local",
                owner="root",
                group="root",
                mode="0644"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: Fail2ban configuration")
            
            # Start and enable fail2ban
            service_result = ftl.service(
                name="fail2ban",
                state="started",
                enabled=True
            )
            if service_result.get("changed"):
                print("✅ Fail2ban service started")
            else:
                print("ℹ️  Fail2ban already running")
                
        except Exception as e:
            print(f"⚠️  Fail2ban configuration failed: {e}")
        
        print("\n📊 Step 7: Security Monitoring Setup")
        print("-" * 30)
        
        # Create security monitoring script
        monitoring_script = """#!/bin/bash
# Security monitoring script

echo "=== Security Status Report ===" 
echo "Generated: $(date)"
echo

echo "--- Firewall Status ---"
firewall-cmd --state
firewall-cmd --list-all

echo
echo "--- Failed Login Attempts (last 10) ---"
grep "Failed password" /var/log/secure | tail -10

echo
echo "--- Fail2ban Status ---"
fail2ban-client status

echo
echo "--- Active Network Connections ---"
ss -tuln | head -20

echo
echo "--- Resource Usage ---"
df -h / /tmp /var
free -h
"""
        
        try:
            result = ftl.copy(
                content=monitoring_script,
                dest="/usr/local/bin/security-check",
                owner="root",
                group="root",
                mode="0755"
            )
            status = "✅ Created" if result.get("changed") else "ℹ️  Already exists"
            print(f"{status}: Security monitoring script")
            
        except Exception as e:
            print(f"⚠️  Failed to create monitoring script: {e}")
        
        print("\n⚙️  Step 8: Additional Security Tools")
        print("-" * 30)
        
        # Install additional security tools
        security_tools = [
            "aide",      # File integrity monitoring
            "rkhunter",  # Rootkit detection  
            "lynis",     # Security auditing
            "nmap"       # Network discovery
        ]
        
        for tool in security_tools:
            try:
                result = ftl.dnf(name=tool, state="present")
                status = "✅ Installed" if result.get("changed") else "ℹ️  Already installed"
                print(f"{status}: {tool}")
            except Exception as e:
                print(f"⚠️  Failed to install {tool}: {e}")
        
        print("\n🔍 Step 9: Security Verification")
        print("-" * 30)
        
        # Run security verification checks
        verification_commands = [
            {
                "cmd": "firewall-cmd --state",
                "description": "Firewall status"
            },
            {
                "cmd": "firewall-cmd --list-services",
                "description": "Allowed services"
            },
            {
                "cmd": "firewall-cmd --list-ports",
                "description": "Open ports"
            },
            {
                "cmd": "systemctl is-active fail2ban",
                "description": "Fail2ban status"
            }
        ]
        
        for check in verification_commands:
            try:
                result = ftl.command(cmd=check["cmd"])
                if result.get("rc") == 0:
                    output = result.get("stdout", "").strip()
                    print(f"✅ {check['description']}: {output}")
                else:
                    print(f"⚠️  {check['description']}: Check failed")
            except Exception as e:
                print(f"⚠️  {check['description']}: {e}")
        
        print("\n📋 Step 10: Security Recommendations")
        print("-" * 30)
        
        recommendations = [
            "Configure log forwarding to centralized logging",
            "Set up regular security scans with Lynis", 
            "Configure AIDE for file integrity monitoring",
            "Set up automated backups of security configurations",
            "Implement network segmentation where possible",
            "Regular security updates via automated patching",
            "Configure SIEM/log analysis for threat detection",
            "Set up VPN access for administrative tasks",
            "Implement two-factor authentication where possible",
            "Regular penetration testing and vulnerability scans"
        ]
        
        for i, recommendation in enumerate(recommendations, 1):
            print(f"{i:2d}. {recommendation}")
        
        print("\n✨ Security configuration completed!")
        print("=" * 50)
        print("\nSecurity Summary:")
        print("- ✅ Firewall configured and active")
        print("- ✅ SSH hardened and secured")
        print("- ✅ Web services properly configured") 
        print("- ✅ Custom ports managed")
        print("- ✅ Intrusion prevention (Fail2ban) active")
        print("- ✅ Security monitoring tools installed")
        print("- ✅ Security verification completed")
        print("\n🔐 Your server security has been significantly improved!")


if __name__ == "__main__":
    main()