#!/usr/bin/env python3
import sys
import operator
import ast

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

def eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](eval_node(node.left), eval_node(node.right))
    raise ValueError('Unsupported expression')

def calculate(expr):
    try:
        tree = ast.parse(expr, mode='eval')
        return eval_node(tree.body)
    except Exception as e:
        return f'Error: {e}'

def main():
    print('Simple calculator. Type "exit" to quit.')
    for line in (ln.rstrip() for ln in sys.stdin):
        if line.lower() == 'exit':
            break
        if not line:
            continue
        result = calculate(line)
        print(result)

if __name__ == '__main__':
    main()
