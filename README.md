# FTL Automation

A pure Python automation library built on Faster Than Light, extracted from ftl-automation-agent without AI dependencies.

## Overview

FTL Automation provides a simple, clean interface for infrastructure automation tasks. It combines the power of FTL's automation engine with an intuitive Python API for provisioning infrastructure, configuring systems, and managing automation workflows.

## Features

- **Pure Python**: No AI or agent framework dependencies  
- **FTL Integration**: Built on the proven Faster Than Light automation engine
- **Direct Tool Calling**: Clean `ftl.tool_name()` syntax for all operations
- **Comprehensive Tools**: Full suite of automation tools for system management
- **Infrastructure Provisioning**: Built-in support for cloud providers like Linode
- **Secrets Management**: Secure environment variable loading
- **Inventory Management**: Automatic inventory file creation and updates
- **Rich Output**: Beautiful console output and progress tracking

## Installation

```bash
cd ftl-automation
pip install -e .
```

## Quick Start

Here's a complete example that provisions a server, configures it, and sends a notification:

```python
#!/usr/bin/env python3
import ftl_automation

with ftl_automation.automation(
    tools=[
        "linode", "hostname", "dnf", "user", 
        "authorized_key", "lineinfile", "service", "slack"
    ],
    inventory="inventory.yml",
    modules=["modules"],
    secrets=["SLACK_TOKEN", "LINODE_TOKEN", "LINODE_ROOT_PASS"],
) as ftl:

    # Provision infrastructure
    ftl.linode(name="web-server-1", ltype="g6-standard-1", image="linode/fedora43")
    
    # Configure system
    ftl.hostname(name="web-server-1")
    ftl.dnf(name="*", state="latest")  # Update all packages
    
    # Create user and setup SSH
    ftl.user(name="deploy", group="wheel")
    ftl.authorized_key(user="deploy", key_file=".ssh/id_rsa.pub")
    
    # Secure SSH configuration
    ftl.lineinfile(
        path="/etc/ssh/sshd_config",
        line="PasswordAuthentication no",
        regexp=r"^PasswordAuthentication.*"
    )
    ftl.service(name="sshd", state="restarted")
    
    # Send notification
    ftl.slack(msg="Server web-server-1 provisioned and configured successfully!")
```

## Available Tools

FTL Automation includes a comprehensive suite of tools for system management:

### Infrastructure & Cloud
- `linode(name, ltype, image)` - Provision Linode servers
- `hostname(name)` - Set system hostname

### Package Management  
- `dnf(name, state)` - Manage packages on Fedora/RHEL systems
- `apt(update_cache, upgrade)` - Manage packages on Debian/Ubuntu systems
- `pip(name, state)` - Manage Python packages

### User & Access Management
- `user(name, group)` - Create and manage system users
- `authorized_key(user, key_file, state)` - Manage SSH authorized keys

### File & Directory Operations
- `copy(src, dest)` - Copy files to remote systems
- `lineinfile(path, line, regexp, state)` - Manage lines in configuration files
- `chown(user, location)` - Change file ownership
- `get_url(url, dest)` - Download files from URLs

### System Services
- `service(name, state)` - Manage system services (start/stop/restart)
- `systemd_service(name, state, enabled)` - Manage systemd services
- `firewalld(port, state, protocol, permanent)` - Configure firewall rules

### System Configuration
- `swapfile(location, size, permanent)` - Create and manage swap files

### Communication
- `slack(msg, channel)` - Send Slack notifications

## Key Concepts

### Inventory Management
- **Automatic Creation**: Inventory files are created automatically if they don't exist
- **Dynamic Updates**: Tools like `linode` automatically add new hosts to inventory
- **YAML Format**: Simple YAML structure for host definitions

### Secrets Management
- **Environment Variables**: Secrets loaded securely from environment variables
- **No Hardcoding**: Credentials never appear in code
- **Multiple Providers**: Support for various cloud provider tokens

### Module System
- **FTL Modules**: Built on proven Faster Than Light automation modules
- **Ansible Compatible**: Uses Ansible-compatible modules under the hood
- **Extensible**: Easy to add custom modules

## Use Cases

- **Infrastructure Provisioning**: Spin up cloud servers and configure them
- **System Configuration**: Manage services, users, and system settings  
- **Security Hardening**: Configure SSH, firewalls, and access controls
- **Application Deployment**: Deploy and manage applications and services
- **Monitoring Setup**: Configure monitoring and alerting systems

## Getting Started

1. **Install**: `pip install -e .` 
2. **Set secrets**: Export required environment variables (e.g., `LINODE_TOKEN`)
3. **Write script**: Use the example above as a starting point
4. **Run**: Execute your Python script

FTL Automation makes infrastructure automation simple, reliable, and maintainable.

## License

This project is licensed under the same terms as the original ftl-automation-agent.