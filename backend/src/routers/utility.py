"""
Utility endpoints for the ScriPTA API.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "ScriPTA", "version": "1.0.1"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ScriPTA API"}
