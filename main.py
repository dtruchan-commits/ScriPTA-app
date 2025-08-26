from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from models import SwatchConfig, SwatchConfigResponse, ColorModel, ColorSpace
from data import get_hardcoded_swatches

app = FastAPI(
    title="SwatchWorx API",
    description="API for managing swatch configurations",
    version="1.0.0"
)


@app.get("/get_swatch_config", response_model=SwatchConfigResponse)
async def get_swatch_config(colorname: Optional[str] = Query(None, description="Filter by colorname")) -> SwatchConfigResponse:
    """
    Get swatch configuration data, optionally filtered by colorname.
    
    Args:
        colorname: Optional colorname to filter results (e.g., "DIELINE")
    
    Returns swatch configuration in the format:
    - Colorname: Name of the color
    - Color Model: SPOT or PROCESS
    - Color Space: CMYK, RGB, LAB
    - Colorvalues: Color values as comma-separated string
    """
    
    # Get all swatch data from external data module
    all_swatches = get_hardcoded_swatches()
    
    # Filter by colorname if provided
    if colorname:
        filtered_swatches = [swatch for swatch in all_swatches if swatch.colorname == colorname]
        if not filtered_swatches:
            raise HTTPException(status_code=404, detail=f"Colorname '{colorname}' not found")
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
