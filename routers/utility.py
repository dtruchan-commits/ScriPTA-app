"""
Utility endpoints for the ScriPTA API.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "ScriPTA", "version": "1.0.1"}
