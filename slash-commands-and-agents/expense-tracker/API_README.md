# Expense Tracker RESTful API

A comprehensive RESTful API for personal expense tracking built with FastAPI, featuring JWT authentication, pagination, filtering, and detailed analytics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Development](#development)

## Features

- **Complete CRUD Operations**: Create, read, update, and delete expenses
- **Advanced Filtering**: Filter by category, amount range
- **Flexible Sorting**: Sort by date, amount, or category
- **Pagination**: Efficient pagination with metadata and navigation links
- **Analytics**: Spending summaries with category breakdowns
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **Input Validation**: Comprehensive validation with detailed error messages
- **OpenAPI Documentation**: Interactive API documentation with Swagger UI
- **Error Tracking**: Request IDs for debugging and error tracking
- **Security Headers**: Built-in security headers for production deployment

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
cd expense-tracker
```

2. Install API dependencies:
```bash
pip install -r requirements-api.txt
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. Edit `.env` and set your configuration (especially SECRET_KEY and JWT_SECRET_KEY for production)

## Quick Start

### Running the API Server

Start the FastAPI server using uvicorn:

```bash
# Development mode with auto-reload
cd expense-tracker
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/api/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

### Health Check

Verify the API is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-10T10:00:00Z",
  "services": {
    "storage": "healthy"
  }
}
```

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. For this basic implementation, you can generate a demo token programmatically.

### Generating a Token (Demo)

```python
from app.utils.auth import create_demo_token

token = create_demo_token(user_id="demo-user")
print(f"Bearer {token}")
```

### Using the Token

Include the token in the Authorization header for all API requests:

```bash
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/v1/expenses
```

**Note**: For production use, implement proper user authentication with login endpoints and password hashing.

## API Endpoints

### Base URL

All API endpoints are prefixed with: `/api/v1`

### Expenses

#### Create Expense

```http
POST /api/v1/expenses
```

**Request Body:**
```json
{
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at cafe"
}
```

**Response (201 Created):**
```json
{
  "id": "d5e2f379-9452-4765-9667-5998c5762117",
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at cafe",
  "date": "2025-10-10 14:30:00"
}
```

---

#### List Expenses

```http
GET /api/v1/expenses?page=1&limit=20&category=Food&sort_by=date&order=desc
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (1-indexed) |
| limit | integer | 20 | Items per page (max 100) |
| category | string | - | Filter by category (case-insensitive) |
| min_amount | float | - | Minimum expense amount |
| max_amount | float | - | Maximum expense amount |
| sort_by | string | date | Sort field (date, amount, category) |
| order | string | desc | Sort order (asc, desc) |

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "d5e2f379-9452-4765-9667-5998c5762117",
      "amount": 25.50,
      "category": "Food",
      "description": "Lunch at cafe",
      "date": "2025-10-10 14:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total_items": 45,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false
  },
  "links": {
    "self": "/api/v1/expenses?page=1&limit=20",
    "next": "/api/v1/expenses?page=2&limit=20",
    "previous": null,
    "first": "/api/v1/expenses?page=1&limit=20",
    "last": "/api/v1/expenses?page=3&limit=20"
  }
}
```

---

#### Get Single Expense

```http
GET /api/v1/expenses/{expense_id}
```

**Response (200 OK):**
```json
{
  "id": "d5e2f379-9452-4765-9667-5998c5762117",
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at cafe",
  "date": "2025-10-10 14:30:00"
}
```

---

#### Update Expense (Full)

```http
PUT /api/v1/expenses/{expense_id}
```

**Request Body:**
```json
{
  "amount": 30.00,
  "category": "Food",
  "description": "Dinner at restaurant"
}
```

**Response (200 OK):** Returns updated expense

---

#### Update Expense (Partial)

```http
PATCH /api/v1/expenses/{expense_id}
```

**Request Body (only fields to update):**
```json
{
  "description": "Updated description only"
}
```

**Response (200 OK):** Returns updated expense

---

#### Delete Expense

```http
DELETE /api/v1/expenses/{expense_id}
```

**Response (204 No Content):** No body returned

---

#### Get Spending Summary

```http
GET /api/v1/expenses/summary
```

**Response (200 OK):**
```json
{
  "total_spending": 245.75,
  "total_expenses": 12,
  "average_expense": 20.48,
  "period": null,
  "by_category": {
    "Food": {
      "total": 125.50,
      "count": 6,
      "percentage": 51.08,
      "average": 20.92
    },
    "Transport": {
      "total": 90.00,
      "count": 4,
      "percentage": 36.63,
      "average": 22.50
    }
  }
}
```

---

#### Get Categories

```http
GET /api/v1/expenses/categories
```

**Response (200 OK):**
```json
{
  "categories": [
    {
      "name": "Food",
      "expense_count": 6,
      "total_amount": 125.50
    },
    {
      "name": "Transport",
      "expense_count": 4,
      "total_amount": 90.00
    }
  ],
  "total_categories": 2
}
```

## Examples

### Using cURL

#### Create an expense

```bash
# First, get a token (in production, use proper login)
TOKEN="your-jwt-token-here"

# Create expense
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at cafe"
  }'
```

#### List expenses with filters

```bash
curl -X GET "http://localhost:8000/api/v1/expenses?category=Food&min_amount=10&max_amount=50&sort_by=amount&order=desc" \
  -H "Authorization: Bearer $TOKEN"
```

#### Get spending summary

```bash
curl -X GET "http://localhost:8000/api/v1/expenses/summary" \
  -H "Authorization: Bearer $TOKEN"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
TOKEN = "your-jwt-token-here"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create expense
response = requests.post(
    f"{BASE_URL}/expenses",
    headers=HEADERS,
    json={
        "amount": 25.50,
        "category": "Food",
        "description": "Lunch at cafe"
    }
)
print(response.json())

# List expenses
response = requests.get(
    f"{BASE_URL}/expenses",
    headers=HEADERS,
    params={
        "page": 1,
        "limit": 20,
        "category": "Food"
    }
)
print(response.json())

# Get summary
response = requests.get(
    f"{BASE_URL}/expenses/summary",
    headers=HEADERS
)
print(response.json())
```

### Using JavaScript (Fetch)

```javascript
const BASE_URL = "http://localhost:8000/api/v1";
const TOKEN = "your-jwt-token-here";

// Create expense
async function createExpense() {
  const response = await fetch(`${BASE_URL}/expenses`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      amount: 25.50,
      category: 'Food',
      description: 'Lunch at cafe'
    })
  });

  const data = await response.json();
  console.log(data);
}

// List expenses
async function listExpenses() {
  const params = new URLSearchParams({
    page: 1,
    limit: 20,
    category: 'Food'
  });

  const response = await fetch(`${BASE_URL}/expenses?${params}`, {
    headers: {
      'Authorization': `Bearer ${TOKEN}`
    }
  });

  const data = await response.json();
  console.log(data);
}
```

## Error Handling

All errors follow a consistent format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "amount",
        "message": "Amount must be positive",
        "type": "value_error"
      }
    ],
    "timestamp": "2025-10-10T10:00:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 422 | Input validation failed |
| RESOURCE_NOT_FOUND | 404 | Requested resource not found |
| AUTHENTICATION_REQUIRED | 401 | Authentication credentials missing |
| INTERNAL_ERROR | 500 | Unexpected server error |

### HTTP Status Codes

- **200 OK**: Successful GET, PUT, PATCH requests
- **201 Created**: Successful POST request (resource created)
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Malformed request
- **401 Unauthorised**: Missing or invalid authentication
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Unexpected server error

## Development

### Project Structure

```
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── api/
│   │   └── v1/
│   │       ├── router.py       # Main router
│   │       └── endpoints/
│   │           └── expenses.py # Expense endpoints
│   ├── schemas/
│   │   └── expense.py          # Pydantic schemas
│   ├── services/
│   │   └── expense_service.py  # Business logic
│   ├── middleware/
│   │   └── error_handler.py    # Error handling
│   └── utils/
│       └── auth.py             # Authentication utilities
├── expense_tracker.py          # Original CLI application
├── requirements-api.txt        # API dependencies
├── .env.example                # Environment variables template
└── API_README.md               # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code with black
black app/

# Lint with flake8
flake8 app/

# Type checking with mypy
mypy app/
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `SECRET_KEY`: Secret key for application (change in production)
- `JWT_SECRET_KEY`: Secret key for JWT tokens (change in production)
- `ENVIRONMENT`: deployment environment (development/production)
- `ALLOWED_ORIGINS`: CORS allowed origins
- `DATA_FILE`: Path to JSON storage file

## API Versioning

The API is versioned using URL path versioning (`/api/v1/`). Future versions will be released as `/api/v2/`, etc.

## Rate Limiting

API requests are rate-limited to 60 requests per minute per user. Rate limit headers are included in responses:

- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time when the rate limit resets

## Security Considerations

### Production Deployment

1. **Change Secret Keys**: Update `SECRET_KEY` and `JWT_SECRET_KEY` in production
2. **Enable HTTPS**: Use TLS/SSL certificates
3. **Configure CORS**: Restrict `ALLOWED_ORIGINS` to your domains
4. **Use Environment Variables**: Never commit secrets to version control
5. **Implement Rate Limiting**: Protect against abuse
6. **Add Logging**: Monitor API usage and errors
7. **Database Migration**: Consider migrating from JSON to PostgreSQL for production

### Security Headers

The API includes the following security headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (production only)

## Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

**Module not found errors**:
```bash
# Ensure you're in the expense-tracker directory
cd expense-tracker
# And that dependencies are installed
pip install -r requirements-api.txt
```

**Authentication errors**:
- Ensure you're including the Authorization header
- Check that your JWT token is valid and not expired
- Verify JWT_SECRET_KEY matches between token generation and validation

## Future Enhancements

- [ ] User registration and login endpoints
- [ ] Database migration (PostgreSQL)
- [ ] Date range filtering for expenses
- [ ] Export expenses to CSV/PDF
- [ ] Recurring expenses
- [ ] Budget management
- [ ] Multi-currency support
- [ ] Expense attachments (receipts)
- [ ] GraphQL API option
- [ ] Websocket support for real-time updates

## Support

For issues, questions, or contributions:

1. Check the interactive API documentation at `/api/docs`
2. Review this README and the main project README
3. Check the issue tracker
4. Submit a pull request with improvements

## Licence

This project is open source. Feel free to use, modify, and distribute.

## Changelog

### v1.0.0 (2025-10-10)
- Initial REST API implementation
- Complete CRUD operations for expenses
- JWT authentication
- Pagination and filtering
- Spending analytics
- OpenAPI/Swagger documentation
- Error handling with request IDs
- Security headers and CORS support
