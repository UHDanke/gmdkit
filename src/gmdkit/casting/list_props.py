# Package Imports
from gmdkit.serialization.type_cast import (
    to_string, to_plist,
    decode_text, encode_text
    )
from gmdkit.serialization import enums
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.level_dict import LevelMapping

LIST_DECODERS = {
    'k3': decode_text,
    'k15': bool,
    'k21': enums.ListType.from_string,
    'k96': IntList.from_string,
    'k97': LevelMapping.from_plist,
}


LIST_ENCODERS = {
    'k3': encode_text,
    'k15': int,
    'k96': to_string,
    'k97': to_plist,
}


LIST_TYPES = {
    'k1': int,
    'k2': str,
    'k3': str,
    'k5': str,
    'k7': int,
    'k11': int,
    'k15': bool,
    'k16': int,
    'k21': enums.ListType,
    'k22': int,
    'k42': int,
    'k46': int,
    'k60': int,
    'k83': int,
    'k84': int,
    'k96': IntList,
    'k97': LevelMapping,
    'k98': int,
    'k99': int,
    'k113': int,
    'k114': int,
    'kCEK': int,
}