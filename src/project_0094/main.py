import sys
from fib import fibonacci, fibonacci_sequence

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <n> [limit]")
        return
    n = int(sys.argv[1])
    print(f"Fibonacci number F({n}) = {fibonacci(n)}")
    if len(sys.argv) >= 3:
        limit = int(sys.argv[2])
        seq = list(fibonacci_sequence(limit))
        print(f"Fibonacci numbers up to {limit}: {seq}")

if __name__ == "__main__":
    main()
