import argparse
from even_odd import check_number

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether given integer(s) are even or odd."
    )
    parser.add_argument(
        "numbers",
        metavar="N",
        type=int,
        nargs="+",
        help="One or more integers to evaluate."
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    for number in args.numbers:
        result = check_number(number)
        print(f"{number}: {result}")

if __name__ == "__main__":
    main()
