# Fibonacci Project

This small multi‑file Python project demonstrates how to generate Fibonacci numbers.

## Files

- **utils.py** – Contains reusable functions:
  - `fibonacci(limit)` returns all Fibonacci numbers less than or equal to `limit`.
  - `fibonacci_iterative(count)` returns the first `count` Fibonacci numbers.
- **main.py** – Provides a command‑line interface to the utilities.
- **README.md** – You are reading it!

## Usage

```bash
# Install (no external dependencies required)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # (empty for this project)
```

```bash
# Generate Fibonacci numbers up to a maximum value
python main.py --max 100

# Generate a specific count of Fibonacci numbers
python main.py --count 10
```

Both commands will print a Python list with the resulting sequence.

## License

This code is released into the public domain (CC0).