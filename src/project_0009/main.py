from geometry import area_of_circle

def main():
    try:
        r = float(input('Enter the radius: '))
        if r < 0:
            raise ValueError('Radius cannot be negative')
        area = area_of_circle(r)
        print(f'Area of the circle: {area:.2f}')
    except ValueError as e:
        print(f'Invalid input: {e}')

if __name__ == '__main__':
    main()