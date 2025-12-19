# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FTL Automation is a pure Python automation library built on Faster Than Light (FTL), extracted from ftl-automation-agent without AI dependencies. It provides infrastructure automation capabilities through a simple Python API.

## Development Commands

### Installation & Setup
```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run example scripts
python examples/basic_usage.py
python examples/tool_loading.py
```

### CLI Usage
```bash
# Basic CLI execution
ftl-automation --inventory inventory.yml --tools hostname,dnf

# Execute specific module
ftl-automation --inventory inventory.yml --module-name command --module-args "cmd=uptime"

# Load tools from files
ftl-automation --tools-files my_tools.py --inventory hosts.yml
```

## Architecture Overview

### Core Components

1. **AutomationContext** (`ftl_automation/context.py:31`): Central state management object that holds inventory, modules, tools, and execution environment. Provides `ftl.tool_name()` syntax through `__getattr__` method.

2. **automation() Context Manager** (`ftl_automation/core.py:53`): Main entry point that sets up FTL environment, loads inventory/modules/tools, manages asyncio event loop for FTL gate cache, and provides clean resource management.

3. **Tool System** (`ftl_automation/tool_base.py:12`): 
   - `AutomationTool` base class for creating automation tools
   - Tools are callable objects that receive automation context
   - Loaded dynamically from `ftl_tools.tools.{tool_name}` packages

4. **Module Execution** (`ftl_automation/core.py:143`): Direct FTL module execution through `run_module()` function, wrapping `ftl.run_module_sync()`.

### Key Design Patterns

- **Context Pattern**: All operations flow through `AutomationContext` which provides unified access to resources
- **Dynamic Tool Loading**: Tools are imported by name from standardized package structure
- **Inventory Auto-Creation**: Empty inventory files are created automatically if missing at `ftl_automation/core.py:24`
- **Secrets Management**: Environment variables loaded securely without hardcoding credentials

### Integration Points

- **FTL Integration**: Built on `faster_than_light` library for core automation engine
- **Rich Console**: Uses `rich.console.Console` for formatted output
- **Click CLI**: Command-line interface built with Click framework
- **YAML Inventory**: Uses PyYAML for inventory file management

## Tool Development

### Creating Custom Tools
```python
from ftl_automation.tool_base import AutomationTool

class MyTool(AutomationTool):
    name = "my_tool"
    description = "My custom tool"
    
    def __call__(self, **kwargs):
        # Access automation context
        result = self.context.run_module("command", cmd="echo hello")
        return result
```

### Tool Loading Locations
- Primary: `ftl_tools.tools.{tool_name}` packages
- Tools must have `name` attribute matching the requested tool name
- Tool classes instantiated with `AutomationContext` parameter

## Common Usage Patterns

### Basic Automation Script
```python
import ftl_automation

with ftl_automation.automation(
    tools=["hostname", "dnf", "service"],
    inventory="inventory.yml",
    secrets=["LINODE_TOKEN"]
) as ftl:
    ftl.hostname(name="web-server")
    ftl.dnf(name="nginx", state="present") 
    ftl.service(name="nginx", state="started")
```

### Direct Module Execution
```python
inventory = ftl_automation.load_inventory("hosts.yml")
modules = ftl_automation.load_modules(["modules"])
result = ftl_automation.run_module(inventory, modules, "command", {"cmd": "uptime"})
```

## Testing

- Test files located in `tests/` directory
- Use pytest for running tests
- Test pattern: `test_*.py` files
- Example: `tests/test_loading_tools.py` tests tool loading functionality

## Dependencies

Core dependencies from `pyproject.toml`:
- `faster_than_light`: Core automation engine
- `rich`: Console output formatting  
- `pyyaml`: YAML inventory parsing
- `click`: CLI framework

## Important Implementation Notes

- **Event Loop Management**: `automation()` context manager creates dedicated asyncio event loop for FTL gate cache to prevent conflicts
- **Resource Cleanup**: Always use context manager pattern to ensure proper cleanup of event loops and gates
- **Inventory Auto-Creation**: Missing inventory files are created as empty YAML automatically
- **Tool Attribute Access**: Tools accessible via `ftl.tool_name()` syntax through `AutomationContext.__getattr__` method