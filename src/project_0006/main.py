from utils import area_of_circle

def main():
    try:
        radius = float(input('Enter the radius of the circle: '))
    except ValueError:
        print('Invalid input. Please enter a numeric value.')
        return
    area = area_of_circle(radius)
    print(f'The area of the circle with radius {radius} is {area}')

if __name__ == '__main__':
    main()
