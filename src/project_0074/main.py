#!/usr/bin/env python3
import argparse
from calculator import Calculator

def parse_args():
    parser = argparse.ArgumentParser(description='Simple command-line calculator')
    parser.add_argument('operation', choices=['add', 'sub', 'mul', 'div'], help='Operation to perform')
    parser.add_argument('x', type=float, help='First operand')
    parser.add_argument('y', type=float, help='Second operand')
    return parser.parse_args()

def main():
    args = parse_args()
    calc = Calculator()
    ops = {
        'add': calc.add,
        'sub': calc.subtract,
        'mul': calc.multiply,
        'div': calc.divide,
    }
    try:
        result = ops[args.operation](args.x, args.y)
        print(f'Result: {result}')
    except ZeroDivisionError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()