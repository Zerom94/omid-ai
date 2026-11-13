import argparse
from calculator import add, sub, mul, div

def parse_args():
    parser = argparse.ArgumentParser(description='Simple command-line calculator')
    parser.add_argument('operation', choices=['add', 'sub', 'mul', 'div'], help='Operation to perform')
    parser.add_argument('a', type=float, help='First operand')
    parser.add_argument('b', type=float, help='Second operand')
    return parser.parse_args()

def main():
    args = parse_args()
    ops = {'add': add, 'sub': sub, 'mul': mul, 'div': div}
    try:
        result = ops[args.operation](args.a, args.b)
        print(f'Result: {result}')
    except ZeroDivisionError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
