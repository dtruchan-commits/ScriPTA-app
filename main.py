from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from data.layers import LAYER_DATA
from data.swatches import SWATCH_DATA
from models import (
    ColorModel,
    ColorSpace,
    LayerConfigResponse,
    LayerConfigSetResponse,
    SwatchConfig,
    SwatchConfigResponse,
)

app = FastAPI(
    title="ScriPTA",
    description="REST API for managing Technical Packaging Material Data and InDesign Swatch and Layer Configurations",
    version="1.0.1"
)


@app.get("/get_swatch_config", response_model=SwatchConfigResponse)
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


@app.get("/get_layer_config", response_model=List[LayerConfigSetResponse])
async def get_layer_config(config_name: Optional[str] = Query(None, description="Filter by config name", alias="configName")) -> List[LayerConfigSetResponse]:
    """
    Get layer configuration data, optionally filtered by config name.
    
    Args:
        config_name: Optional config name to filter results (e.g., "default", "FoldingBox")
    
    Returns layer configuration in the format:
    - configName: Name of the configuration
    - layers: List of layer configurations with name, locked, print, and color properties
    """
    
    # Get all layer data
    all_layer_configs = LAYER_DATA
    
    # Filter by config_name if provided
    if config_name:
        
        filtered_configs = [config for config in all_layer_configs if config.config_name == config_name]
        if not filtered_configs:
            raise HTTPException(status_code=404, detail=f"Config name '{config_name}' not found")
        selected_configs = filtered_configs
    else:
        selected_configs = all_layer_configs
    
    # Convert to response format
    response_configs = []
    for config in selected_configs:
        response_layers = [
            LayerConfigResponse(
                name=layer.name.value,
                locked=layer.locked,
                print=layer.print,
                color=layer.color.value
            )
            for layer in config.layers
        ]
        response_configs.append(
            LayerConfigSetResponse(
                config_name=config.config_name,
                layers=response_layers
            )
        )
    
    return response_configs


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "ScriPTA", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
