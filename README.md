# FTL Automation

A pure Python automation library built on Faster Than Light, extracted from ftl-automation-agent without AI dependencies.

## Overview

FTL Automation provides a simple, function-based interface for infrastructure automation tasks. It combines the power of FTL's automation engine with a clean Python API for loading tools, managing inventories, and executing automation tasks.

## Features

- **Pure Python**: No AI or agent framework dependencies
- **FTL Integration**: Built on the proven Faster Than Light automation engine
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
    
    # Execute a loaded tool
    ftl.execute_tool("bash", script="/path/to/script.sh", user="root")
```

### Loading Tools

```python
import ftl_automation

# Load tools from files
tools = ftl_automation.load_tools_from_files(["my_tools.py"])

# Load specific tools by name
tools = ftl_automation.load_tools_by_name(["bash", "copy"])

# Use in automation context
with ftl_automation.automation(inventory="hosts.yml") as ftl:
    # Tools are available as ftl.tools
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

## Comparison with ftl-automation-agent

| Feature | ftl-automation-agent | ftl-automation |
|---------|---------------------|----------------|
| AI Integration | ✅ smolagents | ❌ None |
| Code Generation | ✅ Python/YAML | ❌ None |
| Agent Framework | ✅ Complex | ❌ None |
| Tool Interface | 🔧 Class-based | 🔧 Function-based |
| Dependencies | 📦 Many | 📦 Minimal |
| Complexity | 🧠 High | 🧠 Low |
| Use Case | AI-driven automation | Direct automation |

## License

This project is licensed under the same terms as the original ftl-automation-agent.