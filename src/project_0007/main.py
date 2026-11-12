from utils import area_of_circle

def main():
    try:
        r = float(input('Enter the radius of the circle: '))
        if r < 0:
            print('Radius cannot be negative.')
            return
        area = area_of_circle(r)
        print(f'The area of the circle with radius {r} is {area:.2f}')
    except ValueError:
        print('Invalid input. Please enter a numeric value.')

if __name__ == '__main__':
    main()