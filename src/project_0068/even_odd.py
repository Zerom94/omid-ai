def is_even(n: int) -> bool:
    """Return True if *n* is even, False otherwise."""
    return n % 2 == 0


def check_number(n: int) -> str:
    """Return a string indicating whether *n* is "Even" or "Odd".

    Parameters
    ----------
    n : int
        The integer to evaluate.
    """
    return "Even" if is_even(n) else "Odd"
