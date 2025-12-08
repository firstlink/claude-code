"""
Unit tests for the expense tracker application.

This module provides comprehensive test coverage for all major components
of the expense tracking system.
"""

import json
import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from expense_tracker import (
    Expense,
    ExpenseTracker,
    InputValidator,
    JsonFileStorage,
    TableFormatter,
    ExpenseTrackerUI,
)


class TestExpense(unittest.TestCase):
    """Test cases for the Expense dataclass."""

    def test_create_new_expense(self):
        """Test creating a new expense with generated ID and timestamp."""
        expense = Expense.create_new(25.50, "Food", "Lunch at cafe")

        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch at cafe")
        self.assertIsNotNone(expense.expense_id)
        self.assertIsNotNone(expense.date)

    def test_to_dict(self):
        """Test converting expense to dictionary."""
        expense = Expense(
            expense_id="test-123",
            amount=50.0,
            category="Transport",
            description="Bus pass",
            date="2024-10-09 12:00:00"
        )

        expense_dict = expense.to_dict()

        self.assertEqual(expense_dict["id"], "test-123")
        self.assertEqual(expense_dict["amount"], 50.0)
        self.assertEqual(expense_dict["category"], "Transport")
        self.assertEqual(expense_dict["description"], "Bus pass")
        self.assertEqual(expense_dict["date"], "2024-10-09 12:00:00")

    def test_from_dict(self):
        """Test creating expense from dictionary."""
        data = {
            "id": "test-456",
            "amount": 30.0,
            "category": "Entertainment",
            "description": "Cinema ticket",
            "date": "2024-10-09 18:30:00"
        }

        expense = Expense.from_dict(data)

        self.assertEqual(expense.expense_id, "test-456")
        self.assertEqual(expense.amount, 30.0)
        self.assertEqual(expense.category, "Entertainment")
        self.assertEqual(expense.description, "Cinema ticket")
        self.assertEqual(expense.date, "2024-10-09 18:30:00")


class TestInputValidator(unittest.TestCase):
    """Test cases for the InputValidator class."""

    def test_validate_amount_positive(self):
        """Test validation of positive amounts."""
        self.assertTrue(InputValidator.validate_amount(1.0))
        self.assertTrue(InputValidator.validate_amount(100.50))
        self.assertTrue(InputValidator.validate_amount(0.01))

    def test_validate_amount_negative_or_zero(self):
        """Test validation fails for negative or zero amounts."""
        self.assertFalse(InputValidator.validate_amount(0))
        self.assertFalse(InputValidator.validate_amount(-1.0))
        self.assertFalse(InputValidator.validate_amount(-100.50))

    def test_validate_text_field_valid(self):
        """Test validation of valid text fields."""
        self.assertTrue(InputValidator.validate_text_field("Food"))
        self.assertTrue(InputValidator.validate_text_field("Lunch at cafe"))
        self.assertTrue(InputValidator.validate_text_field("  Text with spaces  "))

    def test_validate_text_field_invalid(self):
        """Test validation fails for empty or too long text."""
        self.assertFalse(InputValidator.validate_text_field(""))
        self.assertFalse(InputValidator.validate_text_field("   "))
        self.assertFalse(InputValidator.validate_text_field("x" * 101))

    def test_validate_choice(self):
        """Test validation of menu choices."""
        self.assertTrue(InputValidator.validate_choice(1, 1, 5))
        self.assertTrue(InputValidator.validate_choice(3, 1, 5))
        self.assertTrue(InputValidator.validate_choice(5, 1, 5))
        self.assertFalse(InputValidator.validate_choice(0, 1, 5))
        self.assertFalse(InputValidator.validate_choice(6, 1, 5))


class TestJsonFileStorage(unittest.TestCase):
    """Test cases for the JsonFileStorage class."""

    def setUp(self):
        """Create a temporary file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = JsonFileStorage(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_save_and_load_expenses(self):
        """Test saving and loading expenses."""
        expenses = [
            Expense.create_new(25.50, "Food", "Lunch"),
            Expense.create_new(60.0, "Transport", "Bus pass")
        ]

        self.storage.save_expenses(expenses)
        loaded_expenses = self.storage.load_expenses()

        self.assertEqual(len(loaded_expenses), 2)
        self.assertEqual(loaded_expenses[0].amount, 25.50)
        self.assertEqual(loaded_expenses[1].category, "Transport")

    def test_load_nonexistent_file(self):
        """Test loading from a nonexistent file returns empty list."""
        storage = JsonFileStorage("nonexistent_file.json")
        expenses = storage.load_expenses()

        self.assertEqual(expenses, [])

    def test_load_invalid_json(self):
        """Test loading invalid JSON returns empty list."""
        with open(self.temp_file.name, "w") as f:
            f.write("invalid json content")

        expenses = self.storage.load_expenses()

        self.assertEqual(expenses, [])


class TestExpenseTracker(unittest.TestCase):
    """Test cases for the ExpenseTracker class."""

    def setUp(self):
        """Create a tracker with temporary storage."""
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = JsonFileStorage(self.temp_file.name)
        self.tracker = ExpenseTracker(self.storage)

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_expense_valid(self):
        """Test adding a valid expense."""
        result = self.tracker.add_expense(25.50, "Food", "Lunch")

        self.assertTrue(result)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0].amount, 25.50)

    def test_add_expense_invalid_amount(self):
        """Test adding expense with invalid amount fails."""
        result = self.tracker.add_expense(-10.0, "Food", "Lunch")

        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_add_expense_invalid_category(self):
        """Test adding expense with invalid category fails."""
        result = self.tracker.add_expense(25.50, "", "Lunch")

        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_add_expense_invalid_description(self):
        """Test adding expense with invalid description fails."""
        result = self.tracker.add_expense(25.50, "Food", "")

        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_get_all_expenses(self):
        """Test getting all expenses returns a copy."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")

        expenses = self.tracker.get_all_expenses()

        self.assertEqual(len(expenses), 2)
        # Verify it's a copy
        expenses.clear()
        self.assertEqual(len(self.tracker.expenses), 2)

    def test_calculate_total_spending(self):
        """Test calculating total spending."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")
        self.tracker.add_expense(15.25, "Food", "Snack")

        total = self.tracker.calculate_total_spending()

        self.assertEqual(total, 100.75)

    def test_calculate_total_spending_empty(self):
        """Test calculating total with no expenses."""
        total = self.tracker.calculate_total_spending()

        self.assertEqual(total, 0)

    def test_get_spending_by_category(self):
        """Test getting spending breakdown by category."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")
        self.tracker.add_expense(15.25, "Food", "Snack")

        category_totals = self.tracker.get_spending_by_category()

        self.assertEqual(category_totals["Food"], 40.75)
        self.assertEqual(category_totals["Transport"], 60.0)

    def test_filter_by_category(self):
        """Test filtering expenses by category."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")
        self.tracker.add_expense(15.25, "Food", "Snack")

        food_expenses = self.tracker.filter_by_category("Food")

        self.assertEqual(len(food_expenses), 2)
        self.assertTrue(all(e.category == "Food" for e in food_expenses))

    def test_filter_by_category_case_insensitive(self):
        """Test filtering is case-insensitive."""
        self.tracker.add_expense(25.50, "Food", "Lunch")

        food_expenses = self.tracker.filter_by_category("food")

        self.assertEqual(len(food_expenses), 1)

    def test_get_available_categories(self):
        """Test getting list of unique categories."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")
        self.tracker.add_expense(15.25, "Food", "Snack")

        categories = self.tracker.get_available_categories()

        self.assertEqual(len(categories), 2)
        self.assertIn("Food", categories)
        self.assertIn("Transport", categories)

    def test_save_and_load_data(self):
        """Test data persistence."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")

        # Create new tracker with same storage
        new_tracker = ExpenseTracker(self.storage)

        self.assertEqual(len(new_tracker.expenses), 2)
        self.assertEqual(new_tracker.expenses[0].amount, 25.50)


class TestTableFormatter(unittest.TestCase):
    """Test cases for the TableFormatter class."""

    @patch("builtins.print")
    def test_print_separator(self, mock_print):
        """Test printing separator line."""
        TableFormatter.print_separator(50, "=")

        mock_print.assert_called_once_with("=" * 50)

    @patch("builtins.print")
    def test_print_expenses_table_empty(self, mock_print):
        """Test printing empty expenses table."""
        TableFormatter.print_expenses_table([])

        mock_print.assert_called_once_with("No expenses recorded.")

    @patch("builtins.print")
    def test_print_expenses_table_with_data(self, mock_print):
        """Test printing expenses table with data."""
        expenses = [
            Expense(
                expense_id="test-123",
                amount=25.50,
                category="Food",
                description="Lunch",
                date="2024-10-09 12:00:00"
            )
        ]

        TableFormatter.print_expenses_table(expenses)

        # Verify print was called multiple times (header, separator, data)
        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.print")
    def test_print_category_breakdown(self, mock_print):
        """Test printing category breakdown."""
        category_totals = {
            "Food": 40.75,
            "Transport": 60.0
        }

        TableFormatter.print_category_breakdown(category_totals)

        # Verify print was called multiple times
        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.print")
    def test_print_category_expenses_empty(self, mock_print):
        """Test printing empty category expenses."""
        TableFormatter.print_category_expenses([], "Food")

        mock_print.assert_called_once_with("No expenses found for category: Food")


class TestExpenseTrackerUI(unittest.TestCase):
    """Test cases for the ExpenseTrackerUI class."""

    def setUp(self):
        """Create UI with mock tracker."""
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = JsonFileStorage(self.temp_file.name)
        self.tracker = ExpenseTracker(self.storage)
        self.ui = ExpenseTrackerUI(self.tracker)

    def tearDown(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    @patch("builtins.print")
    def test_display_menu(self, mock_print):
        """Test displaying the menu."""
        self.ui.display_menu()

        # Verify menu options were printed
        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.input", side_effect=["25.50", "Food", "Lunch"])
    @patch("builtins.print")
    def test_handle_add_expense_valid(self, mock_print, mock_input):
        """Test handling valid expense addition."""
        self.ui.handle_add_expense()

        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0].amount, 25.50)

    @patch("builtins.input", side_effect=["-10.50", "Food", "Lunch"])
    @patch("builtins.print")
    def test_handle_add_expense_negative_amount(self, mock_print, mock_input):
        """Test handling negative amount."""
        self.ui.handle_add_expense()

        self.assertEqual(len(self.tracker.expenses), 0)

    @patch("builtins.input", return_value="invalid")
    @patch("builtins.print")
    def test_handle_add_expense_invalid_input(self, mock_print, mock_input):
        """Test handling invalid amount input."""
        self.ui.handle_add_expense()

        self.assertEqual(len(self.tracker.expenses), 0)

    @patch("builtins.print")
    def test_handle_view_all_expenses(self, mock_print):
        """Test viewing all expenses."""
        self.tracker.add_expense(25.50, "Food", "Lunch")

        self.ui.handle_view_all_expenses()

        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.print")
    def test_handle_calculate_total(self, mock_print):
        """Test calculating total."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")

        self.ui.handle_calculate_total()

        # Verify total was printed
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("85.50" in call for call in calls))

    @patch("builtins.print")
    def test_handle_view_by_category(self, mock_print):
        """Test viewing by category."""
        self.tracker.add_expense(25.50, "Food", "Lunch")

        self.ui.handle_view_by_category()

        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_handle_filter_by_category(self, mock_print, mock_input):
        """Test filtering by category."""
        self.tracker.add_expense(25.50, "Food", "Lunch")
        self.tracker.add_expense(60.0, "Transport", "Bus pass")

        self.ui.handle_filter_by_category()

        self.assertGreater(mock_print.call_count, 1)

    @patch("builtins.print")
    def test_handle_filter_by_category_no_categories(self, mock_print):
        """Test filtering when no categories exist."""
        self.ui.handle_filter_by_category()

        # Verify message about no categories
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("No categories" in call for call in calls))


if __name__ == "__main__":
    unittest.main()
