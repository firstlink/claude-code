"""Expense class for tracking individual expenses."""

from datetime import datetime
from typing import Dict, Any


class Expense:
    """Represents a single expense with amount, category, and description."""

    def __init__(self, amount: float, category: str, description: str) -> None:
        """Initialize an expense with amount, category, and description.

        Args:
            amount: The expense amount
            category: The expense category
            description: The expense description
        """
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert expense to dictionary for serialisation.

        Returns:
            Dictionary representation of the expense
        """
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Create expense from dictionary.

        Args:
            data: Dictionary containing expense data

        Returns:
            Expense instance
        """
        expense = cls(data["amount"], data["category"], data["description"])
        expense.date = datetime.fromisoformat(data["date"])
        return expense

    def __str__(self) -> str:
        """String representation of the expense."""
        return f"{self.date.strftime('%Y-%m-%d')} | £{self.amount:.2f} | {self.category} | {self.description}"