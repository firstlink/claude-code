"""Test suite for Personal Finance Tracker CLI.

Tests the add and list commands, transaction validation,
and state management using pytest fixtures.
"""

from datetime import datetime
from typing import Any

import pytest
from click.testing import CliRunner

import finance_tracker
from finance_tracker import add, cli, list


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Click CLI test runner.

    Returns:
        CliRunner: Test runner for invoking CLI commands
    """
    return CliRunner()


@pytest.fixture(autouse=True)
def clear_transactions() -> None:
    """Clear transactions before each test.

    This fixture runs automatically before each test to ensure
    test isolation by clearing the module-level transactions list.
    """
    finance_tracker.transactions.clear()


class TestAddCommand:
    """Tests for the add command."""

    def test_add_transaction_with_description(self, runner: CliRunner) -> None:
        """Test adding a transaction with all fields including description."""
        result = runner.invoke(
            cli,
            [
                "add",
                "--amount",
                "50.00",
                "--category",
                "groceries",
                "--description",
                "Weekly shopping",
            ],
        )

        assert result.exit_code == 0
        assert "Transaction added: $50.00" in result.output
        assert "Category: groceries" in result.output
        assert "Description: Weekly shopping" in result.output
        assert len(finance_tracker.transactions) == 1

        transaction = finance_tracker.transactions[0]
        assert transaction["amount"] == 50.00
        assert transaction["category"] == "groceries"
        assert transaction["description"] == "Weekly shopping"
        assert "date" in transaction

    def test_add_transaction_without_description(self, runner: CliRunner) -> None:
        """Test adding a transaction without optional description."""
        result = runner.invoke(
            cli, ["add", "--amount", "125.50", "--category", "utilities"]
        )

        assert result.exit_code == 0
        assert "Transaction added: $125.50" in result.output
        assert "Category: utilities" in result.output
        assert "Description:" not in result.output
        assert len(finance_tracker.transactions) == 1

        transaction = finance_tracker.transactions[0]
        assert transaction["amount"] == 125.50
        assert transaction["category"] == "utilities"
        assert transaction["description"] == ""
        assert "date" in transaction

    def test_add_transaction_stores_iso_date(self, runner: CliRunner) -> None:
        """Test that transaction date is stored in ISO format."""
        before_time = datetime.now()

        result = runner.invoke(
            cli, ["add", "--amount", "25.00", "--category", "entertainment"]
        )

        after_time = datetime.now()

        assert result.exit_code == 0
        transaction = finance_tracker.transactions[0]

        # Parse the stored date and verify it's valid ISO format
        stored_date = datetime.fromisoformat(transaction["date"])
        assert before_time <= stored_date <= after_time

    def test_add_transaction_negative_amount(self, runner: CliRunner) -> None:
        """Test that negative amounts are rejected."""
        result = runner.invoke(
            cli, ["add", "--amount", "-50.00", "--category", "groceries"]
        )

        assert result.exit_code != 0
        assert "Transaction amount must be positive" in result.output
        assert len(finance_tracker.transactions) == 0

    def test_add_transaction_zero_amount(self, runner: CliRunner) -> None:
        """Test that zero amount is rejected."""
        result = runner.invoke(
            cli, ["add", "--amount", "0.00", "--category", "groceries"]
        )

        assert result.exit_code != 0
        assert "Transaction amount must be positive" in result.output
        assert len(finance_tracker.transactions) == 0

    def test_add_multiple_transactions(self, runner: CliRunner) -> None:
        """Test adding multiple transactions maintains state."""
        result1 = runner.invoke(
            cli, ["add", "--amount", "50.00", "--category", "groceries"]
        )
        result2 = runner.invoke(
            cli, ["add", "--amount", "100.00", "--category", "utilities"]
        )
        result3 = runner.invoke(
            cli, ["add", "--amount", "25.00", "--category", "entertainment"]
        )

        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert result3.exit_code == 0
        assert len(finance_tracker.transactions) == 3

        amounts = [t["amount"] for t in finance_tracker.transactions]
        assert amounts == [50.00, 100.00, 25.00]

    def test_add_missing_required_amount(self, runner: CliRunner) -> None:
        """Test that missing required amount parameter fails."""
        result = runner.invoke(cli, ["add", "--category", "groceries"])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()

    def test_add_missing_required_category(self, runner: CliRunner) -> None:
        """Test that missing required category parameter fails."""
        result = runner.invoke(cli, ["add", "--amount", "50.00"])

        assert result.exit_code != 0
        assert "Missing option" in result.output or "required" in result.output.lower()


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty_transactions(self, runner: CliRunner) -> None:
        """Test listing when no transactions exist."""
        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "No transactions found" in result.output

    def test_list_single_transaction(self, runner: CliRunner) -> None:
        """Test listing a single transaction."""
        runner.invoke(
            cli,
            [
                "add",
                "--amount",
                "50.00",
                "--category",
                "groceries",
                "--description",
                "Weekly shopping",
            ],
        )

        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Total transactions: 1" in result.output
        assert "$50.00" in result.output
        assert "groceries" in result.output
        assert "Weekly shopping" in result.output

    def test_list_multiple_transactions(self, runner: CliRunner) -> None:
        """Test listing multiple transactions."""
        runner.invoke(cli, ["add", "--amount", "50.00", "--category", "groceries"])
        runner.invoke(cli, ["add", "--amount", "100.00", "--category", "utilities"])
        runner.invoke(
            cli, ["add", "--amount", "25.00", "--category", "entertainment"]
        )

        result = runner.invoke(cli, ["list"])

        assert result.exit_code == 0
        assert "Total transactions: 3" in result.output
        assert "$50.00" in result.output
        assert "groceries" in result.output
        assert "$100.00" in result.output
        assert "utilities" in result.output
        assert "$25.00" in result.output
        assert "entertainment" in result.output


class TestTransactionStateManagement:
    """Tests for transaction state management and isolation."""

    def test_transactions_cleared_between_tests(self, runner: CliRunner) -> None:
        """Test that transactions are cleared between tests by fixture."""
        # This test verifies the autouse fixture is working
        assert len(finance_tracker.transactions) == 0

        runner.invoke(cli, ["add", "--amount", "50.00", "--category", "groceries"])
        assert len(finance_tracker.transactions) == 1

    def test_transaction_data_structure(self, runner: CliRunner) -> None:
        """Test that transaction dictionary has correct structure."""
        runner.invoke(
            cli,
            [
                "add",
                "--amount",
                "75.50",
                "--category",
                "utilities",
                "--description",
                "Electric bill",
            ],
        )

        transaction = finance_tracker.transactions[0]

        # Verify all required keys exist
        assert "amount" in transaction
        assert "category" in transaction
        assert "description" in transaction
        assert "date" in transaction

        # Verify types
        assert isinstance(transaction["amount"], float)
        assert isinstance(transaction["category"], str)
        assert isinstance(transaction["description"], str)
        assert isinstance(transaction["date"], str)
