import socket
import sys

def send_message(host: str, port: int, message: str, timeout: float = 5.0) -> str:
    """Send a message to a TCP server and return the response.
    
    Args:
        host: Server hostname or IP address.
        port: Server port.
        message: The string message to send.
        timeout: Connection timeout in seconds.
    
    Returns:
        The server's response decoded as UTF‑8.
    """
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.sendall(message.encode('utf-8'))
        # Receive until the server closes the connection
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
    return response.decode('utf-8')
