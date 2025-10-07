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


class TPMConfigResponse(BaseModel):
    tpms: List[TpmConfig]
