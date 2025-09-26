from typing import List, Optional
import sqlite3
import json
import os

from fastapi import FastAPI, HTTPException, Query

from models import (
    ColorModel,
    ColorSpace,
    LayerConfigResponse,
    LayerConfigSetResponse,
    SwatchConfig,
    SwatchConfigResponse,
)

# Database configuration
DB_PATH = "scripta-db.sqlite3"

def get_db_connection():
    """Create and return a database connection."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database file not found")
    return sqlite3.connect(DB_PATH)

def get_swatches_from_db(color_name: Optional[str] = None) -> List[SwatchConfig]:
    """Retrieve swatch configurations from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        if color_name:
            query = """
                SELECT color_name, color_model, color_space, color_values 
                FROM swatches 
                WHERE color_name = ?
            """
            cursor.execute(query, (color_name,))
        else:
            query = """
                SELECT color_name, color_model, color_space, color_values 
                FROM swatches
                ORDER BY color_name
            """
            cursor.execute(query)
        
        rows = cursor.fetchall()
        swatches = []
        
        for row in rows:
            color_values = json.loads(row[3])  # Parse JSON string to list
            swatch = SwatchConfig(
                color_name=row[0],
                color_model=ColorModel(row[1]),
                color_space=ColorSpace(row[2]),
                color_values=color_values
            )
            swatches.append(swatch)
        
        return swatches
    finally:
        conn.close()

def get_layer_configs_from_db(config_name: Optional[str] = None) -> List[LayerConfigSetResponse]:
    """Retrieve layer configurations from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        if config_name:
            query = """
                SELECT lcs.config_name, lc.name, lc.locked, lc.print, lc.color
                FROM layer_config_sets lcs
                JOIN layer_config lc ON lcs.id = lc.config_set_id
                WHERE lcs.config_name = ?
                ORDER BY lcs.config_name, lc.id
            """
            cursor.execute(query, (config_name,))
        else:
            query = """
                SELECT lcs.config_name, lc.name, lc.locked, lc.print, lc.color
                FROM layer_config_sets lcs
                JOIN layer_config lc ON lcs.id = lc.config_set_id
                ORDER BY lcs.config_name, lc.id
            """
            cursor.execute(query)
        
        rows = cursor.fetchall()
        
        # Group layers by config_name
        configs_dict = {}
        for row in rows:
            config_name_db = row[0]
            if config_name_db not in configs_dict:
                configs_dict[config_name_db] = []
            
            layer_config = LayerConfigResponse(
                name=row[1],
                locked=bool(row[2]),
                print=bool(row[3]),
                color=row[4]
            )
            configs_dict[config_name_db].append(layer_config)
        
        # Convert to response format
        response_configs = []
        for config_name_key, layers in configs_dict.items():
            response_configs.append(
                LayerConfigSetResponse(
                    config_name=config_name_key,
                    layers=layers
                )
            )
        
        return response_configs
    finally:
        conn.close()

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
    
    # Get swatch data from database
    swatches = get_swatches_from_db(color_name)
    
    if color_name and not swatches:
        raise HTTPException(status_code=404, detail=f"Color name '{color_name}' not found")
    
    return SwatchConfigResponse(swatches=swatches)


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
    
    # Get layer data from database
    response_configs = get_layer_configs_from_db(config_name)
    
    if config_name and not response_configs:
        raise HTTPException(status_code=404, detail=f"Config name '{config_name}' not found")
    
    return response_configs


@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {"message": "ScriPTA", "version": "1.0.1"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
