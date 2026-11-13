import sys
from calculator import evaluate

def print_help():
    print("Simple Calculator")
    print("Usage: python main.py <expression>")
    print("Example: python main.py \"(2 + 3) * 4 - 5/2\"")

def main():
    if len(sys.argv) != 2:
        print_help()
        sys.exit(1)
    expr = sys.argv[1]
    try:
        result = evaluate(expr)
        print(f"Result: {result}")
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)

if __name__ == "__main__":
    main()
