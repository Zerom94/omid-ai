#!/usr/bin/env python3

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b.
    Raises ZeroDivisionError if b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def get_number(prompt):
    """Prompt the user until a valid float is entered."""
    while True:
        try:
            value = input(prompt)
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_choice():
    """Display the menu and return the user's choice as an integer."""
    print("\n=== Basic Calculator ===")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")
    while True:
        choice = input("Select an option (1-5): ")
        if choice in {"1", "2", "3", "4", "5"}:
            return int(choice)
        else:
            print("Invalid selection. Please choose a number between 1 and 5.")


def main():
    """Main loop handling user interaction and calculations."""
    while True:
        choice = get_choice()
        if choice == 5:
            print("Goodbye!")
            break

        a = get_number("Enter the first number: ")
        b = get_number("Enter the second number: ")

        try:
            if choice == 1:
                result = add(a, b)
                op = '+'
            elif choice == 2:
                result = subtract(a, b)
                op = '-'
            elif choice == 3:
                result = multiply(a, b)
                op = '*'
            elif choice == 4:
                result = divide(a, b)
                op = '/'
            print(f"{a} {op} {b} = {result}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
