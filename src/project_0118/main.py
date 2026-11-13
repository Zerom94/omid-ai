# -*- coding: utf-8 -*-
"""calculator
================
A tiny yet fully‑featured command line calculator.

Features
--------
* Basic arithmetic: addition, subtraction, multiplication, division.
* Input validation – non‑numeric operands raise a clear ``ValueError``.
* Division‑by‑zero is caught and reported as ``ZeroDivisionError``.
* Can be used programmatically via the public ``calculate`` function or
  interactively from the terminal.
* Type hints and thorough docstrings for maintainability.
* PEP 8 compliant.

Typical usage::

    $ python main.py 3 + 5
    8.0

    >>> from main import calculate
    >>> calculate(10, '/', 2)
    5.0
"""

from __future__ import annotations

import argparse
import operator
import sys
from typing import Callable, Dict, Tuple

# Mapping of operator symbols to the corresponding functions from ``operator``.
_OPERATIONS: Dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def _parse_operand(value: str) -> float:
    """Convert a string operand to ``float``.

    Parameters
    ----------
    value:
        The string representation of the operand.

    Returns
    -------
    float
        The numeric value.

    Raises
    ------
    ValueError
        If ``value`` cannot be converted to a ``float``.
    """
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric operand: {value!r}") from exc


def calculate(lhs: float | str, op: str, rhs: float | str) -> float:
    """Perform a binary arithmetic operation.

    The function accepts either ``float`` values or strings that can be cast
    to ``float``.  Supported operators are ``+``, ``-``, ``*`` and ``/``.

    Parameters
    ----------
    lhs:
        Left‑hand side operand.
    op:
        Operator as a string (e.g. ``"+"``).
    rhs:
        Right‑hand side operand.

    Returns
    -------
    float
        The result of the calculation.

    Raises
    ------
    ValueError
        If the operator is unsupported or an operand cannot be parsed.
    ZeroDivisionError
        If division by zero is attempted.
    """
    if op not in _OPERATIONS:
        raise ValueError(f"Unsupported operator: {op!r}. Supported: {', '.join(_OPERATIONS)}")

    left = _parse_operand(str(lhs))
    right = _parse_operand(str(rhs))

    # ``operator.truediv`` will raise ``ZeroDivisionError`` for a zero divisor.
    result = _OPERATIONS[op](left, right)
    return result


def _build_parser() -> argparse.ArgumentParser:
    """Create the ``argparse`` parser for command‑line usage.

    Returns
    -------
    argparse.ArgumentParser
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="Perform a single binary arithmetic operation.",
    )
    parser.add_argument("lhs", help="Left‑hand side operand (numeric)")
    parser.add_argument("op", help="Operator (+, -, *, /)")
    parser.add_argument("rhs", help="Right‑hand side operand (numeric)")
    return parser


def _main(argv: Tuple[str, ...] | None = None) -> int:
    """Entry point for the CLI.

    Parameters
    ----------
    argv:
        Optional tuple of arguments (excluding the program name).  If ``None``
        the arguments are taken from ``sys.argv[1:]``.

    Returns
    -------
    int
        Exit status code – ``0`` for success, ``1`` for error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        result = calculate(args.lhs, args.op, args.rhs)
    except (ValueError, ZeroDivisionError) as exc:
        parser.error(str(exc))
        return 1

    # ``print`` ensures the result is written to ``stdout`` in a user‑friendly way.
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
