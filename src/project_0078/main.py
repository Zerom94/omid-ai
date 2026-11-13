#!/usr/bin/env python3

from com.communicator import Communicator
from com.utils import format_message

def main():
    comm = Communicator()
    msg = "Hello, World!"
    formatted = format_message(msg)
    comm.send_message(formatted)
    response = comm.receive_message()
    print(f"Received response: {response}")

if __name__ == "__main__":
    main()
