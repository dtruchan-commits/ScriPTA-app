"""
Swatch configuration endpoints for the ScriPTA API.
"""
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query

from ..models.models import SwatchConfig, SwatchConfigResponse
from .database import (
    create_swatch_in_db,
    delete_swatch_from_db,
    get_swatches_from_db,
    update_swatch_in_db,
)

router = APIRouter(tags=["Swatch Configuration"])


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


@router.post("/create_swatch_config", response_model=SwatchConfig)
async def create_swatch_config(swatch_config: SwatchConfig) -> SwatchConfig:
    """
    Create a new swatch configuration.

    Args:
        swatch_config: Swatch configuration data to create

    Returns:
        Created swatch configuration
    """
    try:
        created_swatch = create_swatch_in_db(swatch_config)
        return created_swatch
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create swatch: {str(e)}")


@router.put("/update_swatch_config/{color_name}", response_model=SwatchConfig)
async def update_swatch_config(
    color_name: str = Path(..., description="Color name to update"),
    swatch_config: SwatchConfig = Body(...),
) -> SwatchConfig:
    """
    Update an existing swatch configuration.

    Args:
        color_name: The current color name of the swatch to update
        swatch_config: New swatch configuration data

    Returns:
        Updated swatch configuration
    """
    try:
        updated_swatch = update_swatch_in_db(color_name, swatch_config)
        return updated_swatch
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update swatch: {str(e)}")


@router.delete("/delete_swatch_config/{color_name}")
async def delete_swatch_config(
    color_name: str = Path(..., description="Color name to delete")
) -> dict:
    """
    Delete a swatch configuration.

    Args:
        color_name: The color name of the swatch to delete

    Returns:
        Confirmation message
    """
    try:
        delete_swatch_from_db(color_name)
        return {"message": f"Swatch '{color_name}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete swatch: {str(e)}")
