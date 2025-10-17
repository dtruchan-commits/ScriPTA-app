"""
Masterdata configuration endpoints for the ScriPTA API.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from ..cache import cache_manager
from ..models.models import MasterdataConfig, MasterdataConfigResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Masterdata"])


def _convert_dict_to_masterdata_config(data_dict: dict) -> MasterdataConfig:
    """Convert a dictionary to MasterdataConfig model."""
    try:
        return MasterdataConfig(
            MATNR=data_dict.get('MATNR'),
            MATNR8=data_dict.get('MATNR8'),
            materialDescription=data_dict.get('MATERIAL_DESCRIPTION'),
            materialType=data_dict.get('MATERIAL_TYPE'),
            xplantStatus=data_dict.get('XPLANT_STATUS'),
            prdhatxt=data_dict.get('PRDHATXT'),
            makeup=data_dict.get('MAKEUP'),
            plants=data_dict.get('PLANTS'),
            plantsTxt=data_dict.get('PLANTS_TXT'),
            principleTradename=data_dict.get('PRINCIPLE_TRADENAME'),
            contractManufacturerCodetype=data_dict.get('CONTRACT_MANUFACTURER_CODETYPE'),
            contractManufacturerCode=data_dict.get('CONTRACT_MANUFACTURER_CODE'),
            responsibleForSpecification=data_dict.get('RESPONSIBLE_FOR_SPECIFICATION'),
            contractManufacturerMaterial=data_dict.get('CONTRACT_MANUFACTURER_MATERIAL'),
            layoutApproved=data_dict.get('LAYOUT_APPROVED'),
            usagePrefix=data_dict.get('USAGE_PREFIX'),
            numberOfPages=data_dict.get('NUMBER_OF_PAGES'),
            acfFlag=data_dict.get('ACF_FLAG'),
            visibleMarkings=data_dict.get('VISIBLE_MARKINGS'),
            code=data_dict.get('CODE'),
            colors=data_dict.get('COLORS'),
            numberColorsFront=data_dict.get('NUMBER_COLORS_FRONT'),
            contractManufacturer=data_dict.get('CONTRACT_MANUFACTURER'),
            articleCodetype=data_dict.get('ARTICLE_CODETYPE'),
            articleCode=data_dict.get('ARTICLE_CODE'),
            contractManVisibleMarkings=data_dict.get('CONTRACT_MAN_VISIBLE_MARKINGS'),
            contractManufacturerMtIndex=data_dict.get('CONTRACT_MANUFACTURER_MT_INDEX'),
            componentScrabKey=data_dict.get('COMPONENT_SCRAB_KEY'),
            remarks=data_dict.get('REMARKS'),
            printed=data_dict.get('PRINTED'),
            numberColorsBack=data_dict.get('NUMBER_COLORS_BACK'),
            printCharacteristics=data_dict.get('PRINT_CHARACTERISTICS'),
            brailleText=data_dict.get('BRAILLE_TEXT'),
            printcharBraille=data_dict.get('PRINTCHAR_BRAILLE'),
            printcharFoilstamp=data_dict.get('PRINTCHAR_FOILSTAMP'),
            printcharVarnish=data_dict.get('PRINTCHAR_VARNISH'),
            printcharCryptoglyph=data_dict.get('PRINTCHAR_CRYPTOGLYPH'),
            printcharPseudocryptoglyph=data_dict.get('PRINTCHAR_PSEUDOCRYPTOGLYPH'),
            printcharPeak=data_dict.get('PRINTCHAR_PEAK'),
            printcharEmbossing=data_dict.get('PRINTCHAR_EMBOSSING'),
            printcharCoinreactiveink=data_dict.get('PRINTCHAR_COINREACTIVEINK'),
            printcharIriodinlacquer=data_dict.get('PRINTCHAR_IRIODINLACQUER'),
            printcharUvlacquer=data_dict.get('PRINTCHAR_UVLACQUER'),
            printcharPerlmuttlacquer=data_dict.get('PRINTCHAR_PERLMUTTLACQUER'),
            printcharRichpalegold=data_dict.get('PRINTCHAR_RICHPALEGOLD'),
            printcharSilverhotfoil=data_dict.get('PRINTCHAR_SILVERHOTFOIL'),
            printcharUnvarnish=data_dict.get('PRINTCHAR_UNVARNISH'),
            printcharSecurityvarish=data_dict.get('PRINTCHAR_SECURITYVARISH'),
            printcharMattvarnish=data_dict.get('PRINTCHAR_MATTVARNISH'),
            printcharCodingbysupplier=data_dict.get('PRINTCHAR_CODINGBYSUPPLIER'),
            printcharBklogo=data_dict.get('PRINTCHAR_BKLOGO'),
            printcharSDr=data_dict.get('PRINTCHAR_S_DR'),
            draCombination=data_dict.get('DRA_COMBINATION'),
            draCombinationDktxtuc=data_dict.get('DRA_COMBINATION_DKTXTUC'),
            draDieline=data_dict.get('DRA_DIELINE'),
            draDielineDktxtuc=data_dict.get('DRA_DIELINE_DKTXTUC'),
            draOther=data_dict.get('DRA_OTHER'),
            draOtherDktxtuc=data_dict.get('DRA_OTHER_DKTXTUC'),
            draAll=data_dict.get('DRA_ALL'),
            draAllDktxtuc=data_dict.get('DRA_ALL_DKTXTUC'),
            dra1=data_dict.get('DRA_1'),
            dra2=data_dict.get('DRA_2'),
            dra3=data_dict.get('DRA_3'),
            dra4=data_dict.get('DRA_4'),
            dra5=data_dict.get('DRA_5'),
            dra6=data_dict.get('DRA_6'),
            dra7=data_dict.get('DRA_7'),
            dra8=data_dict.get('DRA_8'),
            dra9=data_dict.get('DRA_9'),
            dra10=data_dict.get('DRA_10'),
            lra=data_dict.get('LRA'),
            lraVersion=data_dict.get('LRA_VERSION'),
            lraDate=data_dict.get('LRA_DATE'),
            lraFilename=data_dict.get('LRA_FILENAME'),
            hrl=data_dict.get('HRL'),
            hrlVersion=data_dict.get('HRL_VERSION'),
            hrlDate=data_dict.get('HRL_DATE'),
            acs=data_dict.get('ACS'),
            acsVersion=data_dict.get('ACS_Version'),
            tpmDrawing=data_dict.get('TPM_DRAWING'),
            tpm=data_dict.get('TPM'),
            tpmtxt=data_dict.get('TPMTXT'),
            tpmStatus=data_dict.get('TPM_STATUS'),
            glpt=data_dict.get('GLPT'),
            glpttxt=data_dict.get('GLPTTXT'),
            eclass=data_dict.get('ECLASS'),
            eclasstxt=data_dict.get('ECLASSTXT'),
            eclassS=data_dict.get('ECLASS_S'),
            eclassSText=data_dict.get('ECLASS_S_TXT')
        )
    except ValidationError as e:
        logger.error(f"Validation error converting dict to MasterdataConfig: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error converting dict to MasterdataConfig: {e}")
        raise


@router.get("/get_masterdata_from_sqlite", response_model=MasterdataConfigResponse)
async def get_masterdata_from_sqlite(matnr8: Optional[int] = Query(None, description="Filter by MATNR8", alias="matnr8")) -> MasterdataConfigResponse:
    """
    Get masterdata configuration from in-memory cache, optionally filtered by MATNR8.
    
    This endpoint uses the ultra-fast in-memory SQLite cache for instantaneous responses.

    Args:
        matnr8: Optional MATNR8 (8-digit material number) to filter results (e.g., 91967086)

    Returns masterdata configuration including all material information.
    """
    try:
        if matnr8:
            # Get specific masterdata record from cache
            cache_result = cache_manager.get_masterdata_by_matnr8(matnr8)
            
            if not cache_result:
                raise HTTPException(status_code=404, detail=f"MATNR8 '{matnr8}' not found in cache")
            
            # Convert to MasterdataConfig model
            masterdata_config = _convert_dict_to_masterdata_config(cache_result)
            masterdata = [masterdata_config]
            
        else:
            # Get all masterdata from cache (limit to 1000 for performance)
            cache_results = cache_manager.get_all_masterdata(limit=1000)
            
            if not cache_results:
                # Cache is empty, return empty list
                masterdata = []
            else:
                # Convert all records to MasterdataConfig models
                masterdata = []
                for cache_result in cache_results:
                    try:
                        masterdata_config = _convert_dict_to_masterdata_config(cache_result)
                        masterdata.append(masterdata_config)
                    except Exception as e:
                        logger.error(f"Error converting record MATNR8 {cache_result.get('MATNR8', 'unknown')}: {e}")
                        continue

        return MasterdataConfigResponse(masterdata=masterdata)
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        logger.error(f"Error getting masterdata from cache: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving masterdata from cache: {str(e)}"
        )


@router.get("/cache_stats")
async def get_cache_stats():
    """Get statistics about the in-memory masterdata cache."""
    try:
        stats = cache_manager.get_cache_stats()
        return {
            "success": True,
            "cache_stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "cache_stats": {"initialized": False, "record_count": 0}
        }