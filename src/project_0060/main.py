import argparse
from primes import generate_primes, first_n_primes


def main():
    parser = argparse.ArgumentParser(description="Prime number utilities")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--up-to", type=int, help="Generate all primes up to this number (inclusive)")
    group.add_argument("-n", "--count", type=int, help="Generate the first N prime numbers")
    args = parser.parse_args()

    if args.up_to is not None:
        for p in generate_primes(args.up_to):
            print(p)
    else:
        for p in first_n_primes(args.count):
            print(p)


if __name__ == "__main__":
    main()
