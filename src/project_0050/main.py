import argparse
from factorial import factorial

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate factorial of a non‑negative integer.")
    parser.add_argument("number", type=int, help="Non‑negative integer to compute factorial of.")
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        result = factorial(args.number)
        print(f"{args.number}! = {result}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
