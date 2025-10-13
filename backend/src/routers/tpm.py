"""
TPM configuration endpoints for the ScriPTA API.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from ..models.models import TpmConfigResponse
from .database import get_tpms_from_db

router = APIRouter()


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
