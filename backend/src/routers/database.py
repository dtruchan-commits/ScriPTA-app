"""
Database utility functions for ScriPTA API.
"""
import json
import logging
import os
import sqlite3
from typing import Dict, List, Optional

from fastapi import HTTPException
from pydantic import ValidationError

from ..models.models import (
    ColorModel,
    ColorSpace,
    LayerConfigResponse,
    LayerConfigSet,
    LayerConfigSetResponse,
    MasterdataConfig,
    SwatchConfig,
    TpmConfig,
    TpmConfigRequest,
)

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "scripta-db.sqlite3")


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
                colorName=row[0],
                colorModel=ColorModel(row[1]),
                colorSpace=ColorSpace(row[2]),
                colorValues=color_values
            )
            swatches.append(swatch)

        return swatches
    finally:
        conn.close()


def update_swatch_in_db(color_name: str, swatch_config: SwatchConfig) -> SwatchConfig:
    """Update an existing swatch configuration in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if swatch exists
        cursor.execute("SELECT id FROM swatches WHERE color_name = ?", (color_name,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Swatch with color name '{color_name}' not found")
        
        # Update the swatch
        color_values_json = json.dumps(swatch_config.color_values)
        cursor.execute("""
            UPDATE swatches
            SET color_name = ?, color_model = ?, color_space = ?, color_values = ?
            WHERE color_name = ?
        """, (
            swatch_config.color_name,
            swatch_config.color_model,
            swatch_config.color_space,
            color_values_json,
            color_name
        ))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Swatch with color name '{color_name}' not found")
        
        return swatch_config
    finally:
        conn.close()


def delete_swatch_from_db(color_name: str) -> bool:
    """Delete a swatch configuration from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM swatches WHERE color_name = ?", (color_name,))
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Swatch with color name '{color_name}' not found")
        
        return True
    finally:
        conn.close()


def create_swatch_in_db(swatch_config: SwatchConfig) -> SwatchConfig:
    """Create a new swatch configuration in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if swatch already exists
        cursor.execute("SELECT id FROM swatches WHERE color_name = ?", (swatch_config.color_name,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail=f"Swatch with color name '{swatch_config.color_name}' already exists")
        
        # Insert the new swatch
        color_values_json = json.dumps(swatch_config.color_values)
        cursor.execute("""
            INSERT INTO swatches (color_name, color_model, color_space, color_values)
            VALUES (?, ?, ?, ?)
        """, (
            swatch_config.color_name,
            swatch_config.color_model,
            swatch_config.color_space,
            color_values_json
        ))
        
        conn.commit()
        return swatch_config
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
        configs_dict: Dict[str, List[LayerConfigResponse]] = {}
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
                    configName=config_name_key,
                    layers=layers
                )
            )

        return response_configs
    finally:
        conn.close()


def create_layer_config_in_db(layer_config_set: LayerConfigSet) -> LayerConfigSet:
    """Create a new layer configuration set in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if config set already exists
        cursor.execute("SELECT id FROM layer_config_sets WHERE config_name = ?", (layer_config_set.config_name,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail=f"Layer config set with name '{layer_config_set.config_name}' already exists")
        
        # Insert the new config set
        cursor.execute("INSERT INTO layer_config_sets (config_name) VALUES (?)", (layer_config_set.config_name,))
        config_set_id = cursor.lastrowid
        
        # Insert the layer configurations
        for layer in layer_config_set.layers:
            cursor.execute("""
                INSERT INTO layer_config (config_set_id, name, locked, print, color)
                VALUES (?, ?, ?, ?, ?)
            """, (
                config_set_id,
                layer.name,
                layer.locked,
                layer.print,
                layer.color
            ))
        
        conn.commit()
        return layer_config_set
    finally:
        conn.close()


def update_layer_config_in_db(config_name: str, layer_config_set: LayerConfigSet) -> LayerConfigSet:
    """Update an existing layer configuration set in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if config set exists
        cursor.execute("SELECT id FROM layer_config_sets WHERE config_name = ?", (config_name,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"Layer config set with name '{config_name}' not found")
        
        config_set_id = result[0]
        
        # Update config set name if changed
        if config_name != layer_config_set.config_name:
            cursor.execute("UPDATE layer_config_sets SET config_name = ? WHERE id = ?",
                           (layer_config_set.config_name, config_set_id))
        
        # Delete existing layer configurations
        cursor.execute("DELETE FROM layer_config WHERE config_set_id = ?", (config_set_id,))
        
        # Insert updated layer configurations
        for layer in layer_config_set.layers:
            cursor.execute("""
                INSERT INTO layer_config (config_set_id, name, locked, print, color)
                VALUES (?, ?, ?, ?, ?)
            """, (
                config_set_id,
                layer.name,
                layer.locked,
                layer.print,
                layer.color
            ))
        
        conn.commit()
        return layer_config_set
    finally:
        conn.close()


def delete_layer_config_from_db(config_name: str) -> bool:
    """Delete a layer configuration set from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if config set exists
        cursor.execute("SELECT id FROM layer_config_sets WHERE config_name = ?", (config_name,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"Layer config set with name '{config_name}' not found")
        
        config_set_id = result[0]
        
        # Delete layer configurations first (due to foreign key constraint)
        cursor.execute("DELETE FROM layer_config WHERE config_set_id = ?", (config_set_id,))
        
        # Delete config set
        cursor.execute("DELETE FROM layer_config_sets WHERE id = ?", (config_set_id,))
        
        conn.commit()
        return True
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
                    TPM=row[1],
                    drawDieline=row[2],
                    drawCombination=row[3],
                    A=row[4],
                    B=row[5],
                    H=row[6],
                    variant=row[7],
                    version=row[8],
                    variablesList=row[9],
                    createdBy=row[10],
                    createdAt=row[11],
                    modifiedBy=row[12],
                    modifiedAt=row[13],
                    packType=row[14],
                    description=row[15],
                    comment=row[16],
                    panelList=row[17],
                    createdTimestamp=row[18],
                    updatedTimestamp=row[19]
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


def create_tpm_in_db(tpm_data: TpmConfigRequest) -> TpmConfig:
    """Create a new TPM record in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO tpm (
                TPM, drawDieline, drawCombination, A, B, H, variant, version,
                variablesList, createdBy, createdAt, modifiedBy, modifiedAt,
                packType, description, comment, panelList, created_timestamp, updated_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        
        cursor.execute(query, (
            tpm_data.tpm,
            tpm_data.draw_dieline,
            tpm_data.draw_combination,
            tpm_data.a,
            tpm_data.b,
            tpm_data.h,
            tpm_data.variant,
            tpm_data.version,
            tpm_data.variables_list,
            tpm_data.created_by,
            tpm_data.created_at,
            tpm_data.modified_by,
            tpm_data.modified_at,
            tpm_data.pack_type,
            tpm_data.description,
            tpm_data.comment,
            tpm_data.panel_list
        ))
        
        tpm_id = cursor.lastrowid
        conn.commit()
        
        # Fetch the created record to return it
        cursor.execute("""
            SELECT id, TPM, drawDieline, drawCombination, A, B, H, variant,
                   version, variablesList, createdBy, createdAt, modifiedBy,
                   modifiedAt, packType, description, comment, panelList,
                   created_timestamp, updated_timestamp
            FROM tpm WHERE id = ?
        """, (tpm_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to retrieve created TPM record")
        
        return TpmConfig(
            id=row[0],
            TPM=row[1],
            drawDieline=row[2],
            drawCombination=row[3],
            A=row[4],
            B=row[5],
            H=row[6],
            variant=row[7],
            version=row[8],
            variablesList=row[9],
            createdBy=row[10],
            createdAt=row[11],
            modifiedBy=row[12],
            modifiedAt=row[13],
            packType=row[14],
            description=row[15],
            comment=row[16],
            panelList=row[17],
            createdTimestamp=row[18],
            updatedTimestamp=row[19]
        )
        
    except sqlite3.IntegrityError as e:
        logging.error(f"Database integrity error creating TPM: {e}")
        raise HTTPException(status_code=400, detail=f"Database constraint violation: {str(e)}")
    except Exception as e:
        logging.error(f"Error creating TPM in database: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


def update_tpm_in_db(tpm_id: int, tpm_data: TpmConfigRequest) -> TpmConfig:
    """Update an existing TPM record in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # First check if the record exists
        cursor.execute("SELECT id FROM tpm WHERE id = ?", (tpm_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"TPM with id {tpm_id} not found")
        
        query = """
            UPDATE tpm SET
                TPM = ?, drawDieline = ?, drawCombination = ?, A = ?, B = ?, H = ?,
                variant = ?, version = ?, variablesList = ?, createdBy = ?,
                createdAt = ?, modifiedBy = ?, modifiedAt = ?, packType = ?,
                description = ?, comment = ?, panelList = ?, updated_timestamp = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        
        cursor.execute(query, (
            tpm_data.tpm,
            tpm_data.draw_dieline,
            tpm_data.draw_combination,
            tpm_data.a,
            tpm_data.b,
            tpm_data.h,
            tpm_data.variant,
            tpm_data.version,
            tpm_data.variables_list,
            tpm_data.created_by,
            tpm_data.created_at,
            tpm_data.modified_by,
            tpm_data.modified_at,
            tpm_data.pack_type,
            tpm_data.description,
            tpm_data.comment,
            tpm_data.panel_list,
            tpm_id
        ))
        
        conn.commit()
        
        # Fetch the updated record to return it
        cursor.execute("""
            SELECT id, TPM, drawDieline, drawCombination, A, B, H, variant,
                   version, variablesList, createdBy, createdAt, modifiedBy,
                   modifiedAt, packType, description, comment, panelList,
                   created_timestamp, updated_timestamp
            FROM tpm WHERE id = ?
        """, (tpm_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to retrieve updated TPM record")
        
        return TpmConfig(
            id=row[0],
            TPM=row[1],
            drawDieline=row[2],
            drawCombination=row[3],
            A=row[4],
            B=row[5],
            H=row[6],
            variant=row[7],
            version=row[8],
            variablesList=row[9],
            createdBy=row[10],
            createdAt=row[11],
            modifiedBy=row[12],
            modifiedAt=row[13],
            packType=row[14],
            description=row[15],
            comment=row[16],
            panelList=row[17],
            createdTimestamp=row[18],
            updatedTimestamp=row[19]
        )
        
    except HTTPException:
        raise
    except sqlite3.IntegrityError as e:
        logging.error(f"Database integrity error updating TPM: {e}")
        raise HTTPException(status_code=400, detail=f"Database constraint violation: {str(e)}")
    except Exception as e:
        logging.error(f"Error updating TPM in database: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


def delete_tpm_from_db(tpm_id: int) -> bool:
    """Delete a TPM record from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # First check if the record exists
        cursor.execute("SELECT id FROM tpm WHERE id = ?", (tpm_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"TPM with id {tpm_id} not found")
        
        cursor.execute("DELETE FROM tpm WHERE id = ?", (tpm_id,))
        conn.commit()
        
        return cursor.rowcount > 0
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting TPM from database: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


def get_tpm_by_id_from_db(tpm_id: int) -> Optional[TpmConfig]:
    """Retrieve a specific TPM configuration by ID from the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        query = """
            SELECT id, TPM, drawDieline, drawCombination, A, B, H, variant,
                   version, variablesList, createdBy, createdAt, modifiedBy,
                   modifiedAt, packType, description, comment, panelList,
                   created_timestamp, updated_timestamp
            FROM tpm
            WHERE id = ?
        """
        cursor.execute(query, (tpm_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        try:
            return TpmConfig(
                id=row[0],
                TPM=row[1],
                drawDieline=row[2],
                drawCombination=row[3],
                A=row[4],
                B=row[5],
                H=row[6],
                variant=row[7],
                version=row[8],
                variablesList=row[9],
                createdBy=row[10],
                createdAt=row[11],
                modifiedBy=row[12],
                modifiedAt=row[13],
                packType=row[14],
                description=row[15],
                comment=row[16],
                panelList=row[17],
                createdTimestamp=row[18],
                updatedTimestamp=row[19]
            )
        except ValidationError as e:
            logging.error(f"Validation error for TPM record {row[0]} ('{row[1]}'): {e}")
            raise HTTPException(status_code=422, detail=f"Data validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving TPM by ID from database: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


def get_masterdata_from_db(matnr8: Optional[int] = None) -> List:
    """Retrieve masterdata from the sqlite database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        if matnr8:
            query = """
                SELECT MATNR, MATNR8, MATERIAL_DESCRIPTION, MATERIAL_TYPE, XPLANT_STATUS,
                       MAKEUP, PLANTS, PLANTS_TXT, PRINCIPLE_TRADENAME,
                       CONTRACT_MANUFACTURER_CODETYPE, CONTRACT_MANUFACTURER_CODE,
                       RESPONSIBLE_FOR_SPECIFICATION, CONTRACT_MANUFACTURER_MATERIAL,
                       LAYOUT_APPROVED, USAGE_PREFIX, NUMBER_OF_PAGES, ACF_FLAG,
                       VISIBLE_MARKINGS, CODE, COLORS, NUMBER_COLORS_FRONT,
                       CONTRACT_MANUFACTURER, ARTICLE_CODETYPE, ARTICLE_CODE,
                       CONTRACT_MAN_VISIBLE_MARKINGS, CONTRACT_MANUFACTURER_MT_INDEX,
                       COMPONENT_SCRAB_KEY, REMARKS, PRINTED, NUMBER_COLORS_BACK,
                       PRINT_CHARACTERISTICS, BRAILLE_TEXT, PRINTCHAR_BRAILLE,
                       PRINTCHAR_FOILSTAMP, PRINTCHAR_VARNISH, PRINTCHAR_CRYPTOGLYPH,
                       PRINTCHAR_PSEUDOCRYPTOGLYPH, PRINTCHAR_PEAK, PRINTCHAR_EMBOSSING,
                       PRINTCHAR_COINREACTIVEINK, PRINTCHAR_IRIODINLACQUER,
                       PRINTCHAR_UVLACQUER, PRINTCHAR_PERLMUTTLACQUER,
                       PRINTCHAR_RICHPALEGOLD, PRINTCHAR_SILVERHOTFOIL,
                       PRINTCHAR_UNVARNISH, PRINTCHAR_SECURITYVARISH,
                       PRINTCHAR_MATTVARNISH, PRINTCHAR_CODINGBYSUPPLIER,
                       PRINTCHAR_BKLOGO, PRINTCHAR_S_DR, DRA_COMBINATION,
                       DRA_COMBINATION_DKTXTUC, DRA_DIELINE, DRA_DIELINE_DKTXTUC,
                       DRA_OTHER, DRA_OTHER_DKTXTUC, DRA_ALL, DRA_ALL_DKTXTUC,
                       DRA_1, DRA_2, DRA_3, DRA_4, DRA_5, DRA_6, DRA_7, DRA_8,
                       DRA_9, DRA_10, LRA, LRA_VERSION, LRA_DATE, LRA_FILENAME,
                       HRL, HRL_VERSION, HRL_DATE, ACS, ACS_Version, TPM_DRAWING,
                       TPM, TPMTXT, TPM_STATUS, GLPT, GLPTTXT, ECLASS, ECLASSTXT,
                       ECLASS_S, ECLASS_S_TXT
                FROM masterdata
                WHERE MATNR8 = ?
            """
            cursor.execute(query, (matnr8,))
        else:
            query = """
                SELECT MATNR, MATNR8, MATERIAL_DESCRIPTION, MATERIAL_TYPE, XPLANT_STATUS,
                       MAKEUP, PLANTS, PLANTS_TXT, PRINCIPLE_TRADENAME,
                       CONTRACT_MANUFACTURER_CODETYPE, CONTRACT_MANUFACTURER_CODE,
                       RESPONSIBLE_FOR_SPECIFICATION, CONTRACT_MANUFACTURER_MATERIAL,
                       LAYOUT_APPROVED, USAGE_PREFIX, NUMBER_OF_PAGES, ACF_FLAG,
                       VISIBLE_MARKINGS, CODE, COLORS, NUMBER_COLORS_FRONT,
                       CONTRACT_MANUFACTURER, ARTICLE_CODETYPE, ARTICLE_CODE,
                       CONTRACT_MAN_VISIBLE_MARKINGS, CONTRACT_MANUFACTURER_MT_INDEX,
                       COMPONENT_SCRAB_KEY, REMARKS, PRINTED, NUMBER_COLORS_BACK,
                       PRINT_CHARACTERISTICS, BRAILLE_TEXT, PRINTCHAR_BRAILLE,
                       PRINTCHAR_FOILSTAMP, PRINTCHAR_VARNISH, PRINTCHAR_CRYPTOGLYPH,
                       PRINTCHAR_PSEUDOCRYPTOGLYPH, PRINTCHAR_PEAK, PRINTCHAR_EMBOSSING,
                       PRINTCHAR_COINREACTIVEINK, PRINTCHAR_IRIODINLACQUER,
                       PRINTCHAR_UVLACQUER, PRINTCHAR_PERLMUTTLACQUER,
                       PRINTCHAR_RICHPALEGOLD, PRINTCHAR_SILVERHOTFOIL,
                       PRINTCHAR_UNVARNISH, PRINTCHAR_SECURITYVARISH,
                       PRINTCHAR_MATTVARNISH, PRINTCHAR_CODINGBYSUPPLIER,
                       PRINTCHAR_BKLOGO, PRINTCHAR_S_DR, DRA_COMBINATION,
                       DRA_COMBINATION_DKTXTUC, DRA_DIELINE, DRA_DIELINE_DKTXTUC,
                       DRA_OTHER, DRA_OTHER_DKTXTUC, DRA_ALL, DRA_ALL_DKTXTUC,
                       DRA_1, DRA_2, DRA_3, DRA_4, DRA_5, DRA_6, DRA_7, DRA_8,
                       DRA_9, DRA_10, LRA, LRA_VERSION, LRA_DATE, LRA_FILENAME,
                       HRL, HRL_VERSION, HRL_DATE, ACS, ACS_Version, TPM_DRAWING,
                       TPM, TPMTXT, TPM_STATUS, GLPT, GLPTTXT, ECLASS, ECLASSTXT,
                       ECLASS_S, ECLASS_S_TXT
                FROM masterdata
                ORDER BY MATNR8
            """
            cursor.execute(query)

        rows = cursor.fetchall()
        masterdata_list = []

        for row in rows:
            try:
                masterdata = MasterdataConfig(
                    MATNR=row[0],
                    MATNR8=row[1],
                    materialDescription=row[2],
                    materialType=row[3],
                    xplantStatus=row[4],
                    makeup=row[5],
                    plants=row[6],
                    plantsTxt=row[7],
                    principleTradename=row[8],
                    contractManufacturerCodetype=row[9],
                    contractManufacturerCode=row[10],
                    responsibleForSpecification=row[11],
                    contractManufacturerMaterial=row[12],
                    layoutApproved=row[13],
                    usagePrefix=row[14],
                    numberOfPages=row[15],
                    acfFlag=row[16],
                    visibleMarkings=row[17],
                    code=row[18],
                    colors=row[19],
                    numberColorsFront=row[20],
                    contractManufacturer=row[21],
                    articleCodetype=row[22],
                    articleCode=row[23],
                    contractManVisibleMarkings=row[24],
                    contractManufacturerMtIndex=row[25],
                    componentScrabKey=row[26],
                    remarks=row[27],
                    printed=row[28],
                    numberColorsBack=row[29],
                    printCharacteristics=row[30],
                    brailleText=row[31],
                    printcharBraille=row[32],
                    printcharFoilstamp=row[33],
                    printcharVarnish=row[34],
                    printcharCryptoglyph=row[35],
                    printcharPseudocryptoglyph=row[36],
                    printcharPeak=row[37],
                    printcharEmbossing=row[38],
                    printcharCoinreactiveink=row[39],
                    printcharIriodinlacquer=row[40],
                    printcharUvlacquer=row[41],
                    printcharPerlmuttlacquer=row[42],
                    printcharRichpalegold=row[43],
                    printcharSilverhotfoil=row[44],
                    printcharUnvarnish=row[45],
                    printcharSecurityvarish=row[46],
                    printcharMattvarnish=row[47],
                    printcharCodingbysupplier=row[48],
                    printcharBklogo=row[49],
                    printcharSDr=row[50],
                    draCombination=row[51],
                    draCombinationDktxtuc=row[52],
                    draDieline=row[53],
                    draDielineDktxtuc=row[54],
                    draOther=row[55],
                    draOtherDktxtuc=row[56],
                    draAll=row[57],
                    draAllDktxtuc=row[58],
                    dra1=row[59],
                    dra2=row[60],
                    dra3=row[61],
                    dra4=row[62],
                    dra5=row[63],
                    dra6=row[64],
                    dra7=row[65],
                    dra8=row[66],
                    dra9=row[67],
                    dra10=row[68],
                    lra=row[69],
                    lraVersion=row[70],
                    lraDate=row[71],
                    lraFilename=row[72],
                    hrl=row[73],
                    hrlVersion=row[74],
                    hrlDate=row[75],
                    acs=row[76],
                    acsVersion=row[77],
                    tpmDrawing=row[78],
                    tpm=row[79],
                    tpmtxt=row[80],
                    tpmStatus=row[81],
                    glpt=row[82],
                    glpttxt=row[83],
                    eclass=row[84],
                    eclasstxt=row[85],
                    eclassS=row[86],
                    eclassSText=row[87]
                )
                masterdata_list.append(masterdata)
            except ValidationError as e:
                logging.error(f"Validation error for masterdata record {row[1] if row else 'unknown'}: {e}")
                continue
            except Exception as e:
                logging.error(f"Unexpected error processing masterdata record {row[1] if row else 'unknown'}: {e}")
                continue

        return masterdata_list
    finally:
        conn.close()


def create_masterdata_databricks_table():
    """Create the masterdata_databricks table in SQLite if it doesn't exist."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Drop existing table to recreate with correct schema
        cursor.execute("DROP TABLE IF EXISTS masterdata_databricks")
        
        create_table_sql = """
        CREATE TABLE masterdata_databricks (
            MATNR TEXT PRIMARY KEY,
            MATNR8 INTEGER,
            MATERIAL_DESCRIPTION TEXT,
            MATERIAL_TYPE TEXT,
            XPLANT_STATUS TEXT,
            PRDHATXT TEXT,
            MAKEUP TEXT,
            PLANTS TEXT,
            PLANTS_TXT TEXT,
            CONTRACT_MANUFACTURER_CODETYPE TEXT,
            CONTRACT_MANUFACTURER_CODE TEXT,
            RESPONSIBLE_FOR_SPECIFICATION TEXT,
            CONTRACT_MANUFACTURER_MATERIAL TEXT,
            LAYOUT_APPROVED TEXT,
            USAGE_PREFIX TEXT,
            NUMBER_OF_PAGES TEXT,
            ACF_FLAG TEXT,
            VISIBLE_MARKINGS TEXT,
            CODE TEXT,
            COLORS TEXT,
            NUMBER_COLORS_FRONT TEXT,
            CONTRACT_MANUFACTURER TEXT,
            ARTICLE_CODETYPE TEXT,
            ARTICLE_CODE TEXT,
            CONTRACT_MAN_VISIBLE_MARKINGS TEXT,
            CONTRACT_MANUFACTURER_MT_INDEX TEXT,
            COMPONENT_SCRAB_KEY TEXT,
            REMARKS TEXT,
            PRINTED TEXT,
            NUMBER_COLORS_BACK TEXT,
            PRINT_CHARACTERISTICS TEXT,
            BRAILLE_TEXT TEXT,
            PRINTCHAR_BRAILLE TEXT,
            PRINTCHAR_FOILSTAMP TEXT,
            PRINTCHAR_GOLDHOTFOIL TEXT,
            PRINTCHAR_EMBOSSDEBOSS TEXT,
            PRINTCHAR_SPOTVARNISH TEXT,
            PRINTCHAR_SCRATCHOFF TEXT,
            PRINTCHAR_LAMINATION TEXT,
            PRINTCHAR_DIECUT TEXT,
            PRINTCHAR_PERFORATION TEXT,
            PRINTCHAR_GLOSSVARNISH TEXT,
            PRINTCHAR_LEAFLETING TEXT,
            PRINTCHAR_FOLDING TEXT,
            PRINTCHAR_RICHPALEGOLD TEXT,
            PRINTCHAR_SILVERHOTFOIL TEXT,
            PRINTCHAR_UNVARNISH TEXT,
            PRINTCHAR_SECURITYVARISH TEXT,
            PRINTCHAR_MATTVARNISH TEXT,
            PRINTCHAR_CODINGBYSUPPLIER TEXT,
            PRINTCHAR_BKLOGO TEXT,
            PRINTCHAR_S_DR TEXT,
            DRA_COMBINATION TEXT,
            DRA_COMBINATION_DKTXTUC TEXT,
            DRA_DIELINE TEXT,
            DRA_DIELINE_DKTXTUC TEXT,
            DRA_OTHER TEXT,
            DRA_OTHER_DKTXTUC TEXT,
            DRA_ALL TEXT,
            DRA_ALL_DKTXTUC TEXT,
            DRA_1 TEXT,
            DRA_2 TEXT,
            DRA_3 TEXT,
            DRA_4 TEXT,
            DRA_5 TEXT,
            DRA_6 TEXT,
            DRA_7 TEXT,
            DRA_8 TEXT,
            DRA_9 TEXT,
            DRA_10 TEXT,
            LRA TEXT,
            LRA_VERSION TEXT,
            LRA_DATE TEXT,
            LRA_FILENAME TEXT,
            HRL TEXT,
            HRL_VERSION TEXT,
            HRL_DATE TEXT,
            ACS TEXT,
            ACS_VERSION TEXT,
            TPM_DRAWING TEXT,
            TPM TEXT,
            TPMTXT TEXT,
            TPM_STATUS TEXT,
            GLPT TEXT,
            GLPTTXT TEXT,
            ECLASS TEXT,
            ECLASSTXT TEXT,
            ECLASS_S TEXT,
            ECLASS_S_TXT TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_sql)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_masterdata_databricks_matnr8 ON masterdata_databricks (MATNR8)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_masterdata_databricks_matnr ON masterdata_databricks (MATNR)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_masterdata_databricks_material_type ON masterdata_databricks (MATERIAL_TYPE)")
        
        conn.commit()
        logging.info("masterdata_databricks table created successfully with updated schema")
        
    except Exception as e:
        logging.error(f"Failed to create masterdata_databricks table: {str(e)}")
        raise
    finally:
        conn.close()


def save_masterdata_to_sqlite(masterdata_records: List[Dict]) -> int:
    """Save masterdata records to the SQLite database."""
    if not masterdata_records:
        return 0
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM masterdata_databricks")
        
        # Prepare insert statement - using the first record to determine columns
        first_record = masterdata_records[0]
        columns = list(first_record.keys())
        placeholders = ','.join(['?' for _ in columns])
        insert_sql = f"INSERT OR REPLACE INTO masterdata_databricks ({','.join(columns)}) VALUES ({placeholders})"
        
        # Convert records to tuples
        record_tuples = []
        for record in masterdata_records:
            tuple_data = tuple(record.get(col) for col in columns)
            record_tuples.append(tuple_data)
        
        # Bulk insert
        cursor.executemany(insert_sql, record_tuples)
        
        # Update the updated_at timestamp for all records
        cursor.execute("UPDATE masterdata_databricks SET updated_at = CURRENT_TIMESTAMP")
        
        conn.commit()
        
        rows_saved = len(record_tuples)
        logging.info(f"Saved {rows_saved} masterdata records to SQLite database")
        
        return rows_saved
        
    except Exception as e:
        logging.error(f"Failed to save masterdata to SQLite: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


def get_masterdata_databricks_stats():
    """Get statistics about the masterdata_databricks table."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='masterdata_databricks'
        """)
        
        if not cursor.fetchone():
            return {
                "table_exists": False,
                "record_count": 0,
                "last_updated": None
            }
        
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM masterdata_databricks")
        count = cursor.fetchone()[0]
        
        # Get last updated timestamp
        cursor.execute("SELECT MAX(updated_at) FROM masterdata_databricks")
        last_updated = cursor.fetchone()[0]
        
        return {
            "table_exists": True,
            "record_count": count,
            "last_updated": last_updated
        }
        
    except Exception as e:
        logging.error(f"Failed to get masterdata_databricks stats: {str(e)}")
        return {
            "table_exists": False,
            "record_count": 0,
            "last_updated": None,
            "error": str(e)
        }
    finally:
        conn.close()
