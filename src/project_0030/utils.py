def power(base, exponent):
    """Calculate base raised to the exponent.

    Supports positive, zero, and negative integer exponents.
    """
    # Handle zero exponent
    if exponent == 0:
        return 1

    # Work with positive exponent for the loop
    positive_exp = abs(exponent)
    result = 1
    for _ in range(positive_exp):
        result *= base

    # If exponent was negative, invert the result
    if exponent < 0:
        return 1 / result
    return result
