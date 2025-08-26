from models import SwatchConfig, ColorModel, ColorSpace
from typing import List


def get_hardcoded_swatches() -> List[SwatchConfig]:
    """
    Returns hardcoded swatch configuration data.
    
    Returns:
        List[SwatchConfig]: List of swatch configurations
    """
    return [
        SwatchConfig(
            colorname="DIELINE",
            color_model=ColorModel.SPOT,
            color_space=ColorSpace.CMYK,
            colorvalues="0,50,100,0"
        ),
        SwatchConfig(
            colorname="PA123",
            color_model=ColorModel.SPOT,
            color_space=ColorSpace.CMYK,
            colorvalues="50,50,50,50"
        ),
        SwatchConfig(
            colorname="PA321",
            color_model=ColorModel.PROCESS,
            color_space=ColorSpace.CMYK,
            colorvalues="40,40,40,40"
        )
    ]


SWATCH_DATA = [
    SwatchConfig(
        colorname="DIELINE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        colorvalues="0,50,100,0"
    ),
    SwatchConfig(
        colorname="PA123",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        colorvalues="50,50,50,50"
    ),
    SwatchConfig(
        colorname="PA321",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        colorvalues="40,40,40,40"
    )
]
