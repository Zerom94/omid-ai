#!/usr/bin/env python3
"""Simple command-line calculator.

Supports addition, subtraction, multiplication, division,
exponentiation and parentheses.
"""

import operator
import sys
from typing import Callable, Dict


class CalculatorError(Exception):
    """Base class for calculator errors."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when the input expression cannot be parsed."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero occurs."""
    pass


def evaluate(expression: str) -> float:
    """Evaluate a mathematical expression safely.

    Args:
        expression: The arithmetic expression to evaluate.

    Returns:
        The result of the evaluation as a float.

    Raises:
        InvalidExpressionError: If the expression is syntactically invalid.
        DivisionByZeroError: If a division by zero is attempted.
    """
    # Define allowed operators
    allowed_operators: Dict[str, Callable[[float, float], float]] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
    }

    # Replace '^' with '**' for exponentiation
    expr = expression.replace('^', '**')
    try:
        # Compile the expression to AST and ensure it contains only allowed names
        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_operators:
                raise InvalidExpressionError(f"Unsupported identifier: {name}")
        # Evaluate with restricted globals
        result = eval(code, {"__builtins__": {}}, allowed_operators)
        if isinstance(result, (int, float)):
            return float(result)
        raise InvalidExpressionError("Expression did not evaluate to a number.")
    except ZeroDivisionError as exc:
        raise DivisionByZeroError("Division by zero.") from exc
    except (SyntaxError, NameError) as exc:
        raise InvalidExpressionError("Invalid expression.") from exc


def main() -> None:
    """Run the interactive calculator loop."""
    print("Simple Calculator. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if not user_input:
                continue
            result = evaluate(user_input)
            print(result)
        except CalculatorError as err:
            print(f"Error: {err}")
        except KeyboardInterrupt:
            print("\nInterrupted. Type 'exit' to quit.")
        except Exception as exc:  # Catch unexpected errors
            print(f"Unexpected error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
