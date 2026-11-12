import argparse
import sys
from com import client, server

def echo_handler(data: bytes) -> bytes:
    """Echo handler – returns the received data unchanged."""
    return data

def run_server(args):
    try:
        server.start_server(host=args.host, port=args.port, handler=echo_handler)
    except KeyboardInterrupt:
        print('\nServer stopped by user.', file=sys.stderr)

def run_client(args):
    response = client.send_message(host=args.host, port=args.port, message=args.message)
    print('Response from server:', response)

def main():
    parser = argparse.ArgumentParser(description='Simple TCP echo client/server.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    server_parser = subparsers.add_parser('server', help='Start the echo server')
    server_parser.add_argument('--host', default='127.0.0.1', help='Host to bind')
    server_parser.add_argument('--port', type=int, default=65432, help='Port to bind')
    server_parser.set_defaults(func=run_server)

    client_parser = subparsers.add_parser('client', help='Send a message to the server')
    client_parser.add_argument('--host', default='127.0.0.1', help='Server host')
    client_parser.add_argument('--port', type=int, default=65432, help='Server port')
    client_parser.add_argument('message', help='Message to send')
    client_parser.set_defaults(func=run_client)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
