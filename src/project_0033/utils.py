def power(base: float, exponent: int) -> float:
    """
    Compute base raised to the power exponent.

    Parameters
    ----------
    base : float
        The base number.
    exponent : int
        The exponent (can be negative or zero).

    Returns
    -------
    float
        The result of ``base ** exponent``.
    """
    # Using Python's built‑in exponentiation operator ensures correct handling of
    # negative exponents, zero, and large numbers.
    return base ** exponent
