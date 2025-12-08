"""JSON-based storage service for transactions."""

import json
import logging
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class TransactionStorage:
    """
    JSON-based storage service for financial transactions.

    Stores transactions in a local JSON file within the project directory.
    """

    def __init__(self, data_file: str = "transactions.json"):
        """
        Initialize storage service.

        Args:
            data_file: Name of JSON file to store transactions
        """
        # Store in project root directory
        project_root = Path(__file__).parent.parent.parent.parent
        self.data_file_path = project_root / data_file
        self._ensure_data_file()
        self._next_id = self._get_next_id()

    def _ensure_data_file(self) -> None:
        """Ensure the data file exists."""
        if not self.data_file_path.exists():
            self.data_file_path.write_text(json.dumps([], indent=2))
            logger.info(f"Created new data file: {self.data_file_path}")

    def _get_next_id(self) -> int:
        """Get the next available transaction ID."""
        transactions = self._load_transactions()
        if not transactions:
            return 1
        return max(txn['id'] for txn in transactions) + 1

    def _load_transactions(self) -> list[dict[str, Any]]:
        """Load transactions from JSON file."""
        try:
            with open(self.data_file_path, 'r') as file:
                data = json.load(file)
                # Convert amount strings back to Decimal for processing
                for transaction in data:
                    transaction['amount'] = Decimal(str(transaction['amount']))
                return data
        except (json.JSONDecodeError, FileNotFoundError) as error:
            logger.error(f"Error loading transactions: {error}")
            return []

    def _save_transactions(self, transactions: list[dict[str, Any]]) -> None:
        """Save transactions to JSON file."""
        # Convert Decimal to float for JSON serialization
        serializable_data = []
        for transaction in transactions:
            txn_copy = transaction.copy()
            txn_copy['amount'] = float(txn_copy['amount'])
            serializable_data.append(txn_copy)

        with open(self.data_file_path, 'w') as file:
            json.dump(serializable_data, file, indent=2, default=str)
        logger.debug(f"Saved {len(transactions)} transactions to {self.data_file_path}")

    async def create_transaction(
        self,
        amount: Decimal,
        category: str,
        description: str = "",
    ) -> dict[str, Any]:
        """
        Create a new transaction.

        Args:
            amount: Transaction amount
            category: Transaction category
            description: Optional transaction description

        Returns:
            Created transaction with ID and timestamp

        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError(f"Transaction amount must be positive, got {amount}")

        transaction_data = {
            'id': self._next_id,
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now().isoformat(),
        }

        transactions = self._load_transactions()
        transactions.append(transaction_data)
        self._save_transactions(transactions)

        self._next_id += 1

        logger.info(
            "Transaction created in storage",
            extra={
                'transaction_id': transaction_data['id'],
                'amount': float(amount),
                'category': category,
            }
        )

        return transaction_data

    async def list_transactions(
        self,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        List transactions with optional filtering.

        Args:
            category: Optional category filter
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of transactions
        """
        transactions = self._load_transactions()

        # Filter by category if provided
        if category:
            transactions = [
                txn for txn in transactions
                if txn['category'].lower() == category.lower()
            ]

        # Sort by date (newest first)
        transactions.sort(key=lambda txn: txn['date'], reverse=True)

        # Apply pagination
        return transactions[offset:offset + limit]

    async def count_transactions(self, category: Optional[str] = None) -> int:
        """
        Count total transactions.

        Args:
            category: Optional category filter

        Returns:
            Total count of transactions
        """
        transactions = self._load_transactions()

        if category:
            transactions = [
                txn for txn in transactions
                if txn['category'].lower() == category.lower()
            ]

        return len(transactions)

    async def get_transaction(self, transaction_id: int) -> Optional[dict[str, Any]]:
        """
        Get a specific transaction by ID.

        Args:
            transaction_id: Transaction ID to retrieve

        Returns:
            Transaction data or None if not found
        """
        transactions = self._load_transactions()

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return transaction

        return None

    async def update_transaction(
        self,
        transaction_id: int,
        amount: Optional[Decimal] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Update an existing transaction.

        Args:
            transaction_id: Transaction ID to update
            amount: New amount (optional)
            category: New category (optional)
            description: New description (optional)

        Returns:
            Updated transaction

        Raises:
            ValueError: If transaction not found or amount is invalid
        """
        transactions = self._load_transactions()

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                # Update fields if provided
                if amount is not None:
                    if amount <= 0:
                        raise ValueError(f"Transaction amount must be positive, got {amount}")
                    transaction['amount'] = amount

                if category is not None:
                    transaction['category'] = category

                if description is not None:
                    transaction['description'] = description

                self._save_transactions(transactions)
                logger.info(f"Transaction updated in storage: {transaction_id}")
                return transaction

        raise ValueError(f"Transaction {transaction_id} not found")

    async def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete a transaction.

        Args:
            transaction_id: Transaction ID to delete

        Returns:
            True if deleted, False if not found
        """
        transactions = self._load_transactions()
        initial_count = len(transactions)

        transactions = [
            txn for txn in transactions
            if txn['id'] != transaction_id
        ]

        if len(transactions) < initial_count:
            self._save_transactions(transactions)
            logger.info(f"Transaction deleted from storage: {transaction_id}")
            return True

        return False
