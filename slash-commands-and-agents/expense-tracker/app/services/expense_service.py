"""Expense service for business logic operations."""

import sys
import os
from typing import List, Optional, Dict
from datetime import datetime

# Add parent directory to path to import expense_tracker module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from expense_tracker import ExpenseTracker, JsonFileStorage, Expense

from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    PaginatedExpenseResponse,
    PaginationMeta,
    PaginationLinks,
    CategoryBreakdown,
    SpendingSummaryResponse,
    CategoryInfo,
    CategoriesResponse
)
from app.middleware.error_handler import APIError
from fastapi import status


class ExpenseService:
    """Service class for expense-related business logic."""

    def __init__(self, data_file: str = "expenses.json"):
        """
        Initialise the expense service.

        Args:
            data_file: Path to the JSON file for storing expenses
        """
        storage = JsonFileStorage(data_file)
        self.tracker = ExpenseTracker(storage)

    def create_expense(self, expense_data: ExpenseCreate) -> ExpenseResponse:
        """
        Create a new expense.

        Args:
            expense_data: Expense creation data

        Returns:
            Created expense response

        Raises:
            APIError: If expense creation fails
        """
        success = self.tracker.add_expense(
            amount=expense_data.amount,
            category=expense_data.category,
            description=expense_data.description
        )

        if not success:
            raise APIError(
                code="VALIDATION_ERROR",
                message="Failed to create expense",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Get the most recently added expense
        expenses = self.tracker.get_all_expenses()
        if not expenses:
            raise APIError(
                code="INTERNAL_ERROR",
                message="Failed to retrieve created expense",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        latest_expense = expenses[-1]
        return ExpenseResponse(
            id=latest_expense.expense_id,
            amount=latest_expense.amount,
            category=latest_expense.category,
            description=latest_expense.description,
            date=latest_expense.date
        )

    def list_expenses(
        self,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        sort_by: str = "date",
        order: str = "desc"
    ) -> PaginatedExpenseResponse:
        """
        List expenses with filtering, sorting, and pagination.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            category: Optional category filter
            min_amount: Optional minimum amount filter
            max_amount: Optional maximum amount filter
            sort_by: Field to sort by (date, amount, category)
            order: Sort order (asc, desc)

        Returns:
            Paginated expense response
        """
        expenses = self.tracker.get_all_expenses()

        # Apply filters
        if category:
            expenses = [e for e in expenses if e.category.lower() == category.lower()]

        if min_amount is not None:
            expenses = [e for e in expenses if e.amount >= min_amount]

        if max_amount is not None:
            expenses = [e for e in expenses if e.amount <= max_amount]

        # Apply sorting
        reverse = (order == "desc")
        if sort_by == "amount":
            expenses = sorted(expenses, key=lambda e: e.amount, reverse=reverse)
        elif sort_by == "category":
            expenses = sorted(expenses, key=lambda e: e.category, reverse=reverse)
        else:  # date
            expenses = sorted(expenses, key=lambda e: e.date, reverse=reverse)

        # Calculate pagination
        total_items = len(expenses)
        total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1

        # Validate page number
        if page > total_pages and total_items > 0:
            page = total_pages

        start = (page - 1) * limit
        end = start + limit
        paginated_expenses = expenses[start:end]

        # Convert to response models
        expense_responses = [
            ExpenseResponse(
                id=e.expense_id,
                amount=e.amount,
                category=e.category,
                description=e.description,
                date=e.date
            )
            for e in paginated_expenses
        ]

        # Build pagination links
        base_url = f"/api/v1/expenses?page={{page}}&limit={limit}"
        if category:
            base_url += f"&category={category}"
        if min_amount is not None:
            base_url += f"&min_amount={min_amount}"
        if max_amount is not None:
            base_url += f"&max_amount={max_amount}"
        base_url += f"&sort_by={sort_by}&order={order}"

        return PaginatedExpenseResponse(
            data=expense_responses,
            pagination=PaginationMeta(
                page=page,
                limit=limit,
                total_items=total_items,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            ),
            links=PaginationLinks(
                self=base_url.format(page=page),
                next=base_url.format(page=page + 1) if page < total_pages else None,
                previous=base_url.format(page=page - 1) if page > 1 else None,
                first=base_url.format(page=1),
                last=base_url.format(page=total_pages)
            )
        )

    def get_expense(self, expense_id: str) -> Optional[ExpenseResponse]:
        """
        Get a single expense by ID.

        Args:
            expense_id: Expense ID

        Returns:
            Expense response or None if not found
        """
        expenses = self.tracker.get_all_expenses()
        for expense in expenses:
            if expense.expense_id == expense_id:
                return ExpenseResponse(
                    id=expense.expense_id,
                    amount=expense.amount,
                    category=expense.category,
                    description=expense.description,
                    date=expense.date
                )
        return None

    def update_expense(self, expense_id: str, expense_data: ExpenseCreate) -> Optional[ExpenseResponse]:
        """
        Update an expense (full update).

        Args:
            expense_id: Expense ID
            expense_data: New expense data

        Returns:
            Updated expense response or None if not found
        """
        expenses = self.tracker.expenses
        for i, expense in enumerate(expenses):
            if expense.expense_id == expense_id:
                # Create updated expense with same ID
                updated_expense = Expense(
                    expense_id=expense_id,
                    amount=expense_data.amount,
                    category=expense_data.category,
                    description=expense_data.description,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                expenses[i] = updated_expense
                self.tracker.save_data()

                return ExpenseResponse(
                    id=updated_expense.expense_id,
                    amount=updated_expense.amount,
                    category=updated_expense.category,
                    description=updated_expense.description,
                    date=updated_expense.date
                )
        return None

    def partial_update_expense(
        self, expense_id: str, expense_data: ExpenseUpdate
    ) -> Optional[ExpenseResponse]:
        """
        Partially update an expense.

        Args:
            expense_id: Expense ID
            expense_data: Partial expense data

        Returns:
            Updated expense response or None if not found
        """
        expenses = self.tracker.expenses
        for i, expense in enumerate(expenses):
            if expense.expense_id == expense_id:
                # Update only provided fields
                updated_expense = Expense(
                    expense_id=expense_id,
                    amount=expense_data.amount if expense_data.amount is not None else expense.amount,
                    category=expense_data.category if expense_data.category is not None else expense.category,
                    description=expense_data.description if expense_data.description is not None else expense.description,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                expenses[i] = updated_expense
                self.tracker.save_data()

                return ExpenseResponse(
                    id=updated_expense.expense_id,
                    amount=updated_expense.amount,
                    category=updated_expense.category,
                    description=updated_expense.description,
                    date=updated_expense.date
                )
        return None

    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense.

        Args:
            expense_id: Expense ID

        Returns:
            True if deleted, False if not found
        """
        expenses = self.tracker.expenses
        for i, expense in enumerate(expenses):
            if expense.expense_id == expense_id:
                expenses.pop(i)
                self.tracker.save_data()
                return True
        return False

    def get_spending_summary(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> SpendingSummaryResponse:
        """
        Get spending summary with category breakdown.

        Args:
            start_date: Optional start date filter (ISO format)
            end_date: Optional end date filter (ISO format)

        Returns:
            Spending summary response
        """
        expenses = self.tracker.get_all_expenses()

        # Apply date filters if provided
        # For now, we'll skip date filtering as the existing code doesn't support it
        # This can be enhanced in the future

        total_spending = self.tracker.calculate_total_spending()
        category_totals = self.tracker.get_spending_by_category()

        # Build category breakdown
        by_category: Dict[str, CategoryBreakdown] = {}
        for category, amount in category_totals.items():
            category_expenses = self.tracker.filter_by_category(category)
            count = len(category_expenses)
            percentage = (amount / total_spending * 100) if total_spending > 0 else 0
            average = amount / count if count > 0 else 0

            by_category[category] = CategoryBreakdown(
                total=amount,
                count=count,
                percentage=round(percentage, 2),
                average=round(average, 2)
            )

        period = None
        if start_date or end_date:
            period = {}
            if start_date:
                period["start_date"] = start_date
            if end_date:
                period["end_date"] = end_date

        return SpendingSummaryResponse(
            total_spending=round(total_spending, 2),
            total_expenses=len(expenses),
            average_expense=round(total_spending / len(expenses), 2) if expenses else 0,
            period=period,
            by_category=by_category
        )

    def get_categories(self) -> CategoriesResponse:
        """
        Get list of all categories with statistics.

        Returns:
            Categories response
        """
        categories = self.tracker.get_available_categories()
        category_totals = self.tracker.get_spending_by_category()

        category_list = []
        for category in categories:
            expenses = self.tracker.filter_by_category(category)
            category_list.append(
                CategoryInfo(
                    name=category,
                    expense_count=len(expenses),
                    total_amount=round(category_totals.get(category, 0), 2)
                )
            )

        return CategoriesResponse(
            categories=category_list,
            total_categories=len(category_list)
        )
