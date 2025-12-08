# Personal Finance Tracker API - Usage Guide

## Overview

A FastAPI-based REST API for tracking personal financial transactions with full CRUD operations, JSON storage, and automatic API documentation.

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r src/api/requirements.txt
```

### Running the Server

```bash
# Option 1: Using the run script
./src/api/run.sh

# Option 2: Using uvicorn directly
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000

### API Documentation

Once the server is running, access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root & Health Check

#### GET /
Returns API status and version information.

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "success",
  "message": "Personal Finance Tracker API",
  "version": "1.0.0"
}
```

#### GET /health
Health check endpoint.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### Transaction Endpoints

All transaction endpoints are prefixed with `/api/v1/transactions`

#### POST /api/v1/transactions/
Create a new transaction.

**Request Body:**
```json
{
  "amount": 50.00,
  "category": "groceries",
  "description": "Weekly shopping"  // optional
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 50.00, "category": "groceries", "description": "Weekly shopping"}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "amount": 50.0,
  "category": "groceries",
  "description": "Weekly shopping",
  "date": "2025-10-25T07:55:09.735556"
}
```

#### GET /api/v1/transactions/
List all transactions with optional filtering and pagination.

**Query Parameters:**
- `category` (optional): Filter by category
- `limit` (optional, default: 100): Maximum number of results (1-1000)
- `offset` (optional, default: 0): Number of results to skip

**Example - List all:**
```bash
curl http://localhost:8000/api/v1/transactions/
```

**Example - Filter by category:**
```bash
curl "http://localhost:8000/api/v1/transactions/?category=groceries"
```

**Example - With pagination:**
```bash
curl "http://localhost:8000/api/v1/transactions/?limit=10&offset=0"
```

**Response (200 OK):**
```json
{
  "transactions": [
    {
      "id": 2,
      "amount": 125.5,
      "category": "utilities",
      "description": "",
      "date": "2025-10-25T07:55:33.763567"
    },
    {
      "id": 1,
      "amount": 50.0,
      "category": "groceries",
      "description": "Weekly shopping",
      "date": "2025-10-25T07:55:09.735556"
    }
  ],
  "total_count": 2
}
```

#### GET /api/v1/transactions/{transaction_id}
Get a specific transaction by ID.

**Example:**
```bash
curl http://localhost:8000/api/v1/transactions/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "amount": 50.0,
  "category": "groceries",
  "description": "Weekly shopping",
  "date": "2025-10-25T07:55:09.735556"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Transaction 999 not found"
}
```

#### PUT /api/v1/transactions/{transaction_id}
Update an existing transaction.

**Request Body (all fields optional):**
```json
{
  "amount": 55.00,
  "category": "groceries",
  "description": "Updated description"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/api/v1/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated weekly shopping at Whole Foods"}'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "amount": 50.0,
  "category": "groceries",
  "description": "Updated weekly shopping at Whole Foods",
  "date": "2025-10-25T07:55:09.735556"
}
```

#### DELETE /api/v1/transactions/{transaction_id}
Delete a transaction.

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/transactions/1
```

**Response (204 No Content):**
Empty response with status code 204.

**Response (404 Not Found):**
```json
{
  "detail": "Transaction 1 not found"
}
```

## Data Storage

Transactions are stored in a JSON file at the project root: `transactions.json`

Example structure:
```json
[
  {
    "id": 1,
    "amount": 50.0,
    "category": "groceries",
    "description": "Weekly shopping",
    "date": "2025-10-25T07:55:09.735556"
  }
]
```

## Data Validation

### Amount
- Must be a positive number (greater than 0)
- Stored as Decimal for precision
- Returned as float in JSON responses

### Category
- Required field
- Minimum length: 1 character
- String type

### Description
- Optional field
- Defaults to empty string if not provided
- String type

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Successful GET/PUT request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Validation error (e.g., negative amount)
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Invalid request format

Example error response:
```json
{
  "detail": "Transaction amount must be positive, got -10.0"
}
```

## API Conventions (from src/api/CLAUDE.md)

This API follows specific conventions that override the root project conventions:

1. **String Quotes**: Uses single quotes for dictionary keys and API responses
2. **Error Handling**: Uses FastAPI HTTPException instead of standard exceptions
3. **Logging**: Uses Python's logging module with structured logs
4. **Async**: All route handlers are async functions
5. **Response Models**: Always returns Pydantic models, never raw dicts

## Development

### Code Quality Tools

```bash
# Type checking
mypy src/api/

# Code formatting
black src/api/ && isort src/api/

# Run tests (when available)
pytest src/api/
```

### Project Structure

```
src/api/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── schemas.py              # Pydantic models for validation
├── routers/
│   ├── __init__.py
│   └── transactions.py     # Transaction CRUD endpoints
├── services/
│   ├── __init__.py
│   └── storage.py          # JSON storage service
├── requirements.txt        # Python dependencies
├── run.sh                  # Startup script
└── README.md              # Project overview
```

## Testing Examples

Here's a complete workflow to test all features:

```bash
# 1. Start the server
./src/api/run.sh

# 2. Create transactions
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 50.00, "category": "groceries", "description": "Weekly shopping"}'

curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"amount": 125.50, "category": "utilities"}'

# 3. List all transactions
curl http://localhost:8000/api/v1/transactions/

# 4. Filter by category
curl "http://localhost:8000/api/v1/transactions/?category=groceries"

# 5. Get specific transaction
curl http://localhost:8000/api/v1/transactions/1

# 6. Update transaction
curl -X PUT http://localhost:8000/api/v1/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'

# 7. Delete transaction
curl -X DELETE http://localhost:8000/api/v1/transactions/2

# 8. Verify deletion
curl http://localhost:8000/api/v1/transactions/
```

## Version

Current API version: **1.0.0**
