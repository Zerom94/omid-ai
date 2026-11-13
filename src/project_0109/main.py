#!/usr/bin/env python3
import sys
import operator
import ast

# Mapping of AST operator nodes to corresponding functions
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def evaluate(node):
    """Recursively evaluate a parsed AST expression supporting basic arithmetic."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = evaluate(node.left)
        right = evaluate(node.right)
        return OPS[type(node.op)](left, right)
    raise ValueError('Unsupported expression')

def calc(expr):
    """Parse *expr* and compute its numeric result using safe AST evaluation."""
    tree = ast.parse(expr, mode='eval')
    return evaluate(tree.body)

def main():
    # Lazy reading of input lines – memory‑efficient for large streams
    lines = (line.rstrip('\n') for line in sys.stdin)
    # Filter out empty lines using a generator expression
    for expr in (ln for ln in lines if ln.strip()):
        try:
            result = calc(expr)
            print(result)
        except Exception as exc:
            # Errors are reported to stderr without interrupting the stream
            print(f"Error: {exc}", file=sys.stderr)

if __name__ == '__main__':
    main()
