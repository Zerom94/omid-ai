import sys
from even_odd import check_number

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <integer>")
        sys.exit(1)
    try:
        number = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid integer.")
        sys.exit(1)
    print(check_number(number))

if __name__ == "__main__":
    main()
