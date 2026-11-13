class Greeter:
    """Simple greeter class used in the demo.

    Attributes:
        name (str): The name to greet.
    """

    def __init__(self, name: str = "User"):
        self.name = name

    def greet(self) -> None:
        """Print a greeting message to the console."""
        print(f"Hello, {self.name}!")
