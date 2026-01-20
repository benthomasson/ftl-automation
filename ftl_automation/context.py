"""
Automation context and state management.
"""

import inspect
import os
import glob
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
        dry_run: bool = False,
        auto_discover_modules: bool = False,
        **kwargs,
    ):
        self.inventory = inventory
        self._tools_dict = tools
        self.tools = ToolsProxy(tools, self)  # Enable ftl.tools.tool_name syntax
        self.localhost = localhost
        self.extra_vars = extra_vars or {}
        self.console = console or Console()
        self.secrets = secrets or {}
        self.inventory_file = inventory_file
        self.tool_packages = tool_packages or ["ftl_tools.tools"]
        self.dry_run = dry_run
        self.gate_cache = {}
        self.use_gate = kwargs.get("use_gate", False)
        
        # Handle module discovery and path resolution AFTER console is initialized
        if auto_discover_modules:
            discovered_modules = self._discover_modules()
            all_modules = modules or []
            all_modules.extend(discovered_modules)
            self.modules = self._resolve_module_paths(all_modules)
        else:
            self.modules = self._resolve_module_paths(modules or [])

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
            dry_run=self.dry_run,
        )

    def run_module_locally(self, module_name: str, **module_args):
        """Execute an FTL module."""
        from .core import run_module

        return run_module(
            self.localhost,
            self.modules,
            module_name,
            module_args,
            gate_cache=self.gate_cache,
            use_gate=self.use_gate,
            dry_run=self.dry_run,
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

    def help(self, tool_name: Optional[str] = None, category: Optional[str] = None):
        """
        Display help information for tools.
        
        Args:
            tool_name: Specific tool to show help for
            category: Show all tools in a specific category
        """
        if tool_name:
            self._show_tool_help(tool_name)
        elif category:
            self._show_category_help(category)
        else:
            self._show_general_help()
    
    def _show_tool_help(self, tool_name: str):
        """Show detailed help for a specific tool."""
        tools_info = self.list_available_tools()
        
        if tool_name not in tools_info:
            self.console.print(f"[red]Tool '{tool_name}' not found[/red]")
            
            # Suggest similar tools
            available_tools = list(tools_info.keys())
            similar_tools = [t for t in available_tools if tool_name.lower() in t.lower() or t.lower() in tool_name.lower()]
            
            if similar_tools:
                self.console.print(f"[yellow]Did you mean: {', '.join(similar_tools)}?[/yellow]")
            else:
                self.console.print(f"[dim]Available tools: {', '.join(sorted(available_tools))}[/dim]")
            return
        
        tool_info = tools_info[tool_name]
        
        # Display tool header
        self.console.print(f"\n[bold cyan]{tool_name}[/bold cyan] - {tool_info['description']}")
        self.console.print(f"[dim]Category: {tool_info['category']}[/dim]")
        
        if tool_info.get('module') and tool_info['module'] != 'builtin':
            self.console.print(f"[dim]Module: {tool_info['module']}[/dim]")
        
        # Display parameters
        parameters = tool_info['parameters']
        if parameters:
            self.console.print(f"\n[bold]Parameters:[/bold]")
            
            # Create parameters table
            param_table = Table(show_header=True, header_style="bold magenta")
            param_table.add_column("Parameter", style="cyan")
            param_table.add_column("Type", style="green")
            param_table.add_column("Required", style="yellow")
            param_table.add_column("Default", style="blue")
            
            for param in parameters:
                param_name = param['name']
                param_type = param.get('type', 'any')
                required = "Yes" if param.get('required', True) else "No"
                default = str(param.get('default', '')) if 'default' in param else ''
                
                param_table.add_row(param_name, param_type, required, default)
            
            self.console.print(param_table)
        else:
            self.console.print(f"\n[dim]No parameters required[/dim]")
        
        # Show usage example
        self._show_usage_example(tool_name, tool_info)
    
    def _show_usage_example(self, tool_name: str, tool_info: Dict[str, Any]):
        """Generate and display a usage example for the tool."""
        parameters = tool_info['parameters']
        
        if not parameters:
            example = f"ftl.{tool_name}()"
        else:
            # Generate example parameters based on tool type and name
            example_params = []
            for param in parameters:
                param_name = param['name']
                param_type = param.get('type', 'str')
                
                if 'default' in param:
                    # Skip optional parameters with defaults for cleaner examples
                    continue
                
                # Generate realistic example values based on parameter name and type
                example_value = self._generate_example_value(tool_name, param_name, param_type)
                if param_type == 'str':
                    example_params.append(f'{param_name}="{example_value}"')
                else:
                    example_params.append(f'{param_name}={example_value}')
            
            example = f"ftl.{tool_name}({', '.join(example_params)})"
        
        self.console.print(f"\n[bold]Example:[/bold]")
        self.console.print(f"[green]{example}[/green]")
    
    def _generate_example_value(self, tool_name: str, param_name: str, param_type: str) -> str:
        """Generate realistic example values for tool parameters."""
        # Parameter name-based examples
        if param_name in ['name', 'hostname']:
            if tool_name == 'user':
                return 'myuser'
            elif tool_name == 'hostname':
                return 'web-server'
            elif tool_name in ['service', 'systemd_service']:
                return 'nginx'
            elif tool_name == 'dnf':
                return 'python3'
            else:
                return 'example-name'
        
        elif param_name in ['path', 'dest', 'location']:
            if tool_name == 'mkdir':
                return '/opt/myapp'
            elif tool_name in ['copy', 'template']:
                return '/etc/myapp/config.conf'
            elif tool_name == 'get_url':
                return '/tmp/download.tar.gz'
            else:
                return '/path/to/file'
        
        elif param_name in ['src', 'source']:
            if tool_name == 'copy':
                return 'config.conf'
            elif tool_name == 'template':
                return 'template.j2'
            else:
                return 'source/file'
        
        elif param_name == 'url':
            return 'https://example.com/file.tar.gz'
        
        elif param_name in ['state']:
            if tool_name in ['service', 'systemd_service']:
                return 'started'
            elif tool_name in ['dnf', 'apt', 'pip']:
                return 'present'
            else:
                return 'present'
        
        elif param_name in ['group', 'owner']:
            if param_name == 'group':
                return 'wheel'
            else:
                return 'root'
        
        elif param_name == 'user':
            return 'myuser'
        
        elif param_name in ['msg', 'message']:
            return 'Hello, deployment complete!'
        
        elif param_name == 'channel':
            return '#general'
        
        elif param_name in ['port']:
            return '80/tcp'
        
        elif param_name == 'size':
            return '1024'  # For swapfile size in MB
        
        elif param_name in ['question']:
            return 'Do you want to continue?'
        
        # Type-based fallbacks
        elif param_type == 'bool':
            return 'True'
        elif param_type == 'int':
            return '1024'
        else:
            return 'example-value'
    
    def _show_category_help(self, category: str):
        """Show help for all tools in a specific category."""
        tools_info = self.list_available_tools(category=category)
        
        if not tools_info:
            available_categories = set(info['category'] for info in self.list_available_tools().values())
            self.console.print(f"[red]Category '{category}' not found[/red]")
            self.console.print(f"[dim]Available categories: {', '.join(sorted(available_categories))}[/dim]")
            return
        
        self.console.print(f"\n[bold]{category.title()} Tools[/bold]")
        self.console.print("=" * 50)
        
        for tool_name in sorted(tools_info.keys()):
            tool_info = tools_info[tool_name]
            self.console.print(f"\n[cyan]{tool_name}[/cyan]: {tool_info['description']}")
            
            # Show brief parameter info
            parameters = tool_info['parameters']
            if parameters:
                required_params = [p['name'] for p in parameters if p.get('required', True)]
                optional_params = [p['name'] for p in parameters if not p.get('required', True)]
                
                param_info = []
                if required_params:
                    param_info.append(f"required: {', '.join(required_params)}")
                if optional_params:
                    param_info.append(f"optional: {', '.join(optional_params)}")
                
                if param_info:
                    self.console.print(f"  [dim]Parameters: {' | '.join(param_info)}[/dim]")
        
        self.console.print(f"\n[dim]Use ftl.help('{sorted(tools_info.keys())[0]}') for detailed help on a specific tool[/dim]")
    
    def _show_general_help(self):
        """Show general help with overview of all tools and categories."""
        tools_info = self.list_available_tools()
        
        self.console.print("\n[bold]FTL-Automation Help[/bold]")
        self.console.print("=" * 50)
        
        if not tools_info:
            self.console.print("[yellow]No tools are currently loaded[/yellow]")
            self.console.print("Load tools using: automation(tools=['tool1', 'tool2'], ...)")
            return
        
        # Show summary by category
        categories = {}
        for tool_name, tool_info in tools_info.items():
            category = tool_info['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(tool_name)
        
        self.console.print(f"[bold]Available Tools ({len(tools_info)} total)[/bold]")
        
        for category in sorted(categories.keys()):
            tools_in_category = sorted(categories[category])
            self.console.print(f"\n[magenta]{category.title()}[/magenta] ({len(tools_in_category)} tools):")
            # Show tools in columns
            tools_per_line = 4
            for i in range(0, len(tools_in_category), tools_per_line):
                line_tools = tools_in_category[i:i + tools_per_line]
                formatted_tools = [f"[cyan]{tool}[/cyan]" for tool in line_tools]
                self.console.print(f"  {' '.join(formatted_tools)}")
        
        # Show usage instructions
        self.console.print(f"\n[bold]Usage:[/bold]")
        self.console.print("  [green]ftl.help('tool_name')[/green]     - Show detailed help for a specific tool")
        self.console.print("  [green]ftl.help(category='file')[/green] - Show all tools in a category")
        self.console.print("  [green]ftl.show_tools()[/green]         - Show tools in a formatted table")
        self.console.print("  [green]ftl.show_tools(detailed=True)[/green] - Show tools with parameter details")

    def _discover_modules(self) -> List[str]:
        """Auto-discover modules in common locations.
        
        Returns:
            List of discovered module directory paths
        """
        search_patterns = [
            './modules',                    # Current directory
            '../*/modules',                 # Sibling project modules  
            '../../*/modules',              # Parent level projects
            os.path.expanduser('~/.ftl/modules'),  # User modules directory
        ]
        
        discovered = []
        
        for pattern in search_patterns:
            try:
                # Use glob to find matching directories
                matches = glob.glob(pattern)
                for match in matches:
                    if os.path.isdir(match):
                        abs_path = os.path.abspath(match)
                        if abs_path not in discovered:
                            discovered.append(abs_path)
                            self.console.print(f"[dim]Discovered modules: {abs_path}[/dim]")
            except Exception as e:
                # Silently continue if pattern fails
                self.console.print(f"[yellow]Warning: Module discovery pattern failed: {pattern} - {e}[/yellow]")
                continue
        
        return discovered
    
    def _resolve_module_paths(self, module_paths: List[str]) -> List[str]:
        """Convert relative paths to absolute paths and validate existence.
        
        Args:
            module_paths: List of module path strings
            
        Returns:
            List of validated absolute paths
        """
        resolved = []
        
        for path in module_paths:
            try:
                abs_path = os.path.abspath(path)
                if os.path.exists(abs_path) and os.path.isdir(abs_path):
                    resolved.append(abs_path)
                    self.console.print(f"[dim]Using modules: {abs_path}[/dim]")
                else:
                    self.console.print(f"[yellow]Warning: Module path not found or not a directory: {path}[/yellow]")
            except Exception as e:
                self.console.print(f"[yellow]Warning: Error resolving module path {path}: {e}[/yellow]")
                continue
        
        return resolved

    def cleanup(self):
        """Cleanup resources."""
        # Close any open gates
        if hasattr(self, "gate_cache"):
            # Add cleanup logic for gates if needed
            pass
