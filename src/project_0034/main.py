import argparse
from utils import add, subtract, multiply

def main():
    parser = argparse.ArgumentParser(description='Simple calculator')
    parser.add_argument('operation', choices=['add', 'sub', 'mul'], help='Operation to perform')
    parser.add_argument('x', type=float, help='First operand')
    parser.add_argument('y', type=float, help='Second operand')
    args = parser.parse_args()

    if args.operation == 'add':
        result = add(args.x, args.y)
    elif args.operation == 'sub':
        result = subtract(args.x, args.y)
    else:  # 'mul'
        result = multiply(args.x, args.y)

    print(f'Result: {result}')

if __name__ == '__main__':
    main()
