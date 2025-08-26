from enum import Enum
from typing import List
from pydantic import BaseModel


class ColorModel(str, Enum):
    SPOT = "SPOT"
    PROCESS = "PROCESS"


class ColorSpace(str, Enum):
    CMYK = "CMYK"
    RGB = "RGB"
    LAB = "LAB"


class SwatchConfig(BaseModel):
    colorname: str
    color_model: ColorModel
    color_space: ColorSpace
    colorvalues: str

    class Config:
        # Allow use of enum values in JSON serialization
        use_enum_values = True


class SwatchConfigResponse(BaseModel):
    swatches: List[SwatchConfig]
