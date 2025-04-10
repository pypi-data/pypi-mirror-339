"""
Command-line interface for mcp-panther.
"""
from . import greet

def main() -> None:
    """Entry point for the command-line interface."""
    print(greet("from CLI"))

if __name__ == "__main__":
    main() 