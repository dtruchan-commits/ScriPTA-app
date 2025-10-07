"""
Layer configuration endpoints for the ScriPTA API.
"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from models.models import LayerConfigSetResponse
from routers.database import get_layer_configs_from_db

router = APIRouter()


@router.get("/get_layer_config", response_model=List[LayerConfigSetResponse])
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