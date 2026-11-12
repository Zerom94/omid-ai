# com

A tiny Python utility package that provides a simple command‑line interface for common mathematical operations.

## Features

- **Factorial** – Compute `n!` for any non‑negative integer.
- **Fibonacci** – Get the *n*‑th Fibonacci number (0‑indexed).
- **Prime test** – Determine whether a number is prime.

## Installation

```bash
# Clone the repository
git clone https://example.com/your-repo/com.git
cd com

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install the package in editable mode
pip install -e .
```

## Usage

You can run the tool either via the top‑level ``main.py`` script or directly as a module:

```bash
# Using the provided wrapper script
python main.py factorial 5
# => 120

python main.py fibonacci 10
# => 55

python main.py isprime 17
# => 17 is a prime number.
```

Or, if you have installed the package, the ``com`` command becomes available:

```bash
com factorial 6
com fibonacci 7
com isprime 18
```

## Development

The project follows a minimal layout:

```
com/
    __init__.py
    cli.py
    math_utils.py
main.py
README.md
```

All functionality lives in ``com.math_utils`` and is exercised through the CLI in ``com.cli``.

Feel free to extend the package with additional utilities or integrate it into larger projects.
