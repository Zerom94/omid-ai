import sys
from fibonacci import fibonacci

def parse_args() -> int:
    if len(sys.argv) != 2:
        print(f\"Usage: {sys.argv[0]} <non-negative integer>\")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
        if n < 0:
            raise ValueError
        return n
    except ValueError:
        print(\"Please provide a non‑negative integer.\")
        sys.exit(1)

def main():
    n = parse_args()
    seq = fibonacci(n)
    print(", ".join(map(str, seq)))

if __name__ == \"__main__\":
    main()
