from fib import fibonacci, fibonacci_sequence

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fibonacci utilities')
    parser.add_argument('n', type=int, nargs='?', default=10,
                        help='Compute the nth Fibonacci number (default: 10)')
    parser.add_argument('--list', type=int, metavar='LIMIT',
                        help='Print all Fibonacci numbers up to LIMIT')
    args = parser.parse_args()

    if args.list is not None:
        print(f"Fibonacci numbers up to {args.list}:")
        print(', '.join(str(num) for num in fibonacci_sequence(args.list)))
    else:
        try:
            result = fibonacci(args.n)
            print(f"Fibonacci number F({args.n}) = {result}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
