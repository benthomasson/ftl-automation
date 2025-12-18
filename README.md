# FTL Automation

A pure Python automation library built on Faster Than Light, extracted from ftl-automation-agent without AI dependencies.

## Overview

FTL Automation provides a simple, function-based interface for infrastructure automation tasks. It combines the power of FTL's automation engine with a clean Python API for loading tools, managing inventories, and executing automation tasks.

## Features

- **Pure Python**: No AI or agent framework dependencies
- **FTL Integration**: Built on the proven Faster Than Light automation engine
- **Multiple Tool Syntaxes**: Direct calling (`ftl.tool_name()`), tool assignment (`ftl.tools.tool_name`), and explicit execution
- **Built-in Tools**: Essential automation tools included (user_input_tool, complete, impossible, debug_tool)
- **Secrets Management**: Environment variable loading and secure credential handling
- **ftl-automation-agent Compatibility**: Supports exact patterns from AI-generated scripts
- **Tool Loading**: Dynamic loading of automation tools from files or by name
- **Context Management**: Clean context management for automation sessions
- **Rich Output**: Beautiful console output using Rich
- **Simple API**: Function-based interface, easy to use and extend

## Installation

```bash
cd ftl-automation
pip install -e .
```

## Quick Start

### Basic Usage

```python
import ftl_automation

# Load and execute automation tasks
with ftl_automation.automation(
    inventory="inventory.yml",
    modules=["modules"],
    tools=["bash", "copy", "service"]
) as ftl:
    
    # Run an FTL module directly
    result = ftl.run_module("command", cmd="uptime")
    
    # Execute tools using direct syntax (NEW!)
    ftl.bash(script="/path/to/script.sh", user="root")
    
    # Or use the original method
    ftl.execute_tool("bash", script="/path/to/script.sh", user="root")
```

### Loading Tools

```python
import ftl_automation

# Load tools from files
tools = ftl_automation.load_tools_from_files(["my_tools.py"])

# Load specific tools by name
tools = ftl_automation.load_tools_by_name(["bash", "copy"])

# Use in automation context - Multiple syntax options!
with ftl_automation.automation(inventory="hosts.yml") as ftl:
    
    # Direct calling (cleanest syntax)
    result = ftl.my_tool(param1="value")
    
    # Tool assignment (ftl-automation-agent compatible)
    my_tool = ftl.tools.my_tool
    result = my_tool(param1="value")
    
    # Explicit execution
    result = ftl.execute_tool("my_tool", param1="value")
```

### Direct Module Execution

```python
import ftl_automation

inventory = ftl_automation.load_inventory("inventory.yml")
modules = ftl_automation.load_modules(["modules"])

# Execute module directly
result = ftl_automation.run_module(
    inventory=inventory,
    modules=modules,
    module_name="service",
    module_args={"name": "nginx", "state": "started"}
)
```

## Tool Syntax Patterns

FTL Automation supports multiple ways to call tools for maximum flexibility:

### 1. Direct Calling (Recommended)
```python
with ftl_automation.automation(inventory="hosts.yml") as ftl:
    # Clean, concise syntax
    ftl.debug_tool(message="Starting deployment")
    result = ftl.deploy_service(name="nginx", state="started")
    ftl.user_input_tool(question="Continue? (y/n)")
    ftl.complete(message="Deployment finished")
```

### 2. Tool Assignment (ftl-automation-agent Compatible)
```python
with ftl_automation.automation(inventory="hosts.yml") as ftl:
    # Exact same pattern as AI-generated scripts
    debug_tool = ftl.tools.debug_tool
    deploy_service = ftl.tools.deploy_service
    user_input_tool = ftl.tools.user_input_tool
    complete = ftl.tools.complete
    
    debug_tool(message="Starting deployment")
    result = deploy_service(name="nginx", state="started")
    user_input_tool(question="Continue? (y/n)")
    complete(message="Deployment finished")
```

### 3. Explicit Execution
```python
with ftl_automation.automation(inventory="hosts.yml") as ftl:
    # Explicit method calls
    ftl.execute_tool("debug_tool", message="Starting deployment")
    result = ftl.execute_tool("deploy_service", name="nginx", state="started")
```

### Built-in Tools

Essential automation tools are included automatically:
- `user_input_tool(question, default=None)` - Interactive user prompts
- `complete(message)` - Signal successful task completion  
- `impossible(reason)` - Signal task cannot be completed
- `debug_tool(message)` - Debug output with timestamps
- `get_secret(name)` - Access secrets from environment/context

## CLI Usage

```bash
# Execute a module
ftl-automation --inventory hosts.yml --module-name service --module-args "name=nginx,state=started"

# Load tools and run interactively  
ftl-automation --inventory hosts.yml --tools bash,copy,service

# Load tools from files
ftl-automation --tools-files my_tools.py --inventory hosts.yml
```

## Architecture

### Core Components

- **`automation()` context manager**: Main entry point for automation sessions
- **`AutomationContext`**: Manages state, inventory, modules, and tools
- **Tool loading**: Dynamic loading from files or by name
- **FTL integration**: Direct access to Faster Than Light automation engine

### Tool Functions

Tools are simple Python functions that receive automation context:

```python
def my_automation_tool(inventory, modules, console, **kwargs):
    """Custom automation tool."""
    console.print("[blue]Running my tool...[/blue]")
    
    # Use FTL to execute modules
    result = run_module(
        inventory=inventory,
        modules=modules,
        module_name="command",
        module_args={"cmd": "echo hello"}
    )
    
    console.print(f"[green]Result: {result}[/green]")
    return result
```

## Migration from ftl-automation-agent

### Automatic Compatibility
Existing ftl-automation-agent generated scripts work **without any changes**! 

```python
# This ftl-automation-agent pattern works unchanged:
with ftl_automation.automation(
    tools=("linode_tool", "dnf_tool", "user_input_tool", "complete"),
    inventory="inventory.yml",
    secrets=("LINODE_TOKEN", "LINODE_ROOT_PASS"),
) as ftl:
    
    linode_tool = ftl.tools.linode_tool
    user_input_tool = ftl.tools.user_input_tool
    complete = ftl.tools.complete
    
    server_name = user_input_tool(question="Enter server name:")
    created = linode_tool(name=server_name, image="linode/fedora41")
    complete("Server created successfully")
```

### Optional Syntax Improvements
For new scripts, you can use the cleaner direct syntax:

```python
# Modernized version with direct calling:
with ftl_automation.automation(
    tools=("linode_tool", "dnf_tool"),
    inventory="inventory.yml", 
    secrets=("LINODE_TOKEN", "LINODE_ROOT_PASS"),
) as ftl:
    
    server_name = ftl.user_input_tool(question="Enter server name:")
    created = ftl.linode_tool(name=server_name, image="linode/fedora41")
    ftl.complete(message="Server created successfully")
```

## Comparison with ftl-automation-agent

| Feature | ftl-automation-agent | ftl-automation |
|---------|---------------------|----------------|
| AI Integration | ✅ smolagents | ❌ None |
| Code Generation | ✅ Python/YAML | ❌ None |
| Agent Framework | ✅ Complex | ❌ None |
| Script Compatibility | ✅ Generates scripts | ✅ **Runs same scripts** |
| Tool Interface | 🔧 Class-based | 🔧 Function-based + Direct calling |
| Syntax Options | 🔧 1 pattern | 🔧 **3 patterns** |
| Dependencies | 📦 Many | 📦 Minimal |
| Complexity | 🧠 High | 🧠 Low |
| Use Case | AI-driven automation | Direct automation |

## Summary

**ftl-automation** provides the best of both worlds:
- **Drop-in compatibility** with ftl-automation-agent generated scripts
- **Improved syntax options** for cleaner, more maintainable automation code  
- **Pure Python** implementation without AI complexity or dependencies
- **All the power** of the Faster Than Light automation engine

Whether you're migrating from AI-generated scripts or building new automation from scratch, ftl-automation provides a flexible, powerful, and easy-to-use foundation for infrastructure automation tasks.

## License

This project is licensed under the same terms as the original ftl-automation-agent.