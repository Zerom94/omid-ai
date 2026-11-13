class Communicator:
    """A simple communicator that simulates sending and receiving messages."""

    def __init__(self):
        self._inbox = []

    def send_message(self, message: str) -> None:
        """Simulate sending a message by storing it in the inbox."""
        print(f"Sending message: {message}")
        self._inbox.append(message)

    def receive_message(self) -> str:
        """Simulate receiving the most recent message."""
        if not self._inbox:
            return "No messages."
        # Return the last message and clear inbox
        message = self._inbox.pop()
        return f"Echo: {message}"
