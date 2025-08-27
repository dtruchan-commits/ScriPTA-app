from dataclasses import dataclass
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ConfigDict

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
    
    color_name: str = Field(..., alias="colorName")
    color_model: ColorModel
    color_space: ColorSpace
    color_values: str = Field(..., alias="colorValues")


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
