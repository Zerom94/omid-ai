"""Utility module for the com package.

Provides helper functions that can be reused across the project.
"""

def greet(name: str) -> str:
    """Return a greeting message for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"
