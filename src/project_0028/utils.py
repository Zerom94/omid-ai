"""Utility functions for the example project.

This module provides a couple of simple helper functions that are used
by `main.py`.  The functions are deliberately straightforward so that the
focus remains on project structure rather than algorithmic complexity.
"""

def greet(name: str) -> str:
    """Return a friendly greeting for *name*.

    Parameters
    ----------
    name: str
        The name of the person to greet.

    Returns
    -------
    str
        A greeting string.
    """
    return f"Hello, {name}!"


def add(a: float, b: float) -> float:
    """Return the sum of *a* and *b*.

    This tiny helper demonstrates a basic arithmetic operation that can be
    reused throughout the project.
    """
    return a + b
