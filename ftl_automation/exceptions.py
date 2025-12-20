"""
Exception classes for ftl-automation.

Provides specialized exceptions for automation flow control.
"""


class CompletionException(Exception):
    """Exception raised to signal successful task completion."""
    pass


class ImpossibleException(Exception):
    """Exception raised to signal that a task is impossible to complete."""
    pass