# FastAPI Web API

**INHERITS FROM**: Root CLAUDE.md
**OVERRIDES**: Specific conventions listed below

---

## 🧪 MEMORY LAB: API-Level Memory Configuration

This API-level CLAUDE.md demonstrates how subdirectory memory **overrides** root conventions for API-specific needs.


## API-Specific Conventions

### Async Everything
All route handlers must be async:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/v1/transactions")

@router.post("/", status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_async_db)
) -> TransactionResponse:
    """Create new transaction. Use JSON structure and store it local to the project"""
    result = await json
    return result
```


## Response Models
Always use Pydantic schemas for responses:
```python
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    transaction_type: str
    date: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }


### Error Handling
Use HTTP exceptions:
```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Transaction {transaction_id} not found"
)

# Validation error
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid transaction amount"
)
```


## API Documentation
FastAPI auto-generates docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Always include:
- Operation summary
- Parameter descriptions
- Response model
- Possible error codes


## Development Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

---

## 🧪 MEMORY LAB: API Overrides Root Conventions

### Override 1: String Quotes (OVERRIDES ROOT)
**API RULE**: Use **single quotes** for dictionary keys and API responses.
```python
# Correct (API convention - OVERRIDES root's double quotes)
response_data = {
    'transaction_id': transaction.id,
    'amount': float(transaction.amount),
    'status': 'success'
}

# Root says double quotes, but API overrides for JSON consistency
```

### Override 2: Error Handling (OVERRIDES ROOT)
**API RULE**: Use FastAPI HTTPException instead of standard exceptions.
```python
from fastapi import HTTPException, status

# Correct (API convention - OVERRIDES root's ValueError)
if transaction_id not in storage:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction {transaction_id} not found"
    )

# Root uses ValueError, but API needs HTTP-aware exceptions
```

### Override 3: Logging (OVERRIDES ROOT)
**API RULE**: Use Python's logging module with structured logs.
```python
import logging

logger = logging.getLogger(__name__)

# Correct (API convention - OVERRIDES root's print statements)
logger.info("Transaction created", extra={
    "transaction_id": txn_id,
    "amount": amount,
    "user_id": user_id
})

# Root uses print(), but API needs structured logging for production
```

### Inherited 4: Variable Naming (FROM ROOT)
**INHERITED**: Still use descriptive names, minimum 3 characters.
```python
# Correct (inherits from root)
transaction_data = await get_transaction(transaction_id)
user_request = TransactionCreate(**request_body)

# Still incorrect (root rule applies)
txn = await get_transaction(id)  # Too short
```

### Override 5: Return Types (API-SPECIFIC)
**API RULE**: Always return Pydantic models, never raw dicts.
```python
# Correct (API-specific rule)
@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int) -> TransactionResponse:
    return TransactionResponse(**transaction_data)

# Incorrect - don't return raw dicts in API
async def get_transaction(transaction_id: int) -> dict:
    return {"id": 1, "amount": 50.00}  # Should be Pydantic model
```

**Summary**: API memory overrides root for HTTP-specific concerns (exceptions, logging, response format) but inherits general coding standards (variable naming, type safety).