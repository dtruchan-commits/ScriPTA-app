from models import SwatchConfig, ColorModel, ColorSpace
from typing import List


SWATCH_DATA = [
    SwatchConfig(
        color_name="DIELINE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values="0,50,100,0"
    ),
    SwatchConfig(
        color_name="PA123",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values="50,50,50,50"
    ),
    SwatchConfig(
        color_name="PA321",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values="40,40,40,40"
    )
]
