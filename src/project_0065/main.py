import argparse
from calculator import add, subtract, multiply, divide

def main():
    parser = argparse.ArgumentParser(description="Simple calculator")
    parser.add_argument("operation", choices=["add", "sub", "mul", "div"], help="Operation to perform")
    parser.add_argument("a", type=float, help="First operand")
    parser.add_argument("b", type=float, help="Second operand")
    args = parser.parse_args()
    ops = {"add": add, "sub": subtract, "mul": multiply, "div": divide}
    try:
        result = ops[args.operation](args.a, args.b)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
