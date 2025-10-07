"""
Swatch configuration endpoints for the ScriPTA API.
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models.models import SwatchConfigResponse
from routers.database import get_swatches_from_db

router = APIRouter()


@router.get("/get_swatch_config", response_model=SwatchConfigResponse)
async def get_swatch_config(color_name: Optional[str] = Query(None, description="Filter by color name", alias="colorName")) -> SwatchConfigResponse:
    """
    Get swatch configuration data, optionally filtered by color name.

    Args:
        color_name: Optional color name to filter results (e.g., "DIELINE")

    Returns swatch configuration in the format:
    - Color Name: Name of the color
    - Color Model: SPOT or PROCESS
    - Color Space: CMYK, RGB, LAB
    - Color Values: Color values as comma-separated string
    """

    # Get swatch data from database
    swatches = get_swatches_from_db(color_name)

    if color_name and not swatches:
        raise HTTPException(status_code=404, detail=f"Color name '{color_name}' not found")

    return SwatchConfigResponse(swatches=swatches)
