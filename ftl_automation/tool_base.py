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

    def __init__(self, automation_context):
        """
        Initialize tool with automation context.

        Args:
            automation_context: AutomationContext instance containing all state
        """
        self.context = automation_context

    def __call__(self, **kwargs) -> Any:
        """
        Tool implementation - override this method in subclasses.

        Args:
            **kwargs: Tool parameters plus automation context

        Returns:
            Tool execution result
        """
        raise NotImplementedError("Tools must implement __call__() method")
