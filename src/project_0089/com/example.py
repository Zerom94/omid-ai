class Greeter:
    """Simple greeter class."""

    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f'Hello, {self.name}!'
