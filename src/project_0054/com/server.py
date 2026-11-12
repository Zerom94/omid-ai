import socket
import threading
from typing import Callable

def _handle_client(conn: socket.socket, addr, handler: Callable[[bytes], bytes]):
    """Handle a single client connection.
    
    Reads all data from ``conn``, passes it to ``handler`` and sends the
    handler's return value back to the client.
    """
    with conn:
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        response = handler(data)
        conn.sendall(response)

def start_server(host: str = '127.0.0.1', port: int = 65432,
                 handler: Callable[[bytes], bytes] = lambda d: d):
    """Start a TCP server.
    
    The server runs forever (or until interrupted) and processes each
    incoming connection in its own daemon thread using ``handler``.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=_handle_client,
                             args=(conn, addr, handler),
                             daemon=True).start()
