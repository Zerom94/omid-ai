import sys
from calculator import Calculator

def print_usage():
    print("Usage: python main.py <operation> <num1> <num2>")
    print("Operations: add, sub, mul, div")

def main():
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    operation, a_str, b_str = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        print("Error: Both numbers must be valid numeric values.")
        sys.exit(1)

    calc = Calculator()
    try:
        if operation == "add":
            result = calc.add(a, b)
        elif operation == "sub":
            result = calc.subtract(a, b)
        elif operation == "mul":
            result = calc.multiply(a, b)
        elif operation == "div":
            result = calc.divide(a, b)
        else:
            print(f"Unsupported operation: {operation}")
            print_usage()
            sys.exit(1)
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
