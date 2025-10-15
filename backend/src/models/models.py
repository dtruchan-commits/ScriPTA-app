from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# Enums
class ColorModel(str, Enum):
    SPOT = "SPOT"
    PROCESS = "PROCESS"


class ColorSpace(str, Enum):
    CMYK = "CMYK"
    RGB = "RGB"
    LAB = "LAB"


class LayerName(str, Enum):
    DIELINE = "DIELINE"
    TECHNICAL = "TECHNICAL"
    BRAILLE_EMB = "BRAILLE_EMB"
    TEXT = "TEXT"
    ACF_HRL = "ACF_HRL"
    ACF_LRA_VARNISH = "ACF_LRA_VARNISH"
    DESIGN = "DESIGN"
    INFOBOX = "INFOBOX"
    GUIDES = "GUIDES"
    PANEL = "PANEL"


class LayerColor(str, Enum):
    GOLD = "GOLD"
    TEAL = "TEAL"
    FIESTA = "FIESTA"
    LIGHT_BLUE = "LIGHT_BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    RED = "RED"
    LAVENDER = "LAVENDER"
    GRAY = "GRAY"
    BLUE = "BLUE"


@dataclass
class LayerConfig:
    name: LayerName
    locked: bool
    print: bool
    color: LayerColor


@dataclass
class LayerConfigSet:
    config_name: str
    layers: List[LayerConfig]


class SwatchConfig(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    color_name: str = Field(..., alias="colorName", description="Name of the color")
    color_model: ColorModel = Field(..., alias="colorModel", description="Color model: SPOT or PROCESS")
    color_space: ColorSpace = Field(..., alias="colorSpace", description="Color space: CMYK, RGB, or LAB(maybe)")
    color_values: List[int] = Field(..., alias="colorValues", description="Color values as an array of integers")


class SwatchConfigResponse(BaseModel):
    swatches: List[SwatchConfig]


class LayerConfigResponse(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    name: str
    locked: bool
    print: bool
    color: str


class LayerConfigSetResponse(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    config_name: str = Field(..., alias="configName")
    layers: List[LayerConfigResponse]


class TpmConfig(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    id: int
    tpm: str = Field(..., alias="TPM", description="TPM name")
    draw_dieline: Optional[str] = Field(None, alias="drawDieline", description="Draw dieline value")
    draw_combination: Optional[str] = Field(None, alias="drawCombination", description="Draw combination value")
    a: Optional[int] = Field(None, alias="A", description="Dimension A")
    b: Optional[int] = Field(None, alias="B", description="Dimension B")
    h: Optional[int] = Field(None, alias="H", description="Dimension H")
    variant: Optional[str] = Field(None, description="Variant name")
    version: int = Field(1, description="Version number")
    variables_list: Optional[str] = Field(None, alias="variablesList", description="Variables list")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by user")
    created_at: Optional[str] = Field(None, alias="createdAt", description="Creation date")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by user")
    modified_at: Optional[str] = Field(None, alias="modifiedAt", description="Modification date")
    pack_type: Optional[str] = Field(None, alias="packType", description="Pack type")
    description: Optional[str] = Field(None, description="Description")
    comment: Optional[str] = Field(None, description="Comment")
    panel_list: Optional[str] = Field(None, alias="panelList", description="Panel list as JSON string")
    created_timestamp: Optional[str] = Field(None, alias="createdTimestamp", description="Created timestamp")
    updated_timestamp: Optional[str] = Field(None, alias="updatedTimestamp", description="Updated timestamp")


class TpmConfigRequest(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    tpm: str = Field(..., alias="TPM", description="TPM name")
    draw_dieline: Optional[str] = Field(None, alias="drawDieline", description="Draw dieline value")
    draw_combination: Optional[str] = Field(None, alias="drawCombination", description="Draw combination value")
    a: Optional[int] = Field(None, alias="A", description="Dimension A")
    b: Optional[int] = Field(None, alias="B", description="Dimension B")
    h: Optional[int] = Field(None, alias="H", description="Dimension H")
    variant: Optional[str] = Field(None, description="Variant name")
    version: int = Field(1, description="Version number")
    variables_list: Optional[str] = Field(None, alias="variablesList", description="Variables list")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Created by user")
    created_at: Optional[str] = Field(None, alias="createdAt", description="Creation date")
    modified_by: Optional[str] = Field(None, alias="modifiedBy", description="Modified by user")
    modified_at: Optional[str] = Field(None, alias="modifiedAt", description="Modification date")
    pack_type: Optional[str] = Field(None, alias="packType", description="Pack type")
    description: Optional[str] = Field(None, description="Description")
    comment: Optional[str] = Field(None, description="Comment")
    panel_list: Optional[str] = Field(None, alias="panelList", description="Panel list as JSON string")


class TpmConfigResponse(BaseModel):
    tpms: List[TpmConfig]


class MasterdataConfig(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )

    matnr: Optional[int] = Field(None, alias="MATNR", description="Material number")
    matnr8: Optional[int] = Field(None, alias="MATNR8", description="8-digit material number")
    material_description: Optional[str] = Field(None, alias="materialDescription", description="Material description")
    material_type: Optional[str] = Field(None, alias="materialType", description="Material type")
    xplant_status: Optional[int] = Field(None, alias="xplantStatus", description="Cross-plant status")
    makeup: Optional[str] = Field(None, alias="makeup", description="Makeup")
    plants: Optional[str] = Field(None, alias="plants", description="Plants")
    plants_txt: Optional[str] = Field(None, alias="plantsTxt", description="Plants text")
    principle_tradename: Optional[str] = Field(None, alias="principleTradename", description="Principle tradename")
    contract_manufacturer_codetype: Optional[float] = Field(None, alias="contractManufacturerCodetype", description="Contract manufacturer codetype")
    contract_manufacturer_code: Optional[float] = Field(None, alias="contractManufacturerCode", description="Contract manufacturer code")
    responsible_for_specification: Optional[str] = Field(None, alias="responsibleForSpecification", description="Responsible for specification")
    contract_manufacturer_material: Optional[str] = Field(None, alias="contractManufacturerMaterial", description="Contract manufacturer material")
    layout_approved: Optional[str] = Field(None, alias="layoutApproved", description="Layout approved")
    usage_prefix: Optional[str] = Field(None, alias="usagePrefix", description="Usage prefix")
    number_of_pages: Optional[str] = Field(None, alias="numberOfPages", description="Number of pages")
    acf_flag: Optional[str] = Field(None, alias="acfFlag", description="ACF flag")
    visible_markings: Optional[float] = Field(None, alias="visibleMarkings", description="Visible markings")
    code: Optional[float] = Field(None, alias="code", description="Code")
    colors: Optional[str] = Field(None, alias="colors", description="Colors")
    number_colors_front: Optional[float] = Field(None, alias="numberColorsFront", description="Number of colors front")
    contract_manufacturer: Optional[float] = Field(None, alias="contractManufacturer", description="Contract manufacturer")
    article_codetype: Optional[float] = Field(None, alias="articleCodetype", description="Article codetype")
    article_code: Optional[str] = Field(None, alias="articleCode", description="Article code")
    contract_man_visible_markings: Optional[float] = Field(None, alias="contractManVisibleMarkings", description="Contract man visible markings")
    contract_manufacturer_mt_index: Optional[float] = Field(None, alias="contractManufacturerMtIndex", description="Contract manufacturer MT index")
    component_scrab_key: Optional[float] = Field(None, alias="componentScrabKey", description="Component scrab key")
    remarks: Optional[float] = Field(None, alias="remarks", description="Remarks")
    printed: Optional[str] = Field(None, alias="printed", description="Printed")
    number_colors_back: Optional[float] = Field(None, alias="numberColorsBack", description="Number of colors back")
    print_characteristics: Optional[str] = Field(None, alias="printCharacteristics", description="Print characteristics")
    braille_text: Optional[float] = Field(None, alias="brailleText", description="Braille text")
    printchar_braille: Optional[str] = Field(None, alias="printcharBraille", description="Print char braille")
    printchar_foilstamp: Optional[str] = Field(None, alias="printcharFoilstamp", description="Print char foilstamp")
    printchar_varnish: Optional[str] = Field(None, alias="printcharVarnish", description="Print char varnish")
    printchar_cryptoglyph: Optional[str] = Field(None, alias="printcharCryptoglyph", description="Print char cryptoglyph")
    printchar_pseudocryptoglyph: Optional[str] = Field(None, alias="printcharPseudocryptoglyph", description="Print char pseudocryptoglyph")
    printchar_peak: Optional[str] = Field(None, alias="printcharPeak", description="Print char peak")
    printchar_embossing: Optional[str] = Field(None, alias="printcharEmbossing", description="Print char embossing")
    printchar_coinreactiveink: Optional[str] = Field(None, alias="printcharCoinreactiveink", description="Print char coinreactiveink")
    printchar_iriodinlacquer: Optional[str] = Field(None, alias="printcharIriodinlacquer", description="Print char iriodinlacquer")
    printchar_uvlacquer: Optional[str] = Field(None, alias="printcharUvlacquer", description="Print char UV lacquer")
    printchar_perlmuttlacquer: Optional[str] = Field(None, alias="printcharPerlmuttlacquer", description="Print char perlmuttlacquer")
    printchar_richpalegold: Optional[str] = Field(None, alias="printcharRichpalegold", description="Print char rich pale gold")
    printchar_silverhotfoil: Optional[str] = Field(None, alias="printcharSilverhotfoil", description="Print char silver hot foil")
    printchar_unvarnish: Optional[str] = Field(None, alias="printcharUnvarnish", description="Print char unvarnish")
    printchar_securityvarish: Optional[str] = Field(None, alias="printcharSecurityvarish", description="Print char security varish")
    printchar_mattvarnish: Optional[str] = Field(None, alias="printcharMattvarnish", description="Print char matt varnish")
    printchar_codingbysupplier: Optional[str] = Field(None, alias="printcharCodingbysupplier", description="Print char coding by supplier")
    printchar_bklogo: Optional[str] = Field(None, alias="printcharBklogo", description="Print char BK logo")
    printchar_s_dr: Optional[str] = Field(None, alias="printcharSDr", description="Print char S DR")
    dra_combination: Optional[str] = Field(None, alias="draCombination", description="DRA combination")
    dra_combination_dktxtuc: Optional[str] = Field(None, alias="draCombinationDktxtuc", description="DRA combination DKTXTUC")
    dra_dieline: Optional[str] = Field(None, alias="draDieline", description="DRA dieline")
    dra_dieline_dktxtuc: Optional[str] = Field(None, alias="draDielineDktxtuc", description="DRA dieline DKTXTUC")
    dra_other: Optional[str] = Field(None, alias="draOther", description="DRA other")
    dra_other_dktxtuc: Optional[str] = Field(None, alias="draOtherDktxtuc", description="DRA other DKTXTUC")
    dra_all: Optional[str] = Field(None, alias="draAll", description="DRA all")
    dra_all_dktxtuc: Optional[str] = Field(None, alias="draAllDktxtuc", description="DRA all DKTXTUC")
    dra_1: Optional[str] = Field(None, alias="dra1", description="DRA 1")
    dra_2: Optional[str] = Field(None, alias="dra2", description="DRA 2")
    dra_3: Optional[str] = Field(None, alias="dra3", description="DRA 3")
    dra_4: Optional[str] = Field(None, alias="dra4", description="DRA 4")
    dra_5: Optional[str] = Field(None, alias="dra5", description="DRA 5")
    dra_6: Optional[str] = Field(None, alias="dra6", description="DRA 6")
    dra_7: Optional[str] = Field(None, alias="dra7", description="DRA 7")
    dra_8: Optional[float] = Field(None, alias="dra8", description="DRA 8")
    dra_9: Optional[float] = Field(None, alias="dra9", description="DRA 9")
    dra_10: Optional[float] = Field(None, alias="dra10", description="DRA 10")
    lra: Optional[str] = Field(None, alias="lra", description="LRA")
    lra_version: Optional[float] = Field(None, alias="lraVersion", description="LRA version")
    lra_date: Optional[str] = Field(None, alias="lraDate", description="LRA date")
    lra_filename: Optional[str] = Field(None, alias="lraFilename", description="LRA filename")
    hrl: Optional[str] = Field(None, alias="hrl", description="HRL")
    hrl_version: Optional[float] = Field(None, alias="hrlVersion", description="HRL version")
    hrl_date: Optional[str] = Field(None, alias="hrlDate", description="HRL date")
    acs: Optional[str] = Field(None, alias="acs", description="ACS")
    acs_version: Optional[float] = Field(None, alias="acsVersion", description="ACS version")
    tpm_drawing: Optional[float] = Field(None, alias="tpmDrawing", description="TPM drawing")
    tpm: Optional[str] = Field(None, alias="tpm", description="TPM")
    tpmtxt: Optional[str] = Field(None, alias="tpmtxt", description="TPM text")
    tpm_status: Optional[int] = Field(None, alias="tpmStatus", description="TPM status")
    glpt: Optional[str] = Field(None, alias="glpt", description="GLPT")
    glpttxt: Optional[str] = Field(None, alias="glpttxt", description="GLPT text")
    eclass: Optional[int] = Field(None, alias="eclass", description="ECLASS")
    eclasstxt: Optional[str] = Field(None, alias="eclasstxt", description="ECLASS text")
    eclass_s: Optional[int] = Field(None, alias="eclassS", description="ECLASS S")
    eclass_s_txt: Optional[str] = Field(None, alias="eclassSText", description="ECLASS S text")


class MasterdataConfigResponse(BaseModel):
    masterdata: List[MasterdataConfig]
