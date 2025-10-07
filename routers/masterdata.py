"""
Masterdata configuration endpoints for the ScriPTA API.
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models.models import MasterdataConfigResponse
from routers.database import get_masterdata_from_db

router = APIRouter()


@router.get("/get_masterdata", response_model=MasterdataConfigResponse)
async def get_masterdata(matnr8: Optional[int] = Query(None, description="Filter by MATNR8", alias="matnr8")) -> MasterdataConfigResponse:
    """
    Get masterdata configuration, optionally filtered by MATNR8.

    Args:
        matnr8: Optional MATNR8 (8-digit material number) to filter results (e.g., 91967086)

    Returns masterdata configuration including all material information.
    """

    # Get masterdata from database
    masterdata = get_masterdata_from_db(matnr8)

    if matnr8 and not masterdata:
        raise HTTPException(status_code=404, detail=f"MATNR8 '{matnr8}' not found")

    return MasterdataConfigResponse(masterdata=masterdata)
