# Claude Feature Requests for FTL-Automation

Based on real-world usage of ftl-automation and ftl-tools for complex automation tasks like Minecraft server deployment, these feature requests would significantly improve the developer experience and reduce common errors.

## Implementation Status

**✅ COMPLETED** (5/10):
- ✅ **Better Tool Discovery** - `list_available_tools()` and `show_tools()` methods implemented
- ✅ **Tool Documentation Integration** - Comprehensive `help()` system with examples and parameter tables  
- ✅ **Dry Run Mode** - Comprehensive implementation with context/operation-level control and universal tool support
- ✅ **Consistent Parameter Naming** - File operations standardized across all tools
- ✅ **Better Module Path Handling** - Auto-discovery with search patterns and path resolution

**🚧 PARTIALLY COMPLETED** (0/10):
- (No partially completed features remaining)

**📋 PENDING** (5/10):
- 📋 **Better Error Handling for Missing Files** - Medium priority
- 📋 **Inventory Management Helpers** - Medium priority
- 📋 **Parameter Validation & Error Messages** - Low priority (runtime validation for typos)
- 📋 **Tool Chaining/Pipeline Support** - Low priority
- 📋 **Tool Parameter Auto-completion** - Low priority

## 1. Parameter Validation & Error Messages

**Priority**: Low  
**Status**: 🚧 **PARTIALLY COMPLETED** - Help system provides parameter discovery, runtime validation now low priority due to consistent naming
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
**Status**: 🚧 **PARTIALLY COMPLETED** - File operations standardized, validation updated
**Problem**: Inconsistent parameter names across similar tools create confusion.

**✅ COMPLETED STANDARDIZATION**:
- `mkdir` uses `path` ✅ (was `name`)
- `chown` uses `user`, `path` ✅ (was `location`) 
- `chmod` uses `permissions`, `path` ✅
- `lineinfile` uses `line`, `path` ✅
- `copy` uses `src`, `dest` ✅
- `get_url` uses `url`, `dest` ✅
- `template` uses `src`, `dest` ✅
- `unarchive` uses `src`, `dest` ✅

**Consistent Patterns Achieved**:
- **Single target operations** → `path` parameter
- **Source→destination operations** → `src`/`dest` parameters

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
**Status**: ✅ **COMPLETED** - `list_available_tools()` and `show_tools()` implemented
**Problem**: Tool import warnings are confusing and don't help identify available tools.

```python
# Current confusing output
Warning: Tool 'mkdir' not found in any of the specified packages
```

**✅ IMPLEMENTED SOLUTION**:

```python
# Available methods in AutomationContext
ftl.list_available_tools(category=None)  # Returns detailed tool metadata
ftl.show_tools(category=None, detailed=False)  # Rich table display
ftl.help()  # General help overview by category

# Example usage
with ftl_automation.automation(tools=['mkdir', 'user', 'slack']) as ftl:
    # Programmatic access
    tools = ftl.list_available_tools()
    file_tools = ftl.list_available_tools(category='file')
    
    # Visual display
    ftl.show_tools()  # All tools in table
    ftl.show_tools(category='system', detailed=True)  # System tools with parameters
```

**Features Implemented**:
- Dynamic tool introspection with parameters, types, and descriptions
- Category-based organization (file, system, package, security, development, cloud, notification, automation)
- Rich formatted table output with color coding
- Programmatic access to tool metadata

## 4. Tool Documentation Integration

**Priority**: Medium  
**Status**: ✅ **COMPLETED** - Comprehensive `help()` system implemented
**Problem**: No way to see tool help or parameters during runtime.

**✅ IMPLEMENTED SOLUTION**:

```python
# Three help modes implemented
ftl.help('mkdir')           # Detailed tool help with parameters table and examples
ftl.help(category='file')   # Category-specific help
ftl.help()                  # General overview of all tools

# Example output for ftl.help('mkdir'):
# mkdir - Make a directory on the remote machine
# Category: file
# Parameters:
# ┏━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
# ┃ Parameter ┃ Type ┃ Required ┃ Default ┃
# ┡━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
# │ path      │ str  │ Yes      │         │
# └───────────┴──────┴──────────┴─────────┘
# Example: ftl.mkdir(path="/opt/myapp")
```

**Features Implemented**:
- Rich formatted parameter tables with types and requirements
- Smart example generation with realistic parameter values
- Error handling with tool suggestions for typos  
- Category-based help navigation
- Tool-specific examples like `ftl.user(name="myuser", group="wheel")`
- Integration with tool discovery system

## 5. Better Error Handling for Missing Files

**Priority**: Medium  
**Status**: 📋 **PENDING** - Not yet implemented
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
**Status**: 📋 **PENDING** - Not yet implemented
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
**Status**: 📋 **PENDING** - Not yet implemented
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
**Status**: ✅ **COMPLETED** - Comprehensive implementation with context/operation-level control and full tool integration
**Problem**: No way to preview changes before execution, leading to accidental modifications.

**✅ IMPLEMENTED SOLUTION**: Full dry run support across entire ftl-automation ecosystem:

```python
# Enable dry run mode for entire context
with ftl_automation.automation(dry_run=True, ...) as ftl:
    ftl.dnf(name="nginx", state="present")  # Shows what would be installed
    ftl.service(name="nginx", state="started")  # Shows service would be started
    ftl.firewalld(port="80/tcp", state="enabled")  # Shows firewall changes

# Per-operation dry run override
with ftl_automation.automation(...) as ftl:
    ftl.service(name="nginx", state="started", dry_run=True)  # This operation only
    
# Command-line support
python3 minecraft_automation.py --dry-run  # Preview entire automation workflow
```

**✅ FEATURES IMPLEMENTED**:
- **Context-level dry run**: `automation(dry_run=True)` affects all operations
- **Operation-level override**: Individual tool calls can override context setting
- **CLI integration**: `--dry-run` flag support in automation scripts
- **Ansible check_mode**: Automatic conversion to `_ansible_check_mode=True` for all modules
- **Universal tool support**: All 24 ftl-tools now support dry run mode
- **Builtin tool support**: debug, user_input, complete, impossible tools have dry run previews

**✅ IMPLEMENTATION ARCHITECTURE**:
```python
# ftl-automation framework (AutomationTool base class)
class AutomationTool:
    def __call__(self, dry_run: Optional[bool] = None, **kwargs) -> Any:
        is_dry_run = dry_run if dry_run is not None else getattr(self.context, 'dry_run', False)
        if is_dry_run:
            return self._dry_run_preview(**kwargs)
        else:
            return self._execute(**kwargs)

# ftl-tools individual tool implementation
def __call__(self, name: str, state: str):
    module_args = dict(name=name, state=state)
    if getattr(self.context, 'dry_run', False):
        module_args['_ansible_check_mode'] = True
    return ftl.run_module_sync(..., module_args=module_args, ...)
```

**✅ TESTING VERIFIED**:
- Minecraft automation scripts run safely in dry-run mode
- Package operations show "would install X" instead of actual installation
- Service operations show "service state changed" without actual changes
- File operations preview modifications without touching files

## 9. Tool Parameter Auto-completion

**Priority**: Low  
**Status**: 📋 **PENDING** - Not yet implemented
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
**Status**: ✅ **COMPLETED** - Auto-discovery and path resolution implemented
**Problem**: Hardcoded relative module paths are fragile and break when run from different directories.

**✅ IMPLEMENTED SOLUTION**: Module auto-discovery with intelligent search patterns:

```python
# Enable auto-discovery
with ftl_automation.automation(
    inventory="inventory.yml",
    auto_discover_modules=True,  # Automatically find modules
    tools=["bash", "copy"]
) as ftl:
    # Automatically discovers modules from:
    # - ./modules (current directory)
    # - ../*/modules (sibling projects)  
    # - ../../*/modules (parent projects)
    # - ~/.ftl/modules (user modules)
    pass

# Combine manual + auto-discovery
with ftl_automation.automation(
    modules=["./custom_modules"],  # Manual modules
    auto_discover_modules=True,    # Plus auto-discovery
    tools=["bash"]
) as ftl:
    # Uses both manual and discovered modules
    pass
```

**✅ FEATURES IMPLEMENTED**:
- **Auto-discovery patterns**: Searches common locations for module directories
- **Path resolution**: Converts relative paths to absolute paths with validation
- **Multi-project support**: Finds modules from related projects automatically
- **Fallback handling**: Graceful warnings for missing paths
- **Combined mode**: Manual modules + auto-discovery

**✅ IMPLEMENTATION**:
```python
def _discover_modules(self) -> List[str]:
    search_patterns = [
        './modules',                    # Current directory
        '../*/modules',                 # Sibling project modules  
        '../../*/modules',              # Parent level projects
        os.path.expanduser('~/.ftl/modules'),  # User modules
    ]
    # Auto-discovery with glob patterns and validation

def _resolve_module_paths(self, module_paths: List[str]) -> List[str]:
    # Convert to absolute paths and validate existence
    # Provides helpful warnings for missing directories
```

**✅ BENEFITS ACHIEVED**:
- No more hardcoded relative paths like `../minecraft-world7/modules`
- Works from any directory in project structure
- Automatically finds modules from related projects
- Eliminates fragile path dependencies

## Implementation Priority

### ✅ Phase 1 (High Priority - Core UX) - COMPLETE
1. ~~**Consistent Parameter Naming**~~ - ✅ **COMPLETED** - File operations standardized
2. ~~**Dry Run Mode**~~ - ✅ **COMPLETED** - Comprehensive implementation across all tools

### ✅ Phase 2 (Medium Priority - Developer Experience) - PARTIALLY COMPLETE  
4. ~~**Tool Help System**~~ - ✅ **COMPLETED** - Comprehensive help system implemented
5. **Better Error Messages** - 📋 **PENDING** - Faster debugging
6. **Inventory Management Helpers** - 📋 **PENDING** - Reduces boilerplate  
7. ~~**Enhanced Tool Discovery**~~ - ✅ **COMPLETED** - `list_available_tools()` and `show_tools()`

### 📋 Phase 3 (Low Priority - Nice to Have) - PARTIALLY COMPLETE
8. ~~**Better Module Discovery**~~ - ✅ **COMPLETED** - Auto-discovery with search patterns
9. **Parameter Validation & Error Messages** - 📋 **PENDING** - Runtime validation for typos (downgraded from high priority)
10. **Tool Chaining/Pipeline Support** - 📋 **PENDING** - Advanced workflows
11. **Parameter Auto-completion** - 📋 **PENDING** - Polish

### 🎯 Next Recommended Implementation
**Medium Priority**: **Better Error Handling for Missing Files** - Would improve debugging experience by providing helpful suggestions when file operations fail due to missing source files.

## Impact Assessment

### ✅ **Progress So Far (5/10 features completed)**:
**BEFORE** (painful experience):
- ❌ Trial and error with cryptic parameter failures (`mkdir(name=...)` vs `mkdir(path=...)`)
- ❌ Manual parameter lookup in source code  
- ❌ No way to discover available tools and their parameters
- ❌ Inconsistent parameter naming across similar tools
- ❌ Fear of running destructive operations without preview

**AFTER** (improved experience): 
- ✅ **Consistent parameter naming** - All file operations use logical `path` or `src`/`dest` patterns
- ✅ **Integrated help system** - `ftl.help('mkdir')` shows parameters, types, and examples
- ✅ **Tool discovery** - `ftl.show_tools()` reveals available tools by category
- ✅ **Runtime documentation** - No need to check source code for parameter names
- ✅ **Comprehensive dry run mode** - `--dry-run` flag enables safe preview of all operations
- ✅ **Automatic module discovery** - `auto_discover_modules=True` finds modules from related projects

### 📋 **Still To Address (5/10 remaining)**:
- 📋 File operation error debugging → Better error messages needed
- 📋 Repetitive cloud provisioning patterns → Inventory helpers needed  
- 📋 Runtime parameter typo validation → Low priority due to consistent naming
- 📋 Advanced workflow patterns → Tool chaining/pipeline support needed  
- 📋 Development convenience features → Parameter auto-completion

### 🎯 **Next High Impact**: 
**Better Error Handling for Missing Files** would improve the debugging experience by providing helpful suggestions when file operations fail, reducing trial-and-error debugging for copy/template operations.