"""
TPM configuration endpoints for the ScriPTA API.
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models import TPMConfigResponse
from routers.database import get_tpms_from_db

router = APIRouter()


@router.get("/get_tpm_config", response_model=TPMConfigResponse)
async def get_tpm_config(tpm_name: Optional[str] = Query(None, description="Filter by TPM name", alias="tpmName")) -> TPMConfigResponse:
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
    
    # Get TPM data from database
    tpms = get_tpms_from_db(tpm_name)
    
    if tpm_name and not tpms:
        raise HTTPException(status_code=404, detail=f"TPM name '{tpm_name}' not found")
    
    return TPMConfigResponse(tpms=tpms)