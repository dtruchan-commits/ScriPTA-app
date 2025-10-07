from typing import List

from ..models.models import ColorModel, ColorSpace, SwatchConfig

SWATCH_DATA = [
    SwatchConfig(
        color_name="DIELINE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[50, 50, 0, 0]
    ),
    SwatchConfig(
        color_name="C20M90Y0K40",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[20, 90, 0, 40]
    ),
    SwatchConfig(
        color_name="PROC699",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 7, 0]
    ),
    SwatchConfig(
        color_name="PROCBLACK",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 100]
    ),
    SwatchConfig(
        color_name="PROCCYAN",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="PROCMAGENTA",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PROCYELLOW",
        color_model=ColorModel.PROCESS,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="369C_BLUEFOIL",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="3M_FOIL",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 91, 7, 32]
    ),
    SwatchConfig(
        color_name="BLACK_VARCODE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 100]
    ),
    SwatchConfig(
        color_name="BRAILLE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="CODING_BY_SUPPLIER",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 50, 0, 0]
    ),
    SwatchConfig(
        color_name="DIECUT",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[50, 50, 0, 0]
    ),
    SwatchConfig(
        color_name="EMBOSSING",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[70, 0, 70, 0]
    ),
    SwatchConfig(
        color_name="GOLDFOIL425",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="GUIDE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 85]
    ),
    SwatchConfig(
        color_name="LAFAMME_GOLD",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[41, 48, 80, 8]
    ),
    SwatchConfig(
        color_name="LUMI",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[20, 33, 0, 0]
    ),
    SwatchConfig(
        color_name="NOT_PRINTABLE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PA012",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 51, 0]
    ),
    SwatchConfig(
        color_name="PA021",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 51, 87, 0]
    ),
    SwatchConfig(
        color_name="PA032",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 90, 90, 10]
    ),
    SwatchConfig(
        color_name="PA072",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 79, 0, 0]
    ),
    SwatchConfig(
        color_name="PA100",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 51, 0]
    ),
    SwatchConfig(
        color_name="PA101",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 79, 0]
    ),
    SwatchConfig(
        color_name="PA102",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PA103",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 18]
    ),
    SwatchConfig(
        color_name="PA104",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 30]
    ),
    SwatchConfig(
        color_name="PA105",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 51]
    ),
    SwatchConfig(
        color_name="PA106",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 72, 0]
    ),
    SwatchConfig(
        color_name="PA107",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 79, 0]
    ),
    SwatchConfig(
        color_name="PA108",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PA109",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 94, 0]
    ),
    SwatchConfig(
        color_name="PA110",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 94, 6]
    ),
    SwatchConfig(
        color_name="PA111",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 100, 27]
    ),
    SwatchConfig(
        color_name="PA113",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 7, 66, 0]
    ),
    SwatchConfig(
        color_name="PA114",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 6, 72, 0]
    ),
    SwatchConfig(
        color_name="PA115",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 79, 0]
    ),
    SwatchConfig(
        color_name="PA116",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 94, 0]
    ),
    SwatchConfig(
        color_name="PA117",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 100, 15]
    ),
    SwatchConfig(
        color_name="PA119",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 100, 51]
    ),
    SwatchConfig(
        color_name="PA120",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 58, 0]
    ),
    SwatchConfig(
        color_name="PA1205",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 5, 31, 0]
    ),
    SwatchConfig(
        color_name="PA121",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 69, 0]
    ),
    SwatchConfig(
        color_name="PA1215",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 45, 0]
    ),
    SwatchConfig(
        color_name="PA122",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 17, 80, 0]
    ),
    SwatchConfig(
        color_name="PA1225",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 17, 62, 0]
    ),
    SwatchConfig(
        color_name="PA123",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 24, 94, 0]
    ),
    SwatchConfig(
        color_name="PA1235",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 29, 91, 0]
    ),
    SwatchConfig(
        color_name="PA124",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 28, 100, 6]
    ),
    SwatchConfig(
        color_name="PA1245",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 28, 100, 18]
    ),
    SwatchConfig(
        color_name="PA127",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 7, 50, 0]
    ),
    SwatchConfig(
        color_name="PA128",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 65, 0]
    ),
    SwatchConfig(
        color_name="PA129",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 16, 77, 0]
    ),
    SwatchConfig(
        color_name="PA130",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 100, 0]
    ),
    SwatchConfig(
        color_name="PA131",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 100, 0]
    ),
    SwatchConfig(
        color_name="PA134",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 45, 0]
    ),
    SwatchConfig(
        color_name="PA135",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 72, 0]
    ),
    SwatchConfig(
        color_name="PA1355",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 20, 56, 0]
    ),
    SwatchConfig(
        color_name="PA136",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 76, 0]
    ),
    SwatchConfig(
        color_name="PA1365",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 29, 72, 0]
    ),
    SwatchConfig(
        color_name="PA137",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[5, 35, 90, 0]
    ),
    SwatchConfig(
        color_name="PA1375",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 40, 90, 0]
    ),
    SwatchConfig(
        color_name="PA138",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 42, 100, 1]
    ),
    SwatchConfig(
        color_name="PA141",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 47, 0]
    ),
    SwatchConfig(
        color_name="PA142",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 23, 76, 0]
    ),
    SwatchConfig(
        color_name="PA143",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 83, 0]
    ),
    SwatchConfig(
        color_name="PA144",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 48, 100, 0]
    ),
    SwatchConfig(
        color_name="PA145",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 47, 100, 8]
    ),
    SwatchConfig(
        color_name="PA146",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 38, 100, 34]
    ),
    SwatchConfig(
        color_name="PA148",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 16, 37, 0]
    ),
    SwatchConfig(
        color_name="PA1485",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 54, 0]
    ),
    SwatchConfig(
        color_name="PA149",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 23, 47, 0]
    ),
    SwatchConfig(
        color_name="PA1495",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 33, 67, 0]
    ),
    SwatchConfig(
        color_name="PA150",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 35, 70, 0]
    ),
    SwatchConfig(
        color_name="PA1505",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 42, 77, 0]
    ),
    SwatchConfig(
        color_name="PA151",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 48, 95, 0]
    ),
    SwatchConfig(
        color_name="PA152",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 51, 100, 0]
    ),
    SwatchConfig(
        color_name="PA1535",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 87, 15]
    ),
    SwatchConfig(
        color_name="PA154",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 43, 100, 34]
    ),
    SwatchConfig(
        color_name="PA155",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[2, 9, 20, 0]
    ),
    SwatchConfig(
        color_name="PA1555",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 34, 0]
    ),
    SwatchConfig(
        color_name="PA156",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 43, 0]
    ),
    SwatchConfig(
        color_name="PA1565",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 34, 51, 0]
    ),
    SwatchConfig(
        color_name="PA157",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 38, 76, 0]
    ),
    SwatchConfig(
        color_name="PA1575",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 45, 72, 0]
    ),
    SwatchConfig(
        color_name="PA158",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 87, 0]
    ),
    SwatchConfig(
        color_name="PA1585",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 87, 0]
    ),
    SwatchConfig(
        color_name="PA159",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 87, 10]
    ),
    SwatchConfig(
        color_name="PA1595",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 69, 100, 4]
    ),
    SwatchConfig(
        color_name="PA160",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 55, 65, 15]
    ),
    SwatchConfig(
        color_name="PA162",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 18, 0]
    ),
    SwatchConfig(
        color_name="PA1625",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 31, 38, 0]
    ),
    SwatchConfig(
        color_name="PA163",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 47, 0]
    ),
    SwatchConfig(
        color_name="PA1635",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 39, 48, 0]
    ),
    SwatchConfig(
        color_name="PA164",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 47, 76, 0]
    ),
    SwatchConfig(
        color_name="PA165",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 60, 100, 0]
    ),
    SwatchConfig(
        color_name="PA1655",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 65, 87, 0]
    ),
    SwatchConfig(
        color_name="PA166",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 65, 100, 0]
    ),
    SwatchConfig(
        color_name="PA1665",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 65, 87, 0]
    ),
    SwatchConfig(
        color_name="PA167",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 60, 100, 18]
    ),
    SwatchConfig(
        color_name="PA1675",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 67, 100, 28]
    ),
    SwatchConfig(
        color_name="PA1685",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 69, 100, 43]
    ),
    SwatchConfig(
        color_name="PA169",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 18, 0]
    ),
    SwatchConfig(
        color_name="PA170",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 38, 47, 0]
    ),
    SwatchConfig(
        color_name="PA171",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 53, 68, 0]
    ),
    SwatchConfig(
        color_name="PA172",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 66, 68, 0]
    ),
    SwatchConfig(
        color_name="PA173",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 69, 100, 4]
    ),
    SwatchConfig(
        color_name="PA174",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 70, 100, 36]
    ),
    SwatchConfig(
        color_name="PA1765",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 38, 21, 0]
    ),
    SwatchConfig(
        color_name="PA1767",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 11, 0]
    ),
    SwatchConfig(
        color_name="PA1775",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 47, 29, 0]
    ),
    SwatchConfig(
        color_name="PA1777",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 58, 36, 0]
    ),
    SwatchConfig(
        color_name="PA178",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 59, 56, 0]
    ),
    SwatchConfig(
        color_name="PA1785",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 67, 50, 0]
    ),
    SwatchConfig(
        color_name="PA1787",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 76, 60, 0]
    ),
    SwatchConfig(
        color_name="PA1788",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 84, 88, 0]
    ),
    SwatchConfig(
        color_name="PA179",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 79, 100, 0]
    ),
    SwatchConfig(
        color_name="PA1795",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 94, 100, 0]
    ),
    SwatchConfig(
        color_name="PA180",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 79, 100, 11]
    ),
    SwatchConfig(
        color_name="PA1815",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 90, 100, 51]
    ),
    SwatchConfig(
        color_name="PA183",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 46, 21, 0]
    ),
    SwatchConfig(
        color_name="PA184",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 73, 32, 0]
    ),
    SwatchConfig(
        color_name="PA185",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 91, 76, 0]
    ),
    SwatchConfig(
        color_name="PA186",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 81, 4]
    ),
    SwatchConfig(
        color_name="PA187",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 79, 20]
    ),
    SwatchConfig(
        color_name="PA1895",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 28, 7, 0]
    ),
    SwatchConfig(
        color_name="PA190",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 55, 22, 0]
    ),
    SwatchConfig(
        color_name="PA1905",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 41, 9, 0]
    ),
    SwatchConfig(
        color_name="PA191",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 76, 38, 0]
    ),
    SwatchConfig(
        color_name="PA1915",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 71, 20, 0]
    ),
    SwatchConfig(
        color_name="PA192",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 68, 0]
    ),
    SwatchConfig(
        color_name="PA1925",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 94, 51, 0]
    ),
    SwatchConfig(
        color_name="PA1935",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 60, 6]
    ),
    SwatchConfig(
        color_name="PA1945",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 55, 19]
    ),
    SwatchConfig(
        color_name="PA196",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 25, 4, 0]
    ),
    SwatchConfig(
        color_name="PA197",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 47, 11, 0]
    ),
    SwatchConfig(
        color_name="PA198",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 78, 33, 0]
    ),
    SwatchConfig(
        color_name="PA199",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 62, 0]
    ),
    SwatchConfig(
        color_name="PA200",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 63, 12]
    ),
    SwatchConfig(
        color_name="PA201",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 63, 29]
    ),
    SwatchConfig(
        color_name="PA2013",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 39, 100, 0]
    ),
    SwatchConfig(
        color_name="PA202",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 65, 47]
    ),
    SwatchConfig(
        color_name="PA203",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 34, 3, 0]
    ),
    SwatchConfig(
        color_name="PA204",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 58, 3, 0]
    ),
    SwatchConfig(
        color_name="PA205",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 84, 9, 0]
    ),
    SwatchConfig(
        color_name="PA206",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 38, 3]
    ),
    SwatchConfig(
        color_name="PA207",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 43, 19]
    ),
    SwatchConfig(
        color_name="PA208",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 36, 37]
    ),
    SwatchConfig(
        color_name="PA210",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 39, 6, 0]
    ),
    SwatchConfig(
        color_name="PA211",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 55, 8, 0]
    ),
    SwatchConfig(
        color_name="PA2118",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[58, 55, 0, 53]
    ),
    SwatchConfig(
        color_name="PA2119",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[58, 55, 0, 60]
    ),
    SwatchConfig(
        color_name="PA212",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 72, 11, 0]
    ),
    SwatchConfig(
        color_name="PA213",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 95, 27, 0]
    ),
    SwatchConfig(
        color_name="PA2131",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[74, 52, 0, 26]
    ),
    SwatchConfig(
        color_name="PA214",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 34, 8]
    ),
    SwatchConfig(
        color_name="PA216",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 95, 40, 49]
    ),
    SwatchConfig(
        color_name="PA217",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 28, 0, 0]
    ),
    SwatchConfig(
        color_name="PA218",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[2, 61, 0, 0]
    ),
    SwatchConfig(
        color_name="PA219",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[1, 89, 0, 0]
    ),
    SwatchConfig(
        color_name="PA220",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 13, 17]
    ),
    SwatchConfig(
        color_name="PA221",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 15, 30]
    ),
    SwatchConfig(
        color_name="PA223",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 46, 0, 0]
    ),
    SwatchConfig(
        color_name="PA224",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[1, 63, 0, 0]
    ),
    SwatchConfig(
        color_name="PA225",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[1, 83, 0, 0]
    ),
    SwatchConfig(
        color_name="PA226",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PA227",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 7, 19]
    ),
    SwatchConfig(
        color_name="PA228",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 94, 0, 43]
    ),
    SwatchConfig(
        color_name="PA2295",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 9, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2298",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[33, 0, 72, 0]
    ),
    SwatchConfig(
        color_name="PA230",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 34, 0, 0]
    ),
    SwatchConfig(
        color_name="PA231",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[1, 52, 0, 0]
    ),
    SwatchConfig(
        color_name="PA232",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[8, 84, 0, 0]
    ),
    SwatchConfig(
        color_name="PA233",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2335",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[70, 65, 73, 27]
    ),
    SwatchConfig(
        color_name="PA2348",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 63, 66, 8]
    ),
    SwatchConfig(
        color_name="PA235",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 100, 0, 43]
    ),
    SwatchConfig(
        color_name="PA236",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[1, 30, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2365",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[2, 27, 0, 0]
    ),
    SwatchConfig(
        color_name="PA237",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[7, 35, 0, 0]
    ),
    SwatchConfig(
        color_name="PA239",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 79, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2395",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 95, 0, 0]
    ),
    SwatchConfig(
        color_name="PA240",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 94, 0, 0]
    ),
    SwatchConfig(
        color_name="PA241",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 100, 0, 2]
    ),
    SwatchConfig(
        color_name="PA2415",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[35, 100, 0, 6]
    ),
    SwatchConfig(
        color_name="PA242",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 94, 0, 51]
    ),
    SwatchConfig(
        color_name="PA2425",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[37, 100, 0, 26]
    ),
    SwatchConfig(
        color_name="PA243",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[5, 29, 0, 0]
    ),
    SwatchConfig(
        color_name="PA245",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 60, 0, 0]
    ),
    SwatchConfig(
        color_name="PA248",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 94, 0, 15]
    ),
    SwatchConfig(
        color_name="PA250",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 18, 0, 0]
    ),
    SwatchConfig(
        color_name="PA251",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[13, 39, 0, 0]
    ),
    SwatchConfig(
        color_name="PA252",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[24, 56, 0, 0]
    ),
    SwatchConfig(
        color_name="PA254",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[51, 94, 0, 0]
    ),
    SwatchConfig(
        color_name="PA255",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[51, 100, 0, 25]
    ),
    SwatchConfig(
        color_name="PA256",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[7, 20, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2562",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[19, 35, 0, 0]
    ),
    SwatchConfig(
        color_name="PA257",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[14, 34, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2572",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 47, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2573",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 43, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2577",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 45, 0, 2]
    ),
    SwatchConfig(
        color_name="PA258",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 76, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2582",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[47, 65, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2583",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[46, 63, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2587",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[59, 66, 0, 0]
    ),
    SwatchConfig(
        color_name="PA259",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 100, 1, 5]
    ),
    SwatchConfig(
        color_name="PA2592",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[60, 90, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2597",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[87, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2602",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[63, 100, 0, 3]
    ),
    SwatchConfig(
        color_name="PA2603",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 100, 0, 2]
    ),
    SwatchConfig(
        color_name="PA2607",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[81, 100, 0, 7]
    ),
    SwatchConfig(
        color_name="PA261",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[48, 100, 0, 40]
    ),
    SwatchConfig(
        color_name="PA2612",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[64, 100, 0, 14]
    ),
    SwatchConfig(
        color_name="PA262",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 94, 0, 65]
    ),
    SwatchConfig(
        color_name="PA2622",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[58, 100, 0, 44]
    ),
    SwatchConfig(
        color_name="PA2623",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[59, 100, 0, 32]
    ),
    SwatchConfig(
        color_name="PA263",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[10, 14, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2635",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[28, 27, 0, 0]
    ),
    SwatchConfig(
        color_name="PA264",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[26, 28, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2645",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 36, 0, 0]
    ),
    SwatchConfig(
        color_name="PA265",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[54, 56, 0, 0]
    ),
    SwatchConfig(
        color_name="PA266",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[94, 94, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2665",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[79, 76, 0, 0]
    ),
    SwatchConfig(
        color_name="PA267",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[89, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PA270",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[31, 27, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2705",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 30, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2706",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[19, 9, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2707",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[17, 6, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2708",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[26, 10, 0, 0]
    ),
    SwatchConfig(
        color_name="PA271",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 37, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2716",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[45, 29, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2717",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[29, 12, 0, 0]
    ),
    SwatchConfig(
        color_name="PA272",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[58, 48, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2725",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[79, 69, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2726",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[79, 66, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2727",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[71, 42, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2728",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[96, 69, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2736",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[94, 91, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2738",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 87, 0, 2]
    ),
    SwatchConfig(
        color_name="PA274",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 100, 0, 28]
    ),
    SwatchConfig(
        color_name="PA2745",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 95, 0, 15]
    ),
    SwatchConfig(
        color_name="PA2747",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 86, 0, 15]
    ),
    SwatchConfig(
        color_name="PA275",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[98, 100, 0, 43]
    ),
    SwatchConfig(
        color_name="PA2755",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 97, 0, 30]
    ),
    SwatchConfig(
        color_name="PA2756",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 94, 0, 29]
    ),
    SwatchConfig(
        color_name="PA2757",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 82, 0, 30]
    ),
    SwatchConfig(
        color_name="PA2758",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 91, 7, 32]
    ),
    SwatchConfig(
        color_name="PA2766",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 87, 0, 58]
    ),
    SwatchConfig(
        color_name="PA277",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 7, 0, 0]
    ),
    SwatchConfig(
        color_name="PA278",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[19, 14, 0, 0]
    ),
    SwatchConfig(
        color_name="PA279",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[68, 34, 0, 0]
    ),
    SwatchConfig(
        color_name="PA280",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 72, 0, 18]
    ),
    SwatchConfig(
        color_name="PA281",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 72, 0, 38]
    ),
    SwatchConfig(
        color_name="PA283",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[34, 6, 0, 0]
    ),
    SwatchConfig(
        color_name="PA284",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[56, 18, 0, 0]
    ),
    SwatchConfig(
        color_name="PA285",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[85, 26, 0, 0]
    ),
    SwatchConfig(
        color_name="PA286",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 66, 0, 2]
    ),
    SwatchConfig(
        color_name="PA287",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 69, 0, 11]
    ),
    SwatchConfig(
        color_name="PA288",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 65, 0, 30]
    ),
    SwatchConfig(
        color_name="PA289",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 89, 0, 88]
    ),
    SwatchConfig(
        color_name="PA290",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 6, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2905",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 6, 0, 0]
    ),
    SwatchConfig(
        color_name="PA291",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[47, 11, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2915",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[65, 9, 0, 0]
    ),
    SwatchConfig(
        color_name="PA292",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[72, 27, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2925",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[87, 23, 0, 0]
    ),
    SwatchConfig(
        color_name="PA293",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 56, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2935",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 47, 0, 0]
    ),
    SwatchConfig(
        color_name="PA294",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 56, 0, 18]
    ),
    SwatchConfig(
        color_name="PA295",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 56, 0, 34]
    ),
    SwatchConfig(
        color_name="PA297",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[51, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2975",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 0, 5, 0]
    ),
    SwatchConfig(
        color_name="PA298",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 7, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2985",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[72, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="PA299",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[87, 18, 0, 0]
    ),
    SwatchConfig(
        color_name="PA2995",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 9, 0, 0]
    ),
    SwatchConfig(
        color_name="PA300",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 43, 0, 0]
    ),
    SwatchConfig(
        color_name="PA3005",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 30, 0, 6]
    ),
    SwatchConfig(
        color_name="PA301",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 45, 0, 18]
    ),
    SwatchConfig(
        color_name="PA3015",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 23, 0, 18]
    ),
    SwatchConfig(
        color_name="PA302",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 20, 0, 55]
    ),
    SwatchConfig(
        color_name="PA303",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 0, 76]
    ),
    SwatchConfig(
        color_name="PA304",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 0, 8, 0]
    ),
    SwatchConfig(
        color_name="PA305",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[35, 5, 10, 0]
    ),
    SwatchConfig(
        color_name="PA306",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[76, 0, 6, 0]
    ),
    SwatchConfig(
        color_name="PA307",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 6, 0, 34]
    ),
    SwatchConfig(
        color_name="PA308",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 5, 0, 47]
    ),
    SwatchConfig(
        color_name="PA310",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 9, 0]
    ),
    SwatchConfig(
        color_name="PA3105",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 12, 0]
    ),
    SwatchConfig(
        color_name="PA311",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 10, 0]
    ),
    SwatchConfig(
        color_name="PA3115",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[65, 0, 18, 0]
    ),
    SwatchConfig(
        color_name="PA312",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 15, 0]
    ),
    SwatchConfig(
        color_name="PA3125",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[83, 0, 21, 0]
    ),
    SwatchConfig(
        color_name="PA313",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 6, 18]
    ),
    SwatchConfig(
        color_name="PA3135",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 9, 5, 6]
    ),
    SwatchConfig(
        color_name="PA314",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 9, 34]
    ),
    SwatchConfig(
        color_name="PA315",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 15, 47]
    ),
    SwatchConfig(
        color_name="PA3165",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 9, 5, 40]
    ),
    SwatchConfig(
        color_name="PA317",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 9, 0]
    ),
    SwatchConfig(
        color_name="PA318",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 0, 15, 0]
    ),
    SwatchConfig(
        color_name="PA319",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[51, 0, 18, 0]
    ),
    SwatchConfig(
        color_name="PA320",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 31, 7]
    ),
    SwatchConfig(
        color_name="PA321",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[95, 20, 25, 20]
    ),
    SwatchConfig(
        color_name="PA324",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 0, 11, 0]
    ),
    SwatchConfig(
        color_name="PA3242",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 0, 18, 0]
    ),
    SwatchConfig(
        color_name="PA3245",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[34, 0, 18, 0]
    ),
    SwatchConfig(
        color_name="PA3248",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 23, 0]
    ),
    SwatchConfig(
        color_name="PA325",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[60, 0, 27, 0]
    ),
    SwatchConfig(
        color_name="PA3255",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[47, 0, 30, 0]
    ),
    SwatchConfig(
        color_name="PA3258",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[59, 0, 33, 0]
    ),
    SwatchConfig(
        color_name="PA326",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[94, 0, 43, 0]
    ),
    SwatchConfig(
        color_name="PA3265",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 0, 37, 0]
    ),
    SwatchConfig(
        color_name="PA3268",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[90, 0, 49, 0]
    ),
    SwatchConfig(
        color_name="PA327",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 47, 15]
    ),
    SwatchConfig(
        color_name="PA3272",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 46, 0]
    ),
    SwatchConfig(
        color_name="PA3275",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[95, 0, 47, 0]
    ),
    SwatchConfig(
        color_name="PA3278",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 55, 5]
    ),
    SwatchConfig(
        color_name="PA328",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 45, 32]
    ),
    SwatchConfig(
        color_name="PA3282",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 46, 15]
    ),
    SwatchConfig(
        color_name="PA3285",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 50, 7]
    ),
    SwatchConfig(
        color_name="PA329",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 47, 47]
    ),
    SwatchConfig(
        color_name="PA3292",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 49, 46]
    ),
    SwatchConfig(
        color_name="PA3295",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 53, 21]
    ),
    SwatchConfig(
        color_name="PA3298",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 57, 42]
    ),
    SwatchConfig(
        color_name="PA3305",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 60, 51]
    ),
    SwatchConfig(
        color_name="PA331",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 15, 0]
    ),
    SwatchConfig(
        color_name="PA332",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 0, 20, 0]
    ),
    SwatchConfig(
        color_name="PA335",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 65, 30]
    ),
    SwatchConfig(
        color_name="PA336",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 67, 47]
    ),
    SwatchConfig(
        color_name="PA337",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[31, 0, 20, 0]
    ),
    SwatchConfig(
        color_name="PA3375",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[51, 0, 33, 0]
    ),
    SwatchConfig(
        color_name="PA338",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[47, 0, 32, 0]
    ),
    SwatchConfig(
        color_name="PA339",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[89, 0, 56, 0]
    ),
    SwatchConfig(
        color_name="PA3395",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[61, 0, 45, 0]
    ),
    SwatchConfig(
        color_name="PA340",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 66, 9]
    ),
    SwatchConfig(
        color_name="PA3405",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[83, 0, 65, 0]
    ),
    SwatchConfig(
        color_name="PA341",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 67, 29]
    ),
    SwatchConfig(
        color_name="PA342",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 71, 43]
    ),
    SwatchConfig(
        color_name="PA3425",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 78, 42]
    ),
    SwatchConfig(
        color_name="PA3435",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 79, 60]
    ),
    SwatchConfig(
        color_name="PA344",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 0, 23, 0]
    ),
    SwatchConfig(
        color_name="PA345",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 0, 32, 0]
    ),
    SwatchConfig(
        color_name="PA346",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[55, 0, 47, 0]
    ),
    SwatchConfig(
        color_name="PA347",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 86, 3]
    ),
    SwatchConfig(
        color_name="PA348",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 84, 25]
    ),
    SwatchConfig(
        color_name="PA349",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 91, 42]
    ),
    SwatchConfig(
        color_name="PA351",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[17, 0, 16, 0]
    ),
    SwatchConfig(
        color_name="PA352",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 0, 25, 0]
    ),
    SwatchConfig(
        color_name="PA353",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 0, 36, 0]
    ),
    SwatchConfig(
        color_name="PA354",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[91, 0, 83, 0]
    ),
    SwatchConfig(
        color_name="PA355",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[94, 0, 100, 6]
    ),
    SwatchConfig(
        color_name="PA356",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[70, 0, 70, 30]
    ),
    SwatchConfig(
        color_name="PA357",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 100, 70]
    ),
    SwatchConfig(
        color_name="PA358",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 0, 38, 0]
    ),
    SwatchConfig(
        color_name="PA359",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[36, 0, 49, 0]
    ),
    SwatchConfig(
        color_name="PA3597",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 83, 0, 28]
    ),
    SwatchConfig(
        color_name="PA360",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[48, 0, 80, 0]
    ),
    SwatchConfig(
        color_name="PA361",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[60, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PA362",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[70, 0, 100, 9]
    ),
    SwatchConfig(
        color_name="PA363",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[68, 0, 100, 24]
    ),
    SwatchConfig(
        color_name="PA364",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[65, 0, 100, 42]
    ),
    SwatchConfig(
        color_name="PA365",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[12, 0, 29, 0]
    ),
    SwatchConfig(
        color_name="PA366",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 47, 0]
    ),
    SwatchConfig(
        color_name="PA367",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[32, 0, 59, 0]
    ),
    SwatchConfig(
        color_name="PA368",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[57, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PA369",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[59, 0, 100, 7]
    ),
    SwatchConfig(
        color_name="PA370",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 100, 27]
    ),
    SwatchConfig(
        color_name="PA372",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[10, 0, 33, 0]
    ),
    SwatchConfig(
        color_name="PA374",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[24, 0, 57, 0]
    ),
    SwatchConfig(
        color_name="PA375",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[41, 0, 78, 0]
    ),
    SwatchConfig(
        color_name="PA376",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[52, 0, 100, 5]
    ),
    SwatchConfig(
        color_name="PA377",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[45, 0, 100, 24]
    ),
    SwatchConfig(
        color_name="PA379",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 0, 58, 0]
    ),
    SwatchConfig(
        color_name="PA381",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 91, 0]
    ),
    SwatchConfig(
        color_name="PA382",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 0, 94, 0]
    ),
    SwatchConfig(
        color_name="PA385",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 87, 56]
    ),
    SwatchConfig(
        color_name="PA386",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 56, 0]
    ),
    SwatchConfig(
        color_name="PA387",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[10, 0, 74, 0]
    ),
    SwatchConfig(
        color_name="PA388",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[14, 0, 79, 0]
    ),
    SwatchConfig(
        color_name="PA389",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[20, 0, 85, 0]
    ),
    SwatchConfig(
        color_name="PA390",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[22, 0, 100, 8]
    ),
    SwatchConfig(
        color_name="PA3945",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[3, 0, 85, 0]
    ),
    SwatchConfig(
        color_name="PA395",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[8, 0, 85, 0]
    ),
    SwatchConfig(
        color_name="PA3955",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PA3975",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 29]
    ),
    SwatchConfig(
        color_name="PA3985",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 3, 100, 41]
    ),
    SwatchConfig(
        color_name="PA399",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 0, 100, 43]
    ),
    SwatchConfig(
        color_name="PA3995",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 3, 100, 64]
    ),
    SwatchConfig(
        color_name="PA402",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 6, 15, 34]
    ),
    SwatchConfig(
        color_name="PA408",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 11, 34]
    ),
    SwatchConfig(
        color_name="PA413",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 6, 18]
    ),
    SwatchConfig(
        color_name="PA414",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 9, 30]
    ),
    SwatchConfig(
        color_name="PA416",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 15, 51]
    ),
    SwatchConfig(
        color_name="PA420",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 15]
    ),
    SwatchConfig(
        color_name="PA421",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 26]
    ),
    SwatchConfig(
        color_name="PA422",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[5, 0, 0, 33]
    ),
    SwatchConfig(
        color_name="PA423",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 44]
    ),
    SwatchConfig(
        color_name="PA424",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 61]
    ),
    SwatchConfig(
        color_name="PA425",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 79]
    ),
    SwatchConfig(
        color_name="PA427",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 11]
    ),
    SwatchConfig(
        color_name="PA428",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[2, 0, 0, 18]
    ),
    SwatchConfig(
        color_name="PA429",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[3, 0, 0, 32]
    ),
    SwatchConfig(
        color_name="PA430",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 0, 47]
    ),
    SwatchConfig(
        color_name="PA431",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 1, 0, 64]
    ),
    SwatchConfig(
        color_name="PA432",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[23, 0, 0, 79]
    ),
    SwatchConfig(
        color_name="PA442",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 1, 30]
    ),
    SwatchConfig(
        color_name="PA445",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 0, 11, 69]
    ),
    SwatchConfig(
        color_name="PA446",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 15, 79]
    ),
    SwatchConfig(
        color_name="PA468",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 9, 23, 0]
    ),
    SwatchConfig(
        color_name="PA470",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 94, 34]
    ),
    SwatchConfig(
        color_name="PA4705",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 6, 72, 47]
    ),
    SwatchConfig(
        color_name="PA471",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 56, 1, 18]
    ),
    SwatchConfig(
        color_name="PA475",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 18, 0]
    ),
    SwatchConfig(
        color_name="PA476",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[79, 83, 100, 0]
    ),
    SwatchConfig(
        color_name="PA478",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 86, 100, 30]
    ),
    SwatchConfig(
        color_name="PA480",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 27, 30, 0]
    ),
    SwatchConfig(
        color_name="PA483",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 93, 100, 60]
    ),
    SwatchConfig(
        color_name="PA484",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 95, 100, 29]
    ),
    SwatchConfig(
        color_name="PA485",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 91, 0]
    ),
    SwatchConfig(
        color_name="PA486",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 47, 43, 0]
    ),
    SwatchConfig(
        color_name="PA487",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 34, 27, 0]
    ),
    SwatchConfig(
        color_name="PA488",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 18, 0]
    ),
    SwatchConfig(
        color_name="PA489",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 11, 0]
    ),
    SwatchConfig(
        color_name="PA495",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 35, 15, 0]
    ),
    SwatchConfig(
        color_name="PA496",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 6, 0]
    ),
    SwatchConfig(
        color_name="PA4975",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 77, 83, 79]
    ),
    SwatchConfig(
        color_name="PA503",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 8, 0]
    ),
    SwatchConfig(
        color_name="PA5035",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 6, 6]
    ),
    SwatchConfig(
        color_name="PA506",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 91, 79, 0]
    ),
    SwatchConfig(
        color_name="PA508",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 38, 11, 0]
    ),
    SwatchConfig(
        color_name="PA511",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[83, 100, 69, 0]
    ),
    SwatchConfig(
        color_name="PA512",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[60, 91, 27, 0]
    ),
    SwatchConfig(
        color_name="PA5125",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[65, 86, 49, 0]
    ),
    SwatchConfig(
        color_name="PA5145",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[3, 43, 11, 0]
    ),
    SwatchConfig(
        color_name="PA516",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 0, 0]
    ),
    SwatchConfig(
        color_name="PA519",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[76, 94, 38, 0]
    ),
    SwatchConfig(
        color_name="PA520",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 94, 18, 0]
    ),
    SwatchConfig(
        color_name="PA521",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 47, 0, 0]
    ),
    SwatchConfig(
        color_name="PA522",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 38, 0, 0]
    ),
    SwatchConfig(
        color_name="PA5245",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 11, 6, 0]
    ),
    SwatchConfig(
        color_name="PA526",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[79, 94, 11, 0]
    ),
    SwatchConfig(
        color_name="PA528",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 56, 0, 0]
    ),
    SwatchConfig(
        color_name="PA529",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 43, 0, 0]
    ),
    SwatchConfig(
        color_name="PA530",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 30, 0, 0]
    ),
    SwatchConfig(
        color_name="PA531",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 18, 0, 0]
    ),
    SwatchConfig(
        color_name="PA532",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 83, 76, 0]
    ),
    SwatchConfig(
        color_name="PA533",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 79, 47, 0]
    ),
    SwatchConfig(
        color_name="PA536",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 18, 6, 0]
    ),
    SwatchConfig(
        color_name="PA540",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 55, 0, 55]
    ),
    SwatchConfig(
        color_name="PA541",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 57, 0, 18]
    ),
    SwatchConfig(
        color_name="PA542",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[62, 22, 0, 3]
    ),
    SwatchConfig(
        color_name="PA543",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[56, 15, 0, 6]
    ),
    SwatchConfig(
        color_name="PA544",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[38, 9, 0, 30]
    ),
    SwatchConfig(
        color_name="PA5473",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[65, 9, 23, 34]
    ),
    SwatchConfig(
        color_name="PA548",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 18, 0, 65]
    ),
    SwatchConfig(
        color_name="PA5483",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[62, 0, 21, 31]
    ),
    SwatchConfig(
        color_name="PA5487",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[36, 0, 17, 56]
    ),
    SwatchConfig(
        color_name="PA549",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[89, 7, 5, 15]
    ),
    SwatchConfig(
        color_name="PA5493",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[25, 0, 9, 13]
    ),
    SwatchConfig(
        color_name="PA551",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 0, 0, 15]
    ),
    SwatchConfig(
        color_name="PA552",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 0, 0, 9]
    ),
    SwatchConfig(
        color_name="PA5523",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 6, 6]
    ),
    SwatchConfig(
        color_name="PA5555",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 34, 38]
    ),
    SwatchConfig(
        color_name="PA556",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 3, 27]
    ),
    SwatchConfig(
        color_name="PA558",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 15, 0]
    ),
    SwatchConfig(
        color_name="PA563",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 0, 27, 6]
    ),
    SwatchConfig(
        color_name="PA566",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 9, 0]
    ),
    SwatchConfig(
        color_name="PA569",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[94, 40, 45, 13]
    ),
    SwatchConfig(
        color_name="PA573",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[31, 8, 18, 0]
    ),
    SwatchConfig(
        color_name="PA577",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[23, 0, 51, 11]
    ),
    SwatchConfig(
        color_name="PA5773",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 0, 43, 38]
    ),
    SwatchConfig(
        color_name="PA578",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 0, 40, 4]
    ),
    SwatchConfig(
        color_name="PA5787",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 0, 30, 11]
    ),
    SwatchConfig(
        color_name="PA580",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 23, 0]
    ),
    SwatchConfig(
        color_name="PA581",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 94, 69]
    ),
    SwatchConfig(
        color_name="PA5815",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 91, 79]
    ),
    SwatchConfig(
        color_name="PA582",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 100, 43]
    ),
    SwatchConfig(
        color_name="PA584",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 79, 6]
    ),
    SwatchConfig(
        color_name="PA5845",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 1, 47, 30]
    ),
    SwatchConfig(
        color_name="PA585",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 0, 65, 0]
    ),
    SwatchConfig(
        color_name="PA586",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 0, 51, 0]
    ),
    SwatchConfig(
        color_name="PA587",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[8, 5, 45, 0]
    ),
    SwatchConfig(
        color_name="PA600",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 11, 0]
    ),
    SwatchConfig(
        color_name="PA6017",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 42, 71, 2]
    ),
    SwatchConfig(
        color_name="PA615",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 27, 6]
    ),
    SwatchConfig(
        color_name="PA624",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[47, 0, 38, 18]
    ),
    SwatchConfig(
        color_name="PA628",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[15, 0, 6, 0]
    ),
    SwatchConfig(
        color_name="PA633",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[98, 6, 10, 29]
    ),
    SwatchConfig(
        color_name="PA634",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[95, 7, 4, 30]
    ),
    SwatchConfig(
        color_name="PA640",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 3, 6]
    ),
    SwatchConfig(
        color_name="PA642",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 0, 0, 6]
    ),
    SwatchConfig(
        color_name="PA650",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[30, 11, 0, 0]
    ),
    SwatchConfig(
        color_name="PA651",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[43, 18, 0, 6]
    ),
    SwatchConfig(
        color_name="PA656",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[20, 8, 6, 0]
    ),
    SwatchConfig(
        color_name="PA658",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[33, 8, 0, 6]
    ),
    SwatchConfig(
        color_name="PA659",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[64, 35, 0, 0]
    ),
    SwatchConfig(
        color_name="PA660",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[91, 60, 0, 0]
    ),
    SwatchConfig(
        color_name="PA662",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 79, 0, 11]
    ),
    SwatchConfig(
        color_name="PA663",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[11, 9, 0, 0]
    ),
    SwatchConfig(
        color_name="PA666",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[34, 30, 0, 6]
    ),
    SwatchConfig(
        color_name="PA667",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[56, 47, 0, 11]
    ),
    SwatchConfig(
        color_name="PA668",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[69, 65, 0, 30]
    ),
    SwatchConfig(
        color_name="PA675",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[18, 91, 0, 0]
    ),
    SwatchConfig(
        color_name="PA685",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 27, 0, 6]
    ),
    SwatchConfig(
        color_name="PA688",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[6, 56, 0, 18]
    ),
    SwatchConfig(
        color_name="PA692",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 23, 6, 0]
    ),
    SwatchConfig(
        color_name="PA694",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 6, 15]
    ),
    SwatchConfig(
        color_name="PA699",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 7, 0]
    ),
    SwatchConfig(
        color_name="PA702",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 69, 34, 9]
    ),
    SwatchConfig(
        color_name="PA705",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 6, 0]
    ),
    SwatchConfig(
        color_name="PA706",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 6, 0]
    ),
    SwatchConfig(
        color_name="PA710",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 79, 58, 0]
    ),
    SwatchConfig(
        color_name="PA712",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 6, 18, 0]
    ),
    SwatchConfig(
        color_name="PA713",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 11, 30, 0]
    ),
    SwatchConfig(
        color_name="PA714",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 43, 0]
    ),
    SwatchConfig(
        color_name="PA716",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 50, 100, 0]
    ),
    SwatchConfig(
        color_name="PA720",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 34, 1]
    ),
    SwatchConfig(
        color_name="PA721",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 18, 47, 0]
    ),
    SwatchConfig(
        color_name="PA727",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 15, 30, 6]
    ),
    SwatchConfig(
        color_name="PA731",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 51, 100, 6]
    ),
    SwatchConfig(
        color_name="PA7401",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 4, 18, 0]
    ),
    SwatchConfig(
        color_name="PA7404",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 80, 0]
    ),
    SwatchConfig(
        color_name="PA7408",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 25, 95, 0]
    ),
    SwatchConfig(
        color_name="PA7409",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 30, 95, 0]
    ),
    SwatchConfig(
        color_name="PA7430",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[12, 39, 9, 0]
    ),
    SwatchConfig(
        color_name="PA7435",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 10, 35]
    ),
    SwatchConfig(
        color_name="PA7444",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[20, 17, 0, 0]
    ),
    SwatchConfig(
        color_name="PA7447",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[74, 83, 25, 9]
    ),
    SwatchConfig(
        color_name="PA7461",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[93, 37, 7, 0]
    ),
    SwatchConfig(
        color_name="PA7463",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 43, 0, 65]
    ),
    SwatchConfig(
        color_name="PA7466",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[87, 0, 27, 0]
    ),
    SwatchConfig(
        color_name="PA7469",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 20, 0, 40]
    ),
    SwatchConfig(
        color_name="PA7482",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[85, 12, 96, 1]
    ),
    SwatchConfig(
        color_name="PA7485",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[9, 0, 18, 40]
    ),
    SwatchConfig(
        color_name="PA7495",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[49, 25, 87, 9]
    ),
    SwatchConfig(
        color_name="PA7496",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 0, 100, 38]
    ),
    SwatchConfig(
        color_name="PA7543",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[23, 11, 8, 21]
    ),
    SwatchConfig(
        color_name="PA7546",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[87, 67, 48, 51]
    ),
    SwatchConfig(
        color_name="PA7550",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 34, 98, 12]
    ),
    SwatchConfig(
        color_name="PA7622",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 93, 76, 27]
    ),
    SwatchConfig(
        color_name="PA7625",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 80, 78, 0]
    ),
    SwatchConfig(
        color_name="PA7687",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[82, 52, 0, 46]
    ),
    SwatchConfig(
        color_name="PA8001",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[5, 0, 0, 20]
    ),
    SwatchConfig(
        color_name="PA801",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[84, 11, 10, 0]
    ),
    SwatchConfig(
        color_name="PA802",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[48, 0, 84, 0]
    ),
    SwatchConfig(
        color_name="PA803",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[2, 5, 84, 0]
    ),
    SwatchConfig(
        color_name="PA804",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 40, 79, 0]
    ),
    SwatchConfig(
        color_name="PA807",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[22, 82, 1, 0]
    ),
    SwatchConfig(
        color_name="PA811",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 59, 71, 0]
    ),
    SwatchConfig(
        color_name="PA812",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 50, 15, 0]
    ),
    SwatchConfig(
        color_name="PA814",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[49, 60, 0, 0]
    ),
    SwatchConfig(
        color_name="PA8281",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[20, 5, 15, 15]
    ),
    SwatchConfig(
        color_name="PA871",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 43, 84, 8]
    ),
    SwatchConfig(
        color_name="PA872",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[40, 43, 80, 8]
    ),
    SwatchConfig(
        color_name="PA873",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[41, 48, 80, 8]
    ),
    SwatchConfig(
        color_name="PA873C_GOLDFOIL",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[41, 48, 80, 8]
    ),
    SwatchConfig(
        color_name="PA874",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 29, 100, 0]
    ),
    SwatchConfig(
        color_name="PA875",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[37, 53, 79, 7]
    ),
    SwatchConfig(
        color_name="PA877",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[10, 0, 0, 16]
    ),
    SwatchConfig(
        color_name="PA9300",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[4, 17, 5, 0]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY1",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 8]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY2",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 10]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY3",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 17]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY4",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 24]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY5",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 34]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY6",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 31]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY7",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 38]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY8",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 1, 0, 43]
    ),
    SwatchConfig(
        color_name="PACOOLGRAY9",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 1, 0, 51]
    ),
    SwatchConfig(
        color_name="PAGREEN",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 65, 0]
    ),
    SwatchConfig(
        color_name="PAHEXCHRMAG",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PAN312",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[80, 0, 0, 20]
    ),
    SwatchConfig(
        color_name="PAORANGE021",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 66, 100, 0]
    ),
    SwatchConfig(
        color_name="PAPROCBLUE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 9, 0, 6]
    ),
    SwatchConfig(
        color_name="PAPROCMAG",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 100, 0, 0]
    ),
    SwatchConfig(
        color_name="PAPROCYAN",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="PAPROCYEL",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PARED032",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 79, 95, 0]
    ),
    SwatchConfig(
        color_name="PAREFLEXBLUE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 72, 0, 6]
    ),
    SwatchConfig(
        color_name="PAWARMGRAY8",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 9, 15, 43]
    ),
    SwatchConfig(
        color_name="PAWARMGREY",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 24]
    ),
    SwatchConfig(
        color_name="PAWARMRED",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 79, 90, 0]
    ),
    SwatchConfig(
        color_name="PAYEL012",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 51, 0]
    ),
    SwatchConfig(
        color_name="PAYELLOW",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="PLACEHOLDER",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 100]
    ),
    SwatchConfig(
        color_name="PLACEHOLDER_IMPRINTDUMMY",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 70]
    ),
    SwatchConfig(
        color_name="SICPA340801-F",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[50, 5, 5, 0]
    ),
    SwatchConfig(
        color_name="SICPA360081-F",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[50, 5, 5, 0]
    ),
    SwatchConfig(
        color_name="SILVER",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 10]
    ),
    SwatchConfig(
        color_name="SILVER_HF",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[10, 0, 0, 40]
    ),
    SwatchConfig(
        color_name="SONDERFARBE_EDELMANN",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[70, 7, 60, 0]
    ),
    SwatchConfig(
        color_name="UV_FLUORESCENT",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[100, 0, 0, 0]
    ),
    SwatchConfig(
        color_name="VARNISH",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 0, 30]
    ),
    SwatchConfig(
        color_name="VARNISH_FREE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 10, 20, 0]
    ),
    SwatchConfig(
        color_name="VARNISH_PARTIAL_DISPERSION",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[0, 0, 100, 0]
    ),
    SwatchConfig(
        color_name="WHITE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[12, 7, 7, 0]
    ),
    SwatchConfig(
        color_name="WHITE_OPAQUE",
        color_model=ColorModel.SPOT,
        color_space=ColorSpace.CMYK,
        color_values=[27, 4, 0, 0]
    )
]
