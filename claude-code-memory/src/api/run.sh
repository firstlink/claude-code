#!/bin/bash
# Startup script for FastAPI development server

echo "Starting Personal Finance Tracker API..."
echo "API will be available at: http://localhost:8000"
echo "Swagger UI docs: http://localhost:8000/docs"
echo "ReDoc: http://localhost:8000/redoc"
echo ""

# Navigate to project root
cd "$(dirname "$0")/../.."

# Run uvicorn from project root
uvicorn src.api.main:app --reload --port 8000
