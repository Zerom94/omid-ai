def fibonacci(n: int) -> list[int]:
    \"\"\"Return a list of the Fibonacci sequence up to n elements.
    
    Args:
        n (int): Number of elements to generate. Must be non‑negative.
    
    Returns:
        list[int]: Fibonacci numbers.
    \"\"\"
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq
