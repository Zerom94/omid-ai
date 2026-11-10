#!/usr/bin/env python3
"""OMID AI CLI Entry Point"""
import sys

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    rest = sys.argv[2:]
    from cli import run_command
    return run_command(cmd, rest)

if __name__ == "__main__":
    sys.exit(main())
