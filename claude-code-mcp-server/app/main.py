#!/usr/bin/env python3
"""Main entry point for the expense tracker application."""

from src.cli import ExpenseCLI


def main() -> None:
    """Run the expense tracker application."""
    cli = ExpenseCLI()
    cli.run()


if __name__ == "__main__":
    main()