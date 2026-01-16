# Claude Feature Requests for FTL-Automation

Based on real-world usage of ftl-automation and ftl-tools for complex automation tasks like Minecraft server deployment, these feature requests would significantly improve the developer experience and reduce common errors.

## 1. Parameter Validation & Error Messages

**Priority**: High
**Problem**: Tools fail with cryptic parameter errors that require trial-and-error debugging.

```python
# Current - fails with "unexpected keyword argument 'path'"
ftl.mkdir(path="/etc/ddclient")  # Wrong parameter name

# Desired behavior
ftl.mkdir(path="/etc/ddclient")
# ValueError: mkdir tool uses 'name' parameter, not 'path'. Use: ftl.mkdir(name='/path/to/dir')
```

**Implementation**: Add parameter validation with helpful error messages in AutomationTool base class:

```python
class AutomationTool:
    # Define parameter mappings for common mistakes
    parameter_hints = {
        'path': 'name',  # For tools that use 'name' instead of 'path'
    }
    
    def __call__(self, **kwargs):
        # Check for common parameter mistakes
        for wrong_param, correct_param in self.parameter_hints.items():
            if wrong_param in kwargs and hasattr(self, 'expected_params'):
                if correct_param in self.expected_params:
                    raise ValueError(f"{self.__class__.__name__} tool uses '{correct_param}' parameter, not '{wrong_param}'. Use: ftl.{self.name}({correct_param}='{kwargs[wrong_param]}')")
```

## 2. Consistent Parameter Naming

**Priority**: High
**Problem**: Inconsistent parameter names across similar tools create confusion.

**Current State**:
- `mkdir` uses `name`
- `chown` uses `location` 
- `copy` uses `dest`
- `get_url` uses `dest`

**Proposed Standardization**:
```python
# File/directory path operations - use 'path'
ftl.mkdir(path="/etc/ddclient")
ftl.chown(path="/home/ben", owner="ben", group="wheel")

# File operations with source/destination - keep src/dest for clarity
ftl.copy(src="file.txt", dest="/target/path")
ftl.get_url(url="http://example.com", dest="/target/file")

# Service operations - use 'name'
ftl.service(name="nginx", state="started")
ftl.user(name="ben", group="wheel")
```

**Implementation**: 
1. Update tool signatures to use consistent naming
2. Add backward compatibility with deprecation warnings
3. Update documentation to reflect standard naming conventions

## 3. Better Tool Discovery

**Priority**: Medium
**Problem**: Tool import warnings are confusing and don't help identify available tools.

```python
# Current confusing output
Warning: Tool 'mkdir' not found in any of the specified packages
```

**Proposed Solution**: Add tool discovery helper:

```python
# In ftl-automation context
def list_available_tools(self):
    """List all available tools with their parameters"""
    return {
        'mkdir': {
            'parameters': ['path'],
            'description': 'Create directory',
            'module': 'file'
        },
        'chown': {
            'parameters': ['path', 'owner', 'group'],
            'description': 'Change file ownership',
            'module': 'file'
        },
        # ...
    }

# Usage
with ftl_automation.automation(...) as ftl:
    available = ftl.list_available_tools()
    print(f"Available tools: {', '.join(available.keys())}")
```

## 4. Tool Documentation Integration

**Priority**: Medium
**Problem**: No way to see tool help or parameters during runtime.

**Proposed Solution**: Add integrated help system:

```python
# Show specific tool documentation
ftl.help('mkdir')
# Output:
# mkdir - Create directory
# Parameters:
#   path (str): Directory path to create
# Example: ftl.mkdir(path="/etc/myapp")

# Show all tools
ftl.help()
# Output: List of all available tools with brief descriptions

# Show tools by category
ftl.help(category='file')
# Output: File management tools (mkdir, chown, copy, etc.)
```

**Implementation**: 
```python
class AutomationContext:
    def help(self, tool_name=None, category=None):
        if tool_name:
            return self._show_tool_help(tool_name)
        elif category:
            return self._show_category_help(category)
        else:
            return self._show_all_tools()
```

## 5. Better Error Handling for Missing Files

**Priority**: Medium
**Problem**: Copy operations and other file tools fail silently or with confusing errors.

**Proposed Solution**: Pre-validate file existence with helpful suggestions:

```python
class Copy(AutomationTool):
    def __call__(self, src, dest, **kwargs):
        if not os.path.exists(src):
            # Show available files in current directory
            available_files = [f for f in os.listdir('.') if os.path.isfile(f)]
            similar_files = [f for f in available_files if src.lower() in f.lower()]
            
            error_msg = f"Source file '{src}' not found."
            if similar_files:
                error_msg += f" Did you mean: {', '.join(similar_files)}?"
            else:
                error_msg += f" Available files: {', '.join(available_files[:10])}"
                if len(available_files) > 10:
                    error_msg += "..."
            
            raise FileNotFoundError(error_msg)
        # ... rest of implementation
```

## 6. Tool Chaining/Pipeline Support

**Priority**: Low
**Problem**: No easy way to chain related operations that commonly go together.

**Proposed Solution**: Add pipeline support for common operation sequences:

```python
# Create directory and set ownership in one operation
ftl.pipeline([
    ('mkdir', {'path': '/etc/ddclient'}),
    ('chown', {'path': '/etc/ddclient', 'owner': 'root', 'group': 'root'}),
    ('copy', {'src': 'ddclient.conf', 'dest': '/etc/ddclient/ddclient.conf'})
])

# Or use builder pattern
ftl.mkdir(path='/etc/ddclient').then_chown(owner='root', group='root').then_copy(src='ddclient.conf')
```

## 7. Inventory Management Helpers

**Priority**: Medium
**Problem**: Manual IP extraction and inventory updates are error-prone and repetitive.

**Proposed Solution**: Add inventory helpers for common cloud operations:

```python
class AutomationContext:
    def provision_and_update_inventory(self, **linode_args):
        """Provision server and automatically update inventory with IP"""
        result = self.linode(**linode_args)
        
        # Auto-extract IP from various possible result formats
        server_ip = self._extract_ip_from_result(result)
        if server_ip:
            self._update_inventory_ip(server_ip)
            self.console.print(f"[green]Server provisioned and inventory updated: {server_ip}[/green]")
        
        return result
    
    def _extract_ip_from_result(self, result):
        """Smart IP extraction from provision results"""
        # Try various common IP field names
        ip_fields = ['ip', 'public_ip', 'ipv4', 'ip_address', 'ansible_host']
        for host_data in result.values():
            if isinstance(host_data, dict):
                for field in ip_fields:
                    if field in host_data and host_data[field]:
                        return host_data[field]
        return None
```

## 8. Dry Run Mode

**Priority**: High
**Problem**: No way to preview changes before execution, leading to accidental modifications.

**Proposed Solution**: Add comprehensive dry run support:

```python
# Enable dry run mode
with ftl_automation.automation(dry_run=True, ...) as ftl:
    ftl.mkdir(path="/etc/ddclient")  # Shows preview instead of executing
    # Output: "[DRY RUN] Would create directory: /etc/ddclient"
    
    ftl.service(name="nginx", state="started")
    # Output: "[DRY RUN] Would start service: nginx"

# Also support per-operation dry run
with ftl_automation.automation(...) as ftl:
    ftl.mkdir(path="/etc/test", dry_run=True)  # This operation only
```

**Implementation**:
```python
class AutomationTool:
    def __call__(self, dry_run=None, **kwargs):
        # Check context-level or operation-level dry run
        is_dry_run = dry_run if dry_run is not None else getattr(self.context, 'dry_run', False)
        
        if is_dry_run:
            self._show_dry_run_preview(**kwargs)
            return {'dry_run': True, 'preview': self._generate_preview(**kwargs)}
        else:
            return self._execute(**kwargs)
```

## 9. Tool Parameter Auto-completion

**Priority**: Low
**Problem**: Easy to use wrong parameter names, especially with deprecated parameters.

**Proposed Solution**: Add parameter suggestions and deprecation warnings:

```python
class AutomationTool:
    # Define deprecated parameter mappings
    deprecated_params = {
        'path': 'name',  # For tools that moved from path to name
        'user_name': 'name',  # For user tool
    }
    
    def __call__(self, **kwargs):
        # Check for deprecated parameters
        for old_param, new_param in self.deprecated_params.items():
            if old_param in kwargs:
                warnings.warn(
                    f"Parameter '{old_param}' is deprecated for {self.__class__.__name__}. "
                    f"Use '{new_param}' instead.",
                    DeprecationWarning,
                    stacklevel=2
                )
                # Auto-convert for backward compatibility
                kwargs[new_param] = kwargs.pop(old_param)
```

## 10. Better Module Path Handling

**Priority**: Low
**Problem**: Hardcoded relative module paths are fragile and break when run from different directories.

**Current Problem**:
```python
modules=["../minecraft-world7/modules"]  # Fragile relative path
```

**Proposed Solution**: Add module discovery with multiple search strategies:

```python
class AutomationContext:
    def __init__(self, modules=None, auto_discover_modules=False, **kwargs):
        if auto_discover_modules:
            discovered_modules = self._discover_modules()
            modules = modules or []
            modules.extend(discovered_modules)
        
        self.modules = self._resolve_module_paths(modules or [])
    
    def _discover_modules(self):
        """Auto-discover modules in common locations"""
        search_paths = [
            './modules',              # Current directory
            '../*/modules',           # Sibling project modules
            '../../*/modules',        # Parent level projects
            os.path.expanduser('~/.ftl/modules'),  # User modules
        ]
        
        found_modules = []
        for pattern in search_paths:
            found_modules.extend(glob.glob(pattern))
        
        return found_modules
    
    def _resolve_module_paths(self, module_paths):
        """Convert relative paths to absolute paths"""
        resolved = []
        for path in module_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                resolved.append(abs_path)
            else:
                self.console.print(f"[yellow]Warning: Module path not found: {path}[/yellow]")
        return resolved
```

## Implementation Priority

### Phase 1 (High Priority - Core UX)
1. **Parameter Validation & Error Messages** - Prevents most common errors
2. **Consistent Parameter Naming** - Reduces cognitive load  
3. **Dry Run Mode** - Enables safe experimentation

### Phase 2 (Medium Priority - Developer Experience)
4. **Tool Help System** - Improves discoverability
5. **Better Error Messages** - Faster debugging
6. **Inventory Management Helpers** - Reduces boilerplate

### Phase 3 (Low Priority - Nice to Have)
7. **Tool Chaining/Pipeline Support** - Advanced workflows
8. **Parameter Auto-completion** - Polish
9. **Better Module Discovery** - Convenience
10. **Enhanced Tool Discovery** - Power user features

## Impact Assessment

These changes would transform the ftl-automation experience from:
- **"Trial and error with cryptic failures"** 
- Manual parameter lookup in source code
- Repetitive boilerplate for common patterns
- Fear of running destructive operations

To:
- **"Guided automation with clear feedback"**
- Integrated help and parameter validation
- Reusable patterns and helpers  
- Confident iterative development with dry run mode

The most impactful changes (Phase 1) would address the majority of friction points experienced during complex automation tasks while maintaining backward compatibility.