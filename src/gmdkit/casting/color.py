# Package Imports
from gmdkit.models.prop.hsv import HSV


COLOR_DECODERS = {
    1: int,
    2: int,
    3: int,
    4: int,
    5: lambda x: bool(int(x)),
    6: int,
    7: float,
    8: lambda x: bool(int(x)),
    9: int,
    10: HSV.from_string,
    11: int,
    12: int,
    13: int,
    14: float,
    15: float,
    16: float,
    17: float,
    18: lambda x: bool(int(x))
    }

COLOR_ENCODERS = {
    5: lambda x: str(int(x)),
    8: lambda x: str(int(x)),
    10: HSV.to_string,
    18: lambda x: str(int(x))
    }