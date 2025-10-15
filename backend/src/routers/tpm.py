"""
TPM configuration endpoints for the ScriPTA API.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from ..models.models import TpmConfig, TpmConfigRequest, TpmConfigResponse
from .database import (
    create_tpm_in_db,
    delete_tpm_from_db,
    get_tpm_by_id_from_db,
    get_tpms_from_db,
    update_tpm_in_db,
)

router = APIRouter(tags=["TPM"])


@router.get("/get_tpm_config", response_model=TpmConfigResponse)
async def get_tpm_config(tpm_name: Optional[str] = Query(None, description="Filter by TPM name", alias="tpmName")) -> TpmConfigResponse:
    """
    Get TPM configuration data, optionally filtered by TPM name.

    Args:
        tpm_name: Optional TPM name to filter results (e.g., "new one two three")

    Returns TPM configuration with all fields from the database:
    - ID: Unique identifier
    - TPM: Name of the TPM
    - drawDieline: Draw dieline value
    - drawCombination: Draw combination value
    - A, B, H: Dimensions
    - variant: Variant name
    - version: Version number
    - variablesList: Variables list
    - createdBy: Created by user
    - createdAt: Creation date
    - modifiedBy: Modified by user
    - modifiedAt: Modification date
    - packType: Pack type
    - description: Description
    - comment: Comment
    - panelList: Panel list as JSON string
    - createdTimestamp: Created timestamp
    - updatedTimestamp: Updated timestamp
    """

    try:
        # Get TPM data from database
        tpms = get_tpms_from_db(tpm_name)

        if tpm_name and not tpms:
            raise HTTPException(status_code=404, detail=f"TPM name '{tpm_name}' not found")

        return TpmConfigResponse(tpms=tpms)

    except HTTPException:
        # Re-raise HTTPExceptions (like 404) without modification
        raise

    except ValidationError as e:
        logging.error(f"Validation error when processing TPM data: {e}")
        raise HTTPException(status_code=422, detail=f"Data validation error: {str(e)}")

    except Exception as e:
        logging.error(f"Unexpected error in get_tpm_config: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving TPM configuration")


@router.get("/get_tpm_by_id/{tpm_id}", response_model=TpmConfig)
async def get_tpm_by_id(tpm_id: int) -> TpmConfig:
    """
    Get a specific TPM configuration by ID.

    Args:
        tpm_id: The unique ID of the TPM record

    Returns:
        TpmConfig: The TPM configuration with the specified ID
    """
    try:
        tpm = get_tpm_by_id_from_db(tpm_id)
        if not tpm:
            raise HTTPException(status_code=404, detail=f"TPM with ID {tpm_id} not found")
        
        return tpm

    except HTTPException:
        raise
    except ValidationError as e:
        logging.error(f"Validation error when processing TPM data: {e}")
        raise HTTPException(status_code=422, detail=f"Data validation error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in get_tpm_by_id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving TPM configuration")


@router.post("/create_tpm", response_model=TpmConfig, status_code=201)
async def create_tpm(tpm_data: TpmConfigRequest) -> TpmConfig:
    """
    Create a new TPM configuration.

    Args:
        tpm_data: The TPM configuration data to create

    Returns:
        TpmConfig: The created TPM configuration with generated ID and timestamps
    """
    try:
        created_tpm = create_tpm_in_db(tpm_data)
        return created_tpm

    except HTTPException:
        raise
    except ValidationError as e:
        logging.error(f"Validation error when creating TPM: {e}")
        raise HTTPException(status_code=422, detail=f"Data validation error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in create_tpm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while creating TPM configuration")


@router.put("/update_tpm/{tpm_id}", response_model=TpmConfig)
async def update_tpm(tpm_id: int, tpm_data: TpmConfigRequest) -> TpmConfig:
    """
    Update an existing TPM configuration.

    Args:
        tpm_id: The unique ID of the TPM record to update
        tpm_data: The updated TPM configuration data

    Returns:
        TpmConfig: The updated TPM configuration
    """
    try:
        updated_tpm = update_tpm_in_db(tpm_id, tpm_data)
        return updated_tpm

    except HTTPException:
        raise
    except ValidationError as e:
        logging.error(f"Validation error when updating TPM: {e}")
        raise HTTPException(status_code=422, detail=f"Data validation error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in update_tpm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating TPM configuration")


@router.delete("/delete_tpm/{tpm_id}", status_code=204)
async def delete_tpm(tpm_id: int):
    """
    Delete a TPM configuration.

    Args:
        tpm_id: The unique ID of the TPM record to delete

    Returns:
        No content (204 status code) on successful deletion
    """
    try:
        success = delete_tpm_from_db(tpm_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"TPM with ID {tpm_id} not found")

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error in delete_tpm: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while deleting TPM configuration")
