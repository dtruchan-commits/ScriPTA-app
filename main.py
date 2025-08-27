from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from models import SwatchConfig, SwatchConfigResponse, ColorModel, ColorSpace
from data.swatches import SWATCH_DATA

app = FastAPI(
    title="SwatchWorx API",
    description="API for managing swatch configurations",
    version="1.0.0"
)


@app.get("/get_swatch_config", response_model=SwatchConfigResponse)
async def get_swatch_config(color_name: Optional[str] = Query(None, description="Filter by color name", alias="colorName")) -> SwatchConfigResponse:
    """
    Get swatch configuration data, optionally filtered by color name.
    
    Args:
        color_name: Optional color name to filter results (e.g., "DIELINE")
    
    Returns swatch configuration in the format:
    - ColorName: Name of the color
    - Color Model: SPOT or PROCESS
    - Color Space: CMYK, RGB, LAB
    - ColorValues: Color values as comma-separated string
    """
    
    # Get all swatch data from external data module
    all_swatches = SWATCH_DATA
    
    # Filter by color_name if provided
    if color_name:
        filtered_swatches = [swatch for swatch in all_swatches if swatch.color_name == color_name]
        if not filtered_swatches:
            raise HTTPException(status_code=404, detail=f"Color name '{color_name}' not found")
        return SwatchConfigResponse(swatches=filtered_swatches)
    
    # Return all swatches if no filter is provided
    return SwatchConfigResponse(swatches=all_swatches)


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "SwatchWorx API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
