def add(a, b):
    \"\"\"Return the sum of a and b.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Return the difference of a and b.\"\"\"
    return a - b

def multiply(a, b):
    \"\"\"Return the product of a and b.\"\"\"
    return a * b

def divide(a, b):
    \"\"\"Return the division of a by b. Raises ZeroDivisionError if b is zero.\"\"\"
    if b == 0:
        raise ZeroDivisionError(\"Division by zero is undefined.\")
    return a / b

def power(a, b):
    \"\"\"Return a raised to the power of b.\"\"\"
    return a ** b
