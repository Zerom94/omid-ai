from utils import add, subtract, multiply, divide, power

def print_menu():
    print(\"Simple Calculator\")
    print(\"-----------------\")
    print(\"Available operations:\")
    print(\"1. Add\")
    print(\"2. Subtract\")
    print(\"3. Multiply\")
    print(\"4. Divide\")
    print(\"5. Power\")
    print(\"6. Exit\")

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(\"Invalid number, please try again.\")

def main():
    while True:
        print_menu()
        choice = input(\"Select an option (1-6): \").strip()
        if choice == '6':
            print(\"Goodbye!\")
            break
        if choice not in {'1','2','3','4','5'}:
            print(\"Invalid choice, try again.\")
            continue
        a = get_number(\"Enter first number: \")
        b = get_number(\"Enter second number: \")
        try:
            if choice == '1':
                result = add(a, b)
                op = '+'
            elif choice == '2':
                result = subtract(a, b)
                op = '-'
            elif choice == '3':
                result = multiply(a, b)
                op = '*'
            elif choice == '4':
                result = divide(a, b)
                op = '/'
            elif choice == '5':
                result = power(a, b)
                op = '^'
            print(f\"{a} {op} {b} = {result}\")
        except ZeroDivisionError as e:
            print(e)

if __name__ == \"__main__\":
    main()
