#!/usr/bin/env python3
import operator
import sys
from typing import Callable, Iterable

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
}

def evaluate(expr: str) -> float:
    """Evaluate a simple space‑separated expression like '3 + 4 * 2'."""
    # Token generator – lazy evaluation
    def tokens() -> Iterable[str]:
        return (t for t in expr.split())
    # Convert infix to RPN using Shunting‑Yard algorithm (lazy)
    output = []
    stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_assoc = {'^'}
    for token in tokens():
        if token.replace('.','',1).lstrip('-').isdigit():
            output.append(float(token))
        elif token in OPS:
            while (stack and stack[-1] in OPS and
                   (precedence[stack[-1]] > precedence[token] or
                    (precedence[stack[-1]] == precedence[token] and token not in right_assoc))):
                output.append(stack.pop())
            stack.append(token)
        else:
            raise ValueError(f'Unknown token: {token}')
    while stack:
        output.append(stack.pop())
    # Evaluate RPN using a generator for the stack
    def rpn_eval(seq):
        stack = []
        for item in seq:
            if isinstance(item, float):
                stack.append(item)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(OPS[item](a, b))
        return stack[0]
    return rpn_eval(output)

def main(args: list[str] | None = None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        # interactive REPL
        print('Basic Calculator – type "exit" to quit')
        while True:
            line = input('> ').strip()
            if line.lower() in ('exit', 'quit'):
                break
            if not line:
                continue
            try:
                result = evaluate(line)
                print(result)
            except Exception as e:
                print(f'Error: {e}')
    else:
        # evaluate each argument as an expression
        results = (str(evaluate(expr)) for expr in args)
        # join using newline – efficient string building
        sys.stdout.write('\n'.join(results))

if __name__ == '__main__':
    main()
