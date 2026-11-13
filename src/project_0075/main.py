import sys
from calculator import add, subtract, multiply, divide

def print_help():
    print("Simple Calculator")
    print("Usage: python main.py <operation> <num1> <num2>")
    print("Operations: add, sub, mul, div")
    print("Example: python main.py add 5 3")

def main():
    if len(sys.argv) != 4:
        print_help()
        sys.exit(1)

    op = sys.argv[1].lower()
    try:
        a = float(sys.argv[2])
        b = float(sys.argv[3])
    except ValueError:
        print("Error: both numbers must be valid numeric values.")
        sys.exit(1)

    try:
        if op in ("add", "+"):
            result = add(a, b)
        elif op in ("sub", "subtract", "-"):
            result = subtract(a, b)
        elif op in ("mul", "multiply", "*"):
            result = multiply(a, b)
        elif op in ("div", "divide", "/"):
            result = divide(a, b)
        else:
            print(f"Unsupported operation: {op}")
            print_help()
            sys.exit(1)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
