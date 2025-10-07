"""
Database utility functions for ScriPTA API.
"""
import json
import logging
import os
import sqlite3
from typing import List, Optional

from fastapi import HTTPException
from pydantic import ValidationError

from models.models import (
    ColorModel,
    ColorSpace,
    LayerConfigResponse,
    LayerConfigSetResponse,
    SwatchConfig,
    TpmConfig,
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


def get_tpms_from_db(tpm_name: Optional[str] = None) -> List[TpmConfig]:
    """Retrieve TPM configurations from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        if tpm_name:
            query = """
                SELECT id, TPM, drawDieline, drawCombination, A, B, H, variant, 
                       version, variablesList, createdBy, createdAt, modifiedBy, 
                       modifiedAt, packType, description, comment, panelList, 
                       created_timestamp, updated_timestamp
                FROM tpm 
                WHERE TPM = ?
            """
            cursor.execute(query, (tpm_name,))
        else:
            query = """
                SELECT id, TPM, drawDieline, drawCombination, A, B, H, variant, 
                       version, variablesList, createdBy, createdAt, modifiedBy, 
                       modifiedAt, packType, description, comment, panelList, 
                       created_timestamp, updated_timestamp
                FROM tpm
                ORDER BY TPM
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        tpms = []

        for row in rows:
            try:
                tpm = TpmConfig(
                    id=row[0],
                    tpm=row[1],
                    draw_dieline=row[2],
                    draw_combination=row[3],
                    a=row[4],
                    b=row[5],
                    h=row[6],
                    variant=row[7],
                    version=row[8],
                    variables_list=row[9],
                    created_by=row[10],
                    created_at=row[11],
                    modified_by=row[12],
                    modified_at=row[13],
                    pack_type=row[14],
                    description=row[15],
                    comment=row[16],
                    panel_list=row[17],
                    created_timestamp=row[18],
                    updated_timestamp=row[19]
                )
                tpms.append(tpm)
            except ValidationError as e:
                logging.error(f"Validation error for TPM record {row[0]} ('{row[1]}'): {e}")
                # Skip this record and continue with the next one
                continue
            except Exception as e:
                logging.error(f"Unexpected error processing TPM record {row[0] if row else 'unknown'}: {e}")
                continue

        return tpms
    finally:
        conn.close()
