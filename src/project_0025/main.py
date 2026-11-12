from utils import factorial

def main():
    try:
        n = int(input('Enter a non‑negative integer: '))
        print(f"{n}! = {factorial(n)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
