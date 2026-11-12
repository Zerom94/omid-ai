import argparse
from utils import greet

def main():
    parser = argparse.ArgumentParser(description="Simple greeting script.")
    parser.add_argument("name", nargs="?", default="World", help="Name to greet")
    args = parser.parse_args()
    message = greet(args.name)
    print(message)

if __name__ == "__main__":
    main()
