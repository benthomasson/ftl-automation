"""
Automation context and state management.
"""

import inspect
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table


class ToolsProxy:
    """Proxy object that allows tool access via attribute notation."""

    def __init__(self, tools_dict, context):
        self._tools = tools_dict
        self._context = context

    def __getattr__(self, name):
        if name in self._tools:
            return self.tools[name]
        raise AttributeError(f"Tool '{name}' not found")

    def __contains__(self, name):
        return name in self._tools

    def __iter__(self):
        return iter(self._tools)

    def keys(self):
        return self._tools.keys()


class AutomationContext:
    """
    Context object that holds automation state and resources.

    Provides access to inventory, modules, tools, and execution environment.
    """

    def __init__(
        self,
        inventory: Dict[str, Any],
        modules: List[str],
        tools: Dict[str, Any],
        localhost: Any,
        extra_vars: Optional[Dict[str, Any]] = None,
        console: Optional[Console] = None,
        secrets: Optional[Dict[str, str]] = None,
        inventory_file: Optional[str] = None,
        tool_packages: Optional[List[str]] = None,
        **kwargs,
    ):
        self.inventory = inventory
        self.modules = modules
        self._tools_dict = tools
        self.tools = ToolsProxy(tools, self)  # Enable ftl.tools.tool_name syntax
        self.localhost = localhost
        self.extra_vars = extra_vars or {}
        self.console = console or Console()
        self.secrets = secrets or {}
        self.inventory_file = inventory_file
        self.tool_packages = tool_packages or ["ftl_tools.tools"]
        self.gate_cache = {}
        self.use_gate = kwargs.get("use_gate", False)

        # Store additional context variables
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_tool(self, name: str):
        """Get a tool by name."""
        return self._tools_dict.get(name)

    def __getattr__(self, name: str):
        """Allow direct tool calls like ftl.bash(...)"""
        if name in self._tools_dict:
            return self._tools_dict[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def run_module(self, module_name: str, **module_args):
        """Execute an FTL module."""
        from .core import run_module

        return run_module(
            self.inventory,
            self.modules,
            module_name,
            module_args,
            gate_cache=self.gate_cache,
            use_gate=self.use_gate,
        )

    def print(self, *args, **kwargs):
        """Print to the console."""
        self.console.print(*args, **kwargs)

    def list_available_tools(self, category: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        List all available tools with their parameters and descriptions.
        
        Args:
            category: Optional category to filter tools by
            
        Returns:
            Dictionary mapping tool names to their metadata
        """
        tools_info = {}
        
        for tool_name, tool_instance in self._tools_dict.items():
            try:
                # Get the tool's description
                description = getattr(tool_instance, 'description', 'No description available')
                
                # Get the module name if available
                module = getattr(tool_instance, 'module', 'builtin')
                
                # Extract parameters from the __call__ method signature
                call_method = getattr(tool_instance, '__call__', None)
                parameters = []
                if call_method:
                    sig = inspect.signature(call_method)
                    for param_name, param in sig.parameters.items():
                        if param_name == 'self':
                            continue
                        
                        param_info = {'name': param_name}
                        
                        # Add type annotation if available
                        if param.annotation != inspect.Parameter.empty:
                            param_info['type'] = param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation)
                        
                        # Add default value if available
                        if param.default != inspect.Parameter.empty:
                            param_info['default'] = param.default
                            param_info['required'] = False
                        else:
                            param_info['required'] = True
                            
                        parameters.append(param_info)
                
                # Categorize tools based on their functionality
                tool_category = self._categorize_tool(tool_name, module)
                
                tools_info[tool_name] = {
                    'description': description,
                    'parameters': parameters,
                    'module': module,
                    'category': tool_category
                }
                
            except Exception as e:
                # If we can't introspect a tool, provide basic info
                tools_info[tool_name] = {
                    'description': 'Tool information unavailable',
                    'parameters': [],
                    'module': 'unknown',
                    'category': 'other',
                    'error': str(e)
                }
        
        # Filter by category if specified
        if category:
            tools_info = {
                name: info for name, info in tools_info.items() 
                if info['category'] == category
            }
            
        return tools_info
    
    def _categorize_tool(self, tool_name: str, module: str) -> str:
        """Categorize a tool based on its name and module."""
        file_tools = ['copy', 'copyfrom', 'mkdir', 'chmod', 'chown', 'get_url', 'template', 'unarchive', 'lineinfile']
        system_tools = ['service', 'systemd_service', 'user', 'hostname', 'timezone', 'swapfile']
        package_tools = ['dnf', 'apt', 'pip']
        security_tools = ['firewalld', 'authorized_key', 'certbot', 'setsebool']
        dev_tools = ['git', 'java_jar', 'bash', 'podman']
        cloud_tools = ['linode']
        notification_tools = ['slack', 'discord']
        automation_tools = ['complete', 'debug', 'impossible', 'user_input']
        
        if tool_name in file_tools:
            return 'file'
        elif tool_name in system_tools:
            return 'system'
        elif tool_name in package_tools:
            return 'package'
        elif tool_name in security_tools:
            return 'security'
        elif tool_name in dev_tools:
            return 'development'
        elif tool_name in cloud_tools:
            return 'cloud'
        elif tool_name in notification_tools:
            return 'notification'
        elif tool_name in automation_tools:
            return 'automation'
        else:
            return 'other'
    
    def show_tools(self, category: Optional[str] = None, detailed: bool = False):
        """
        Display available tools in a formatted table.
        
        Args:
            category: Optional category to filter by
            detailed: Show detailed parameter information
        """
        tools_info = self.list_available_tools(category)
        
        if not tools_info:
            category_msg = f" in category '{category}'" if category else ""
            self.console.print(f"[yellow]No tools found{category_msg}[/yellow]")
            return
        
        # Create table
        table = Table(title=f"Available Tools{' - ' + category.title() if category else ''}")
        table.add_column("Tool", style="cyan", no_wrap=True)
        table.add_column("Category", style="magenta")
        table.add_column("Description", style="white")
        
        if detailed:
            table.add_column("Parameters", style="green")
        
        # Sort tools by category, then by name
        sorted_tools = sorted(tools_info.items(), key=lambda x: (x[1]['category'], x[0]))
        
        for tool_name, info in sorted_tools:
            row = [tool_name, info['category'], info['description']]
            
            if detailed:
                # Format parameters
                params = []
                for param in info['parameters']:
                    param_str = param['name']
                    if 'type' in param:
                        param_str += f": {param['type']}"
                    if not param.get('required', True):
                        param_str += " (optional)"
                    params.append(param_str)
                row.append(", ".join(params) if params else "No parameters")
            
            table.add_row(*row)
        
        self.console.print(table)
        
        if not detailed and tools_info:
            self.console.print("\n[dim]Use show_tools(detailed=True) to see parameter details[/dim]")

    def cleanup(self):
        """Cleanup resources."""
        # Close any open gates
        if hasattr(self, "gate_cache"):
            # Add cleanup logic for gates if needed
            pass
