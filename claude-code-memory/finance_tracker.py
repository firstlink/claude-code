"""Personal Finance Tracker CLI Application.

A command-line tool for tracking personal financial transactions with categories,
amounts, and descriptions.
"""

from datetime import datetime
from typing import Any

import click


# Module-level transaction storage
transactions: list[dict[str, Any]] = []


# Application version
__version__ = "1.0.0"


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Personal Finance Tracker CLI.

    Track your personal finances with categorized transactions.
    """
    pass


@cli.command()
@click.option(
    "--amount",
    type=float,
    required=True,
    help="The transaction amount (must be positive)",
)
@click.option(
    "--category",
    type=str,
    required=True,
    help="The transaction category (e.g., groceries, utilities)",
)
@click.option(
    "--description",
    type=str,
    default="",
    help="Optional description of the transaction",
)
def add(amount: float, category: str, description: str) -> None:
    """Add a new financial transaction.

    Creates a transaction with amount, category, optional description,
    and automatically captures the current date/time.

    Args:
        amount: The transaction amount (must be positive)
        category: The transaction category
        description: Optional description (defaults to empty string)

    Raises:
        click.BadParameter: If amount is not positive
    """
    # Validate amount is positive
    if amount <= 0:
        raise click.BadParameter(
            f"Transaction amount must be positive, got {amount}",
            param_hint="--amount",
        )

    # Create transaction dictionary
    transaction: dict[str, Any] = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().isoformat(),
    }

    # Add to storage
    transactions.append(transaction)

    # Display confirmation to user
    print(f"Transaction added: ${amount:.2f}")
    print(f"Category: {category}")
    if description:
        print(f"Description: {description}")
    print(f"Date: {transaction['date']}")


@cli.command()
def list() -> None:
    """List all transactions.

    TODO: Implementation pending

    Currently displays basic transaction information.
    Full implementation with formatting and filtering to be added.
    """
    if not transactions:
        print("No transactions found.")
        return

    print(f"Total transactions: {len(transactions)}")
    print("\nTransactions:")
    for idx, transaction in enumerate(transactions, 1):
        print(f"\n{idx}. ${transaction['amount']:.2f} - {transaction['category']}")
        if transaction["description"]:
            print(f"   Description: {transaction['description']}")
        print(f"   Date: {transaction['date']}")


if __name__ == "__main__":
    cli()
