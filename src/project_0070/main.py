from fib import fibonacci
import sys

def parse_args():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <non-negative integer>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
    if n < 0:
        print("Argument must be non-negative.")
        sys.exit(1)
    return n

def main():
    n = parse_args()
    result = fibonacci(n)
    print(f"Fibonacci({n}) = {result}")

if __name__ == "__main__":
    main()
