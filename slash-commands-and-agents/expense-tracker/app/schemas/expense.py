"""Pydantic schemas for expense-related requests and responses."""

import re
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    """Schema for creating a new expense."""

    amount: float = Field(..., gt=0, le=1000000, description="Expense amount in GBP")
    category: str = Field(..., min_length=1, max_length=100, description="Expense category")
    description: str = Field(..., min_length=1, max_length=500, description="Expense description")

    @field_validator("category", "description")
    @classmethod
    def sanitise_text(cls, v: str) -> str:
        """Sanitise text fields by stripping whitespace and removing dangerous characters."""
        v = v.strip()
        # Remove potentially dangerous characters
        v = re.sub(r'[<>"\'\\]', '', v)
        return v

    @field_validator("amount")
    @classmethod
    def validate_precision(cls, v: float) -> float:
        """Ensure amount has maximum 2 decimal places."""
        if round(v, 2) != v:
            raise ValueError("Amount can have maximum 2 decimal places")
        return v


class ExpenseUpdate(BaseModel):
    """Schema for partially updating an expense."""

    amount: Optional[float] = Field(None, gt=0, le=1000000, description="Expense amount in GBP")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Expense category")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Expense description")

    @field_validator("category", "description")
    @classmethod
    def sanitise_text(cls, v: Optional[str]) -> Optional[str]:
        """Sanitise text fields."""
        if v is None:
            return v
        v = v.strip()
        v = re.sub(r'[<>"\'\\]', '', v)
        return v

    @field_validator("amount")
    @classmethod
    def validate_precision(cls, v: Optional[float]) -> Optional[float]:
        """Ensure amount has maximum 2 decimal places."""
        if v is not None and round(v, 2) != v:
            raise ValueError("Amount can have maximum 2 decimal places")
        return v


class ExpenseResponse(BaseModel):
    """Schema for expense response."""

    id: str = Field(..., description="Unique expense identifier")
    amount: float = Field(..., description="Expense amount")
    category: str = Field(..., description="Expense category")
    description: str = Field(..., description="Expense description")
    date: str = Field(..., description="Expense date/time")

    class Config:
        """Pydantic config."""

        from_attributes = True


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Items per page")
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")


class PaginationLinks(BaseModel):
    """Pagination links."""

    self: str
    next: Optional[str] = None
    previous: Optional[str] = None
    first: str
    last: str


class PaginatedExpenseResponse(BaseModel):
    """Schema for paginated expense list response."""

    data: List[ExpenseResponse]
    pagination: PaginationMeta
    links: PaginationLinks


class CategoryInfo(BaseModel):
    """Schema for category information."""

    name: str
    expense_count: int
    total_amount: float


class CategoriesResponse(BaseModel):
    """Schema for categories list response."""

    categories: List[CategoryInfo]
    total_categories: int


class CategoryBreakdown(BaseModel):
    """Schema for category spending breakdown."""

    total: float
    count: int
    percentage: float
    average: float


class SpendingSummaryResponse(BaseModel):
    """Schema for spending summary response."""

    total_spending: float
    total_expenses: int
    average_expense: float
    period: Optional[Dict[str, str]] = None
    by_category: Dict[str, CategoryBreakdown]


class HealthResponse(BaseModel):
    """Schema for health check response."""

    status: str
    version: str
    timestamp: str
    services: Dict[str, str]


class ErrorDetail(BaseModel):
    """Schema for error detail."""

    field: Optional[str] = None
    message: str
    value: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Schema for error response."""

    error: Dict[str, Any] = Field(
        ...,
        description="Error information",
        example={
            "code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": [],
            "timestamp": "2025-10-10T10:00:00Z",
            "request_id": "req_abc123xyz"
        }
    )
