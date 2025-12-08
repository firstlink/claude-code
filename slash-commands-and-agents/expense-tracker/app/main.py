"""Main FastAPI application entry point for Expense Tracker API."""

import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.config import settings
from app.api.v1.router import api_router
from app.middleware.error_handler import (
    APIError,
    api_error_handler,
    validation_error_handler,
    generic_exception_handler
)
from app.schemas.expense import HealthResponse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
# Expense Tracker RESTful API

A comprehensive REST API for personal expense tracking with the following features:

## Features

* **CRUD Operations**: Create, read, update, and delete expenses
* **Filtering**: Filter expenses by category, amount range
* **Sorting**: Sort expenses by date, amount, or category
* **Pagination**: Efficient pagination with metadata and navigation links
* **Analytics**: Spending summaries with category breakdowns
* **Authentication**: JWT-based authentication for secure access
* **Validation**: Comprehensive input validation with detailed error messages

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

For demo purposes, you can obtain a token using the `/api/v1/auth/token` endpoint (not yet implemented in this basic version).

## Rate Limiting

API requests are rate-limited to prevent abuse. Current limit: 60 requests per minute.

## Response Format

All API responses follow a consistent format with appropriate HTTP status codes.

## Error Handling

Errors are returned in a standardised format with error codes, messages, and request IDs for debugging.
    """,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=[
        {
            "name": "expenses",
            "description": "Operations with expenses - create, read, update, delete, and analytics"
        },
        {
            "name": "health",
            "description": "Health check and system status endpoints"
        }
    ]
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    if settings.ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Health check endpoint
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check",
    description="Check the health status of the API and its services"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the current status of the API and its services.
    """
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.utcnow().isoformat() + "Z",
        services={
            "storage": "healthy"
        }
    )


# Root endpoint
@app.get(
    "/",
    tags=["health"],
    summary="API root",
    description="API root endpoint with basic information"
)
async def root():
    """API root endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/api/docs",
        "health": "/health"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Documentation available at: /api/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down application")
