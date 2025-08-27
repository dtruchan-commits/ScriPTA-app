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

# Models
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
