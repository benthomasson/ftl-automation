# FTL Automation

An **AI-first** automation library built on Faster Than Light, specifically designed for Claude and other coding agents to perform infrastructure automation tasks.

## Overview

FTL Automation provides a simple, clean interface optimized for AI agents to perform complex infrastructure automation. The library is designed with Claude Code as the primary user in mind, offering an intuitive Python API that allows AI assistants to provision infrastructure, configure systems, and manage automation workflows through natural conversation.

### AI-First Design Philosophy

- **Designed for Claude**: The primary user is expected to be Claude Code and other AI coding assistants
- **Conversational Automation**: AI agents can translate user requests into working infrastructure code
- **Context-Aware**: Built to work seamlessly within AI coding sessions and automation workflows
- **Self-Documenting**: Clear APIs that AI agents can understand and use effectively

## Features

### AI-Optimized Capabilities
- **Agent-Friendly**: Designed specifically for Claude Code and AI coding assistants
- **Natural Language to Code**: AI agents can translate user requests into working automation
- **Context-Aware Execution**: Seamless integration with AI coding sessions
- **Intelligent Defaults**: Sensible defaults that reduce cognitive load on AI agents

### Core Infrastructure Features
- **Pure Python**: No AI or agent framework dependencies - clean integration
- **FTL Integration**: Built on the proven Faster Than Light automation engine
- **Direct Tool Calling**: Clean `ftl.tool_name()` syntax optimized for AI understanding
- **Comprehensive Tools**: Full suite of automation tools for system management
- **Module Auto-Discovery**: Automatically finds and loads modules from related projects
- **Infrastructure Provisioning**: Built-in support for cloud providers (AWS, Linode)
- **Secrets Management**: Secure environment variable loading without hardcoded credentials
- **Inventory Management**: Automatic inventory file creation and updates
- **Rich Output**: Beautiful console output and progress tracking for debugging

## Installation

```bash
cd ftl-automation
pip install -e .
```

## Quick Start

Here's a complete example that Claude Code would write to provision a server, configure it, and send a notification when a user requests "Set up a web server on Linode":

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

### AWS Cloud Services (via ftl-aws-tools)
- `kms_key(alias, description, policy)` - Manage AWS KMS encryption keys
- Additional AWS tools available through ftl-aws-tools integration

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

### Module System & Auto-Discovery
- **FTL Modules**: Built on proven Faster Than Light automation modules
- **Ansible Compatible**: Uses Ansible-compatible modules (including AnsibleAWSModule)
- **Auto-Discovery**: Automatically finds modules from related projects in `../*/modules/`
- **Multi-Project Support**: Works seamlessly across ftl-automation, aws-automation, ftl-tools
- **Extensible**: Easy to add custom modules and tool packages

## AI Agent Use Cases

### What Claude Code Can Do With FTL Automation

- **"Create a web server"**: Claude provisions cloud infrastructure, configures services, and secures access
- **"Set up monitoring"**: Claude deploys monitoring tools, configures alerts, and sets up dashboards  
- **"Deploy my app"**: Claude handles the entire deployment pipeline from infrastructure to application
- **"Secure my servers"**: Claude implements security best practices, hardens SSH, configures firewalls
- **"Scale my infrastructure"**: Claude adds servers, load balancers, and configures auto-scaling

### Traditional Use Cases (for human developers)

- **Infrastructure Provisioning**: Spin up cloud servers and configure them
- **System Configuration**: Manage services, users, and system settings  
- **Security Hardening**: Configure SSH, firewalls, and access controls
- **Application Deployment**: Deploy and manage applications and services
- **Monitoring Setup**: Configure monitoring and alerting systems

## Getting Started

### For AI Agents (Claude Code)
1. **Context**: AI agents can use FTL Automation directly in coding sessions
2. **Natural Requests**: Users can request infrastructure in natural language
3. **Code Generation**: AI generates working automation code using the FTL API
4. **Execution**: Code runs immediately with proper error handling and feedback

### For Human Developers  
1. **Install**: `pip install -e .` 
2. **Set secrets**: Export required environment variables (e.g., `LINODE_TOKEN`, `AWS_PROFILE`)
3. **Write script**: Use the example above as a starting point
4. **Run**: Execute your Python script

## AI-First Architecture

FTL Automation is specifically designed to be the foundation for AI-driven infrastructure automation. Whether you're Claude Code helping a user deploy applications, or a human developer building automation scripts, FTL Automation provides the reliable, clean interface needed to turn infrastructure requirements into working code.

### Key AI-Friendly Design Patterns
- **Declarative Syntax**: `ftl.tool_name()` calls that clearly express intent
- **Intelligent Defaults**: Sensible defaults that work out of the box
- **Clear Error Messages**: Detailed feedback that helps AI agents debug issues  
- **Modular Design**: Tools can be combined naturally to build complex workflows
- **State Management**: Automatic inventory and secrets handling

FTL Automation makes infrastructure automation simple, reliable, and maintainable - whether you're an AI agent or a human developer.

## License

This project is licensed under the same terms as the original ftl-automation-agent.