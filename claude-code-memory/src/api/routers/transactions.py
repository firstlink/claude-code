"""Transaction router with CRUD endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from src.api.schemas import (
    TransactionCreate,
    TransactionList,
    TransactionResponse,
    TransactionUpdate,
)
from src.api.services.storage import TransactionStorage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions")

# Initialize storage service
storage = TransactionStorage()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
) -> TransactionResponse:
    """
    Create a new transaction.

    Args:
        transaction: Transaction data to create

    Returns:
        Created transaction with ID and timestamp

    Raises:
        HTTPException: 400 if validation fails
    """
    try:
        created_transaction = await storage.create_transaction(
            amount=transaction.amount,
            category=transaction.category,
            description=transaction.description or "",
        )
        logger.info(
            "Transaction created",
            extra={
                'transaction_id': created_transaction['id'],
                'amount': float(created_transaction['amount']),
                'category': created_transaction['category'],
            }
        )
        return TransactionResponse(**created_transaction)
    except ValueError as error:
        logger.error(f"Validation error creating transaction: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get("/", response_model=TransactionList)
async def list_transactions(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> TransactionList:
    """
    List all transactions with optional filtering.

    Args:
        category: Optional category filter
        limit: Maximum number of results to return (1-1000)
        offset: Number of results to skip for pagination

    Returns:
        List of transactions and total count
    """
    transactions = await storage.list_transactions(
        category=category,
        limit=limit,
        offset=offset,
    )
    total_count = await storage.count_transactions(category=category)

    logger.info(
        "Transactions listed",
        extra={
            'count': len(transactions),
            'category_filter': category,
            'limit': limit,
            'offset': offset,
        }
    )

    return TransactionList(
        transactions=[TransactionResponse(**txn) for txn in transactions],
        total_count=total_count
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int) -> TransactionResponse:
    """
    Get a specific transaction by ID.

    Args:
        transaction_id: Unique transaction identifier

    Returns:
        Transaction details

    Raises:
        HTTPException: 404 if transaction not found
    """
    transaction = await storage.get_transaction(transaction_id)

    if transaction is None:
        logger.warning(f"Transaction not found: {transaction_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )

    logger.info(f"Transaction retrieved: {transaction_id}")
    return TransactionResponse(**transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
) -> TransactionResponse:
    """
    Update an existing transaction.

    Args:
        transaction_id: Unique transaction identifier
        transaction_update: Fields to update

    Returns:
        Updated transaction

    Raises:
        HTTPException: 404 if transaction not found, 400 if validation fails
    """
    # Check if transaction exists
    existing = await storage.get_transaction(transaction_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )

    try:
        updated_transaction = await storage.update_transaction(
            transaction_id=transaction_id,
            amount=transaction_update.amount,
            category=transaction_update.category,
            description=transaction_update.description,
        )
        logger.info(f"Transaction updated: {transaction_id}")
        return TransactionResponse(**updated_transaction)
    except ValueError as error:
        logger.error(f"Validation error updating transaction: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int) -> None:
    """
    Delete a transaction.

    Args:
        transaction_id: Unique transaction identifier

    Raises:
        HTTPException: 404 if transaction not found
    """
    deleted = await storage.delete_transaction(transaction_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )

    logger.info(f"Transaction deleted: {transaction_id}")
