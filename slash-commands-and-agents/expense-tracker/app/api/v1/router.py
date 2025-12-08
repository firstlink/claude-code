"""Main API v1 router."""

from fastapi import APIRouter
from app.api.v1.endpoints import expenses


api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(expenses.router)
