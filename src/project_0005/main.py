"""Main script to calculate area of a circle."""
from utils import circle_area

def main():
    try:
        radius = float(input("Enter the radius of the circle: "))
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    area = circle_area(radius)
    print(f"The area of the circle with radius {radius} is {area:.2f}")

if __name__ == "__main__":
    main()