"""FastAPI main application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import transactions

# Configure logging (API convention - overrides root's print statements)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Finance Tracker API",
    description="A RESTful API for tracking personal financial transactions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint returning API status."""
    logger.info("Root endpoint accessed")
    return {
        'status': 'success',
        'message': 'Personal Finance Tracker API',
        'version': '1.0.0'
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'healthy'}
