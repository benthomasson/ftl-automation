# FTL Automation Examples

This directory contains examples demonstrating various usage patterns and features of the ftl-automation library.

## Examples Overview

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

## Integration Examples

These examples can be integrated into larger systems:
- **CI/CD pipelines**: Use for deployment automation
- **Configuration management**: Integrate with existing CM tools
- **Monitoring systems**: Create health check tools
- **Development workflows**: Automate development environment setup

For questions or contributions to examples, see the main project documentation.