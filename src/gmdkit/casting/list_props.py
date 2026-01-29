# Package Imports
from gmdkit.serialization.type_cast import to_string
from gmdkit.models.prop.list import IntList


LIST_DECODERS = {
    'k15': bool,
    'k96': IntList.from_string,
}


LIST_ENCODERS = {
    'k15': int,
    'k96': to_string,
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
    'k21': int,
    'k22': int,
    'k42': int,
    'k46': int,
    'k60': int,
    'k83': int,
    'k84': int,
    'k96': IntList,
    'k98': int,
    'k99': int,
    'k113': int,
    'k114': int,
    'kCEK': int,
}