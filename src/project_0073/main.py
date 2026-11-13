#!/usr/bin/env python3
import sys
from calculator import Calculator

def print_usage():
    print("Usage: python main.py <operation> <num1> <num2>")
    print("Operations: add, sub, mul, div")

def main():
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    op, a_str, b_str = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        print("Error: both numbers must be valid numeric values.")
        sys.exit(1)

    try:
        if op == "add":
            result = Calculator.add(a, b)
        elif op == "sub":
            result = Calculator.subtract(a, b)
        elif op == "mul":
            result = Calculator.multiply(a, b)
        elif op == "div":
            result = Calculator.divide(a, b)
        else:
            print(f"Unknown operation: {op}")
            print_usage()
            sys.exit(1)
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
