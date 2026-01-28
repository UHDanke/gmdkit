# Package Imports
from gmdkit.models.prop.hsv import HSV
from gmdkit.serialization.type_cast import to_bool, to_string, from_bool, from_float

COLOR_DECODERS = {
    1: int,
    2: int,
    3: int,
    4: int,
    5: to_bool,
    6: int,
    7: float,
    8: to_bool,
    9: int,
    10: HSV.from_string,
    11: int,
    12: int,
    13: int,
    14: float,
    15: float,
    16: float,
    17: float,
    18: to_bool
    }

COLOR_ENCODERS = {
    5: from_bool,
    7: from_float,
    8: from_bool,
    10: to_string,
    14: from_float,
    15: from_float,
    16: from_float,
    17: from_float,
    18: from_bool
    }

COLOR_TYPES = {
    1: int,
    2: int,
    3: int,
    4: int,
    5: bool,
    6: int,
    7: float,
    8: bool,
    9: int,
    10: HSV,
    11: int,
    12: int,
    13: int,
    14: float,
    15: float,
    16: float,
    17: float,
    18: bool
    }