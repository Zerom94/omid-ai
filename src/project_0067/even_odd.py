def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0

def check_number(n: int) -> str:
    """Return a string indicating whether n is even or odd."""
    return f"{n} is even" if is_even(n) else f"{n} is odd"
