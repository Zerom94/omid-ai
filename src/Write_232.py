def fibonacci_sequence(n):
    """Return a list containing the first n Fibonacci numbers."""
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def main():
    count = 10
    fib_numbers = fibonacci_sequence(count)
    for i, num in enumerate(fib_numbers, start=1):
        print(f"{i}: {num}")

if __name__ == "__main__":
    main()