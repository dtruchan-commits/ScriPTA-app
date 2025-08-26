from fastapi import FastAPI
from typing import List
from models import SwatchConfig, SwatchConfigResponse, ColorModel, ColorSpace
from data import get_hardcoded_swatches

app = FastAPI(
    title="SwatchWorx API",
    description="API for managing swatch configurations",
    version="1.0.0"
)


@app.get("/get_swatch_config", response_model=SwatchConfigResponse)
async def get_swatch_config() -> SwatchConfigResponse:
    """
    Get hardcoded swatch configuration data.
    
    Returns swatch configuration in the format:
    - Colorname: Name of the color
    - Color Model: SPOT or PROCESS
    - Color Space: CMYK, RGB, LAB
    - Colorvalues: Color values as comma-separated string
    """
    
    # Get swatch data from external data module
    hardcoded_swatches = get_hardcoded_swatches()
    
    return SwatchConfigResponse(swatches=hardcoded_swatches)


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "SwatchWorx API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
