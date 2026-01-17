# FTL Automation Examples

This directory contains examples demonstrating various usage patterns and features of the ftl-automation library.

## Examples Overview

### Core Examples

### 🔰 [basic_usage.py](basic_usage.py)
**Beginner-friendly introduction to ftl-automation**
- Using the `automation()` context manager
- Loading inventories and modules
- Running basic FTL modules
- Direct module execution without context

```bash
python examples/basic_usage.py
```

### 🛠️ [tool_loading.py](tool_loading.py)
**Working with custom tools and tool loading**
- Creating custom tool functions
- Loading tools from Python files
- Using tools within automation context
- Loading tools by name from packages

```bash
python examples/tool_loading.py
```

### 🔧 [builtin_tools_demo.py](builtin_tools_demo.py)
**Demonstration of built-in automation tools**
- Using debug and user input tools
- Tool completion patterns
- Interactive automation workflows

```bash
python examples/builtin_tools_demo.py
```

### 📋 [inventory_example.py](inventory_example.py)
**Inventory management and host operations**
- Creating and loading inventory files
- Working with host groups and variables
- Running tasks across multiple hosts
- Localhost operations

```bash
python examples/inventory_example.py
```

### 💻 [cli_examples.py](cli_examples.py)
**Command-line interface usage patterns**
- CLI tool demonstrations
- Various command-line options
- Integration with shell scripts
- Batch automation tasks

```bash
python examples/cli_examples.py
```

### 🚀 [advanced_usage.py](advanced_usage.py)
**Complex automation scenarios**
- Error handling and rollback strategies
- Progress tracking and user feedback
- Custom context management
- Resource management and cleanup
- Multiple automation contexts

```bash
python examples/advanced_usage.py
```

### 🔍 [module_discovery_example.py](module_discovery_example.py)
**Automatic module discovery and path handling**
- Auto-discovery of module directories in common locations
- Combining manual modules with auto-discovery
- Multi-project environment support
- Eliminating hardcoded relative module paths

```bash
python examples/module_discovery_example.py
```

### Real-World Infrastructure Examples

### 🖥️ [server_provisioning.py](server_provisioning.py)
**Cloud server provisioning and initial setup**
- System information gathering
- Hostname configuration
- User account creation with sudo access
- SSH key management and security
- Basic system package updates
- Infrastructure automation patterns

```bash
python examples/server_provisioning.py
```

### ⚙️ [system_setup.py](system_setup.py)
**Comprehensive system administration tasks**
- Multi-user management and groups
- Essential package installation
- SSH security hardening
- System directory structure creation
- Service management and startup configuration
- Configuration file deployment
- System update automation

```bash
python examples/system_setup.py
```

### 🌐 [web_application_deployment.py](web_application_deployment.py)
**Complete web application stack deployment**
- Web server installation (Nginx)
- Application runtime setup (Node.js)
- Database configuration (PostgreSQL)
- Application user and directory structure
- Systemd service configuration
- Reverse proxy setup
- Firewall configuration
- Health checks and monitoring

```bash
python examples/web_application_deployment.py
```

### 🔥 [firewall_security.py](firewall_security.py)
**Security hardening and firewall configuration**
- Firewalld setup and management
- Default deny security policies
- SSH hardening and custom port configuration
- Web service security configuration
- Custom port management
- Intrusion prevention with Fail2ban
- Security monitoring and reporting
- Additional security tool installation

```bash
python examples/firewall_security.py
```

### 💾 [backup_restore.py](backup_restore.py)
**Comprehensive backup and disaster recovery**
- Backup infrastructure setup
- Database backup automation (PostgreSQL/MySQL)
- File system backup strategies
- Restore procedures and scripts
- Automated backup scheduling with cron
- Backup monitoring and reporting
- Integrity verification
- Disaster recovery documentation

```bash
python examples/backup_restore.py
```

## Running Examples

### Prerequisites
1. Install ftl-automation:
   ```bash
   cd /path/to/ftl-automation
   pip install -e .
   ```

2. Ensure you have a basic inventory file or the examples will create test files

3. Make sure the faster-than-light modules are available

### Individual Examples
Run any example directly:
```bash
python examples/basic_usage.py
python examples/tool_loading.py
# etc.
```

### All Examples
Run all examples in sequence:
```bash
for example in examples/*.py; do
    echo "Running $example..."
    python "$example"
    echo "---"
done
```

### By Category
Run examples by category:
```bash
# Core examples (learning ftl-automation basics)
python examples/basic_usage.py
python examples/tool_loading.py
python examples/builtin_tools_demo.py

# Infrastructure examples (real-world scenarios)
python examples/server_provisioning.py
python examples/system_setup.py
python examples/web_application_deployment.py
python examples/firewall_security.py
python examples/backup_restore.py
```

## Key Concepts Demonstrated

### Context Management
```python
with ftl_automation.automation(
    inventory="hosts.yml",
    modules=["modules"],
    tools=["bash", "copy"]
) as ftl:
    # Automation operations
    result = ftl.run_module("command", cmd="uptime")
```

### Custom Tools
```python
def my_tool(inventory, modules, console, **kwargs):
    console.print("[blue]Running my tool...[/blue]")
    return ftl_automation.run_module(
        inventory, modules, "command", {"cmd": "echo hello"}
    )
```

### Tool Loading Patterns
```python
# From files
tools = ftl_automation.load_tools_from_files(["my_tools.py"])

# By name
tools = ftl_automation.load_tools_by_name(["bash", "copy"])

# In context
with ftl_automation.automation(tools_files=["my_tools.py"]) as ftl:
    ftl.execute_tool("my_tool", param="value")
```

### Direct Module Execution
```python
inventory = ftl_automation.load_inventory("hosts.yml")
modules = ftl_automation.load_modules(["modules"])

result = ftl_automation.run_module(
    inventory, modules, "service", 
    {"name": "nginx", "state": "started"}
)
```

## Common Patterns

### Service Management
```python
# Check service status
result = ftl.run_module("service", name="nginx", state="started")

# Restart service
result = ftl.run_module("service", name="apache2", state="restarted")
```

### File Operations
```python
# Create file
result = ftl.run_module("file", path="/tmp/test", state="touch")

# Copy file
result = ftl.run_module("copy", src="local.txt", dest="/remote/path/")
```

### Command Execution
```python
# Simple command
result = ftl.run_module("command", cmd="uptime")

# Complex command with shell
result = ftl.run_module("shell", cmd="ps aux | grep nginx")
```

### Package Management
```python
# Install package
result = ftl.run_module("package", name="htop", state="present")

# Update package
result = ftl.run_module("package", name="nginx", state="latest")
```

## Tips for Development

1. **Start with basic_usage.py** to understand core concepts
2. **Use tool_loading.py** to learn custom tool development
3. **Check inventory_example.py** for multi-host scenarios
4. **Review advanced_usage.py** for production patterns

## Creating Your Own Examples

When creating new examples:
1. Include docstrings explaining the purpose
2. Add error handling for robustness
3. Use Rich console for better output
4. Clean up any temporary files
5. Follow the existing code style

## Example Use Cases

### Infrastructure Automation
- **Server Provisioning**: Cloud instance creation and basic setup
- **System Configuration**: User management, package installation, security hardening
- **Application Deployment**: Full web application stack with database, web server, and monitoring
- **Security Management**: Firewall configuration, intrusion prevention, security monitoring
- **Backup Operations**: Automated backup/restore with disaster recovery procedures

### Integration Patterns
These examples can be integrated into larger systems:
- **CI/CD Pipelines**: Use for automated deployment and infrastructure management
- **Configuration Management**: Integrate with existing CM tools for hybrid automation
- **Monitoring Systems**: Create health check and remediation tools
- **Development Workflows**: Automate development environment setup and maintenance
- **Disaster Recovery**: Implement automated backup and restore procedures
- **Security Compliance**: Automate security policy enforcement and auditing

### Production Considerations
When adapting these examples for production use:
1. **Inventory Management**: Use real inventory files with proper host groups and variables
2. **Secret Management**: Implement secure credential storage and rotation
3. **Error Handling**: Add comprehensive error handling and rollback procedures
4. **Logging**: Implement structured logging and audit trails
5. **Testing**: Add automated testing for infrastructure changes
6. **Monitoring**: Integrate with monitoring and alerting systems
7. **Documentation**: Maintain runbooks and disaster recovery procedures

## Example Progression

### Learning Path
1. **Start with Core Examples** (`basic_usage.py`, `tool_loading.py`) to understand fundamentals
2. **Practice with Infrastructure Examples** to see real-world applications
3. **Customize Examples** for your specific infrastructure needs
4. **Build Complex Workflows** combining multiple examples

### From Examples to Production
- Use examples as templates for your infrastructure automation
- Adapt inventory structures for your environment
- Implement proper secret management
- Add monitoring and alerting integration
- Create automated testing and validation

For questions or contributions to examples, see the main project documentation.