"""
Layer configuration endpoints for the ScriPTA API.
"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query

from ..models.models import LayerConfigSet, LayerConfigSetResponse
from .database import (
    create_layer_config_in_db,
    delete_layer_config_from_db,
    get_layer_configs_from_db,
    update_layer_config_in_db,
)

router = APIRouter(tags=["InDesign Layer Configuration"])


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


@router.post("/create_layer_config", response_model=LayerConfigSet)
async def create_layer_config(layer_config_set: LayerConfigSet) -> LayerConfigSet:
    """
    Create a new layer configuration set.

    Args:
        layer_config_set: Layer configuration set data to create

    Returns:
        Created layer configuration set
    """
    try:
        created_config = create_layer_config_in_db(layer_config_set)
        return created_config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create layer config: {str(e)}")


@router.put("/update_layer_config/{config_name}", response_model=LayerConfigSet)
async def update_layer_config(
    layer_config_set: LayerConfigSet,
    config_name: str = Path(..., description="Config name to update"),
) -> LayerConfigSet:
    """
    Update an existing layer configuration set.

    Args:
        config_name: The current config name of the layer configuration set to update
        layer_config_set: New layer configuration set data

    Returns:
        Updated layer configuration set
    """
    try:
        updated_config = update_layer_config_in_db(config_name, layer_config_set)
        return updated_config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update layer config: {str(e)}")


@router.delete("/delete_layer_config/{config_name}")
async def delete_layer_config(
    config_name: str = Path(..., description="Config name to delete")
) -> dict:
    """
    Delete a layer configuration set.

    Args:
        config_name: The config name of the layer configuration set to delete

    Returns:
        Confirmation message
    """
    try:
        delete_layer_config_from_db(config_name)
        return {"message": f"Layer config '{config_name}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete layer config: {str(e)}")
