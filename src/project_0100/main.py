import argparse
from operations import add, subtract, multiply, divide

def parse_args():
    parser = argparse.ArgumentParser(description='Simple command-line calculator')
    parser.add_argument('operation', choices=['add', 'sub', 'mul', 'div'], help='Operation to perform')
    parser.add_argument('x', type=float, help='First operand')
    parser.add_argument('y', type=float, help='Second operand')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.operation == 'add':
        result = add(args.x, args.y)
    elif args.operation == 'sub':
        result = subtract(args.x, args.y)
    elif args.operation == 'mul':
        result = multiply(args.x, args.y)
    elif args.operation == 'div':
        result = divide(args.x, args.y)
    print(f'Result: {result}')

if __name__ == '__main__':
    main()
