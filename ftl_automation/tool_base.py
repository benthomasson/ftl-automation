"""
Base tool class for ftl-automation.

Provides a simple, function-based interface for automation tools that can replace
smolagents.Tool while maintaining compatibility with existing tool patterns.
"""

import inspect
from typing import Any, Dict, Optional, Callable


class AutomationTool:
    """
    Base class for ftl-automation compatible tools.

    Tools are simple functions that can be called with automation context.
    This replaces smolagents.Tool with a lightweight, dependency-free alternative.
    """

    name: str = None
    module: Optional[str] = None
    description: str = ""
    supports_dry_run: bool = True  # Most tools should support dry run mode

    def __init__(self, automation_context):
        """
        Initialize tool with automation context.

        Args:
            automation_context: AutomationContext instance containing all state
        """
        self.context = automation_context

    def __call__(self, dry_run: Optional[bool] = None, **kwargs) -> Any:
        """
        Tool implementation - override this method in subclasses.

        Args:
            dry_run: Override context-level dry run setting for this operation
            **kwargs: Tool parameters plus automation context

        Returns:
            Tool execution result or dry run preview
        """
        # Determine if this operation should be a dry run
        is_dry_run = dry_run if dry_run is not None else getattr(self.context, 'dry_run', False)
        
        if is_dry_run and not self.supports_dry_run:
            # Tool doesn't support dry run - show skipped message
            preview = f"[DRY RUN] Tool '{self.name}' does not support dry run mode - would execute normally"
            self.context.console.print(f"[yellow]{preview}[/yellow]")
            return {
                'dry_run': True,
                'skipped': True,
                'msg': f"Tool '{self.name}' does not support dry run mode",
                'preview': preview
            }
        
        # If dry run is enabled and supported, tools should override this method
        # to provide dry run functionality
        if is_dry_run:
            return self._dry_run_preview(**kwargs)
        else:
            return self._execute(**kwargs)
    
    def _execute(self, **kwargs) -> Any:
        """
        Execute the tool operation. Override this in subclasses.
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        raise NotImplementedError("Tools must implement _execute() method")
    
    def _dry_run_preview(self, **kwargs) -> Dict[str, Any]:
        """
        Generate dry run preview. Override this in subclasses for custom preview.
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            Dry run preview result
        """
        preview = f"[DRY RUN] Would execute {self.name}"
        if kwargs:
            params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            preview += f" with parameters: {params}"
        
        self.context.console.print(f"[cyan]{preview}[/cyan]")
        
        return {
            'dry_run': True,
            'changed': True,  # Assume the tool would have made changes
            'preview': preview,
            'msg': f'Dry run preview for {self.name}'
        }
