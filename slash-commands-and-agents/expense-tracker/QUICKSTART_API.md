# Quick Start Guide - Expense Tracker REST API

This guide will help you get the Expense Tracker REST API up and running in 5 minutes.

## Prerequisites

- Python 3.7+
- pip

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements-api.txt
```

### 2. Set Up Environment (Optional)

```bash
cp .env.example .env
# Edit .env if needed (default values work for local development)
```

### 3. Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4. Access the Interactive Documentation

Open your browser and navigate to:

**Swagger UI**: http://localhost:8000/api/docs

This provides an interactive interface to test all API endpoints!

## Testing the API

### Option 1: Using Swagger UI (Easiest)

1. Go to http://localhost:8000/api/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the request body (if required)
5. For authentication:
   - Generate a token: Run Python script below
   - Click "Authorize" button at the top
   - Enter: `your-token-here` (without "Bearer" prefix)
   - Click "Authorize"
6. Click "Execute" to test the endpoint

### Option 2: Using cURL

First, generate a demo token:

```python
# Run this in Python to get a token
from app.utils.auth import create_demo_token
token = create_demo_token("demo-user")
print(f"Token: {token}")
```

Then use the token in your requests:

```bash
# Replace YOUR_TOKEN with the token from above
TOKEN="YOUR_TOKEN"

# Create an expense
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at cafe"
  }'

# List all expenses
curl -X GET "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer $TOKEN"

# Get spending summary
curl -X GET "http://localhost:8000/api/v1/expenses/summary" \
  -H "Authorization: Bearer $TOKEN"
```

### Option 3: Using Python

```python
import requests
from app.utils.auth import create_demo_token

# Generate token
token = create_demo_token("demo-user")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create expense
response = requests.post(
    "http://localhost:8000/api/v1/expenses",
    headers=headers,
    json={
        "amount": 25.50,
        "category": "Food",
        "description": "Lunch at cafe"
    }
)
print(response.json())

# List expenses
response = requests.get(
    "http://localhost:8000/api/v1/expenses",
    headers=headers
)
print(response.json())
```

## Common Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/expenses | Create a new expense |
| GET | /api/v1/expenses | List all expenses (paginated) |
| GET | /api/v1/expenses/{id} | Get a specific expense |
| PUT | /api/v1/expenses/{id} | Update an expense (full) |
| PATCH | /api/v1/expenses/{id} | Update an expense (partial) |
| DELETE | /api/v1/expenses/{id} | Delete an expense |
| GET | /api/v1/expenses/summary | Get spending summary |
| GET | /api/v1/expenses/categories | Get all categories |
| GET | /health | Health check |

## Example Workflow

```bash
# 1. Create some expenses
curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.50, "category": "Food", "description": "Lunch"}'

curl -X POST "http://localhost:8000/api/v1/expenses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 60.00, "category": "Transport", "description": "Monthly pass"}'

# 2. List expenses with filtering
curl -X GET "http://localhost:8000/api/v1/expenses?category=Food&sort_by=amount&order=desc" \
  -H "Authorization: Bearer $TOKEN"

# 3. Get spending summary
curl -X GET "http://localhost:8000/api/v1/expenses/summary" \
  -H "Authorization: Bearer $TOKEN"

# 4. Get categories
curl -X GET "http://localhost:8000/api/v1/expenses/categories" \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### "Module not found" errors

Make sure you're in the expense-tracker directory and have installed dependencies:

```bash
pwd  # Should show .../expense-tracker
pip install -r requirements-api.txt
```

### "Port already in use"

Use a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

### Authentication errors

Make sure you're including the Authorization header with a valid JWT token. Generate a new token using the Python code above.

### API returns 422 Validation Error

Check your request body format. Common issues:
- Amount must be positive
- Category and description cannot be empty
- Amount can have max 2 decimal places

## Next Steps

- Read the full [API_README.md](API_README.md) for detailed documentation
- Explore the interactive docs at http://localhost:8000/api/docs
- Check out example requests in the Swagger UI
- Review the [expense_tracker.py](expense_tracker.py) for the original CLI implementation

## Production Deployment

For production use:

1. Change `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`
2. Set `ENVIRONMENT=production` in `.env`
3. Use a proper database (PostgreSQL) instead of JSON file storage
4. Implement proper user authentication
5. Set up HTTPS with TLS certificates
6. Configure rate limiting and monitoring
7. Use a production ASGI server with multiple workers:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Happy API development!
