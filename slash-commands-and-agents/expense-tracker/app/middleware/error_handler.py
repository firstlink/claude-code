"""Error handling middleware and custom exceptions."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import uuid


class APIError(Exception):
    """Custom API error exception."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        details: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialise API error.

        Args:
            code: Error code
            message: Error message
            status_code: HTTP status code
            details: Optional list of error details
        """
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(self.message)


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """
    Handle custom API errors.

    Args:
        request: The request object
        exc: The API error exception

    Returns:
        JSON response with error details
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": request_id
            }
        }
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors.

    Args:
        request: The request object
        exc: The validation error exception

    Returns:
        JSON response with validation error details
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": errors,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": request_id
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.

    Args:
        request: The request object
        exc: The exception

    Returns:
        JSON response with generic error message
    """
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": [],
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": request_id
            }
        }
    )
