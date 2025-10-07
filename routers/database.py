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

from models.models import (
    ColorModel,
    ColorSpace,
    LayerConfigResponse,
    LayerConfigSetResponse,
    MasterdataConfig,
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
                colorName=row[0],
                colorModel=ColorModel(row[1]),
                colorSpace=ColorSpace(row[2]),
                colorValues=color_values
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


def get_masterdata_from_db(matnr8: Optional[int] = None) -> List:
    """Retrieve masterdata from the database."""
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
