import operator
import ast

# Mapping of AST operator nodes to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval(node):
    """Recursively evaluate an AST node representing a mathematical expression.
    Supports +, -, *, /, //, %, ** and parentheses.
    """
    if isinstance(node, ast.Num):  # < Python 3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise TypeError(f"Unsupported constant type: {type(node.value)}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](left, right)
        raise TypeError(f"Unsupported binary operator: {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            return _OPERATORS[op_type](operand)
        raise TypeError(f"Unsupported unary operator: {op_type}")
    raise TypeError(f"Unsupported AST node: {type(node)}")

def evaluate(expression: str) -> float:
    """Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expression: str
        The arithmetic expression to evaluate.

    Returns
    -------
    float
        The result of the evaluated expression.
    """
    try:
        # Parse expression into an AST node
        parsed = ast.parse(expression, mode='eval')
        return _eval(parsed.body)
    except Exception as e:
        raise ValueError(f"Invalid expression '{expression}': {e}")
