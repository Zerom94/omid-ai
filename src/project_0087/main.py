# Entry point for the com package demo

from com.example import Greeter

def main():
    greeter = Greeter(name="World")
    greeter.greet()

if __name__ == "__main__":
    main()
