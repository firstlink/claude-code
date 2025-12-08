"""Pydantic schemas for API request/response models."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""

    amount: Decimal = Field(..., description="Transaction amount", gt=0)
    category: str = Field(..., min_length=1, description="Transaction category")
    description: Optional[str] = Field(default="", description="Transaction description")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        """Validate amount is positive."""
        if value <= 0:
            raise ValueError(f"Transaction amount must be positive, got {value}")
        return value


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating an existing transaction."""

    amount: Optional[Decimal] = Field(None, description="Transaction amount", gt=0)
    category: Optional[str] = Field(None, min_length=1, description="Transaction category")
    description: Optional[str] = Field(None, description="Transaction description")


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""

    id: int = Field(..., description="Unique transaction ID")
    date: datetime = Field(..., description="Transaction date")

    class Config:
        """Pydantic model configuration."""

        from_attributes = True
        json_encoders = {
            Decimal: lambda value: float(value),
            datetime: lambda value: value.isoformat()
        }


class TransactionList(BaseModel):
    """Schema for list of transactions."""

    transactions: list[TransactionResponse]
    total_count: int

    class Config:
        """Pydantic model configuration."""

        json_encoders = {
            Decimal: lambda value: float(value),
            datetime: lambda value: value.isoformat()
        }
