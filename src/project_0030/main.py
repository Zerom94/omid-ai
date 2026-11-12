from utils import power


def main():
    # Example usages of the power function
    examples = [
        (2, 5),   # 2^5 = 32
        (3, 3),   # 3^3 = 27
        (5, 0),   # 5^0 = 1
        (4, -2),  # 4^-2 = 0.0625
    ]

    for base, exp in examples:
        result = power(base, exp)
        print(f"{base}^{exp} = {result}")


if __name__ == "__main__":
    main()
