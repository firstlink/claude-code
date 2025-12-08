"""Expense-related API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    PaginatedExpenseResponse,
    SpendingSummaryResponse,
    CategoriesResponse
)
from app.services.expense_service import ExpenseService
from app.middleware.error_handler import APIError
from app.utils.auth import get_current_user


router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_expense_service() -> ExpenseService:
    """Dependency to get expense service instance."""
    return ExpenseService()


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Create a new expense entry with amount, category, and description"
)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Create a new expense with the following information:

    - **amount**: Positive number representing expense amount in GBP (max 2 decimal places)
    - **category**: Category name (1-100 characters)
    - **description**: Expense description (1-500 characters)

    Returns the created expense with generated ID and timestamp.
    """
    return service.create_expense(expense_data)


@router.get(
    "",
    response_model=PaginatedExpenseResponse,
    summary="List all expenses",
    description="List expenses with filtering, sorting, and pagination support"
)
async def list_expenses(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    category: Optional[str] = Query(None, description="Filter by category (case-insensitive)"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum expense amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum expense amount"),
    sort_by: str = Query("date", regex="^(date|amount|category)$", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> PaginatedExpenseResponse:
    """
    List expenses with comprehensive filtering and pagination:

    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    - **category**: Filter by specific category
    - **min_amount**: Filter expenses >= this amount
    - **max_amount**: Filter expenses <= this amount
    - **sort_by**: Sort by date, amount, or category (default: date)
    - **order**: Sort order - asc or desc (default: desc)

    Returns paginated results with metadata and navigation links.
    """
    return service.list_expenses(
        page=page,
        limit=limit,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        sort_by=sort_by,
        order=order
    )


@router.get(
    "/summary",
    response_model=SpendingSummaryResponse,
    summary="Get spending summary",
    description="Get comprehensive spending statistics with category breakdown"
)
async def get_spending_summary(
    start_date: Optional[str] = Query(None, description="Start date (ISO 8601 format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO 8601 format)"),
    # current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> SpendingSummaryResponse:
    """
    Get spending summary and analytics:

    - Total spending across all expenses
    - Total number of expenses
    - Average expense amount
    - Breakdown by category with percentages
    - Optional date range filtering

    Returns comprehensive spending statistics.
    """
    return service.get_spending_summary(start_date=start_date, end_date=end_date)


@router.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="Get all categories",
    description="Get list of all expense categories with statistics"
)
async def get_categories(
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> CategoriesResponse:
    """
    Get list of all expense categories:

    - Category names
    - Number of expenses per category
    - Total amount spent per category

    Returns list of categories with statistics.
    """
    return service.get_categories()


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get a single expense",
    description="Retrieve a specific expense by its unique ID"
)
async def get_expense(
    expense_id: str,
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Get a single expense by ID.

    Returns the expense details if found.
    """
    expense = service.get_expense(expense_id)
    if not expense:
        raise APIError(
            code="RESOURCE_NOT_FOUND",
            message=f"Expense with ID {expense_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return expense


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Update an expense (full update)",
    description="Replace all fields of an existing expense"
)
async def update_expense(
    expense_id: str,
    expense_data: ExpenseCreate,
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Update an existing expense (full replacement).

    All fields (amount, category, description) must be provided.
    Returns the updated expense.
    """
    expense = service.update_expense(expense_id, expense_data)
    if not expense:
        raise APIError(
            code="RESOURCE_NOT_FOUND",
            message=f"Expense with ID {expense_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return expense


@router.patch(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Partially update an expense",
    description="Update specific fields of an existing expense"
)
async def partial_update_expense(
    expense_id: str,
    expense_data: ExpenseUpdate,
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> ExpenseResponse:
    """
    Partially update an existing expense.

    Only provided fields will be updated. Other fields remain unchanged.
    Returns the updated expense.
    """
    expense = service.partial_update_expense(expense_id, expense_data)
    if not expense:
        raise APIError(
            code="RESOURCE_NOT_FOUND",
            message=f"Expense with ID {expense_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return expense


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Permanently delete an expense by ID"
)
async def delete_expense(
    expense_id: str,
    current_user: str = Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service)
) -> None:
    """
    Delete an expense by ID.

    Returns 204 No Content on success.
    """
    success = service.delete_expense(expense_id)
    if not success:
        raise APIError(
            code="RESOURCE_NOT_FOUND",
            message=f"Expense with ID {expense_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
