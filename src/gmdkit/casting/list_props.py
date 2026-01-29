# Package Imports
from gmdkit.serialization.type_cast import to_string, zip_string
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.gzip import ObjectString, ReplayString


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
    'k11': int,
    'k113': int,
    'k114': int,
    'k15': bool,
    'k16': int,
    'k2': str,
    'k21': int,
    'k22': int,
    'k3': str,
    'k42': int,
    'k46': int,
    'k5': str,
    'k60': int,
    'k7': int,
    'k83': int,
    'k84': int,
    'k96': IntList,
    'k98': int,
    'k99': int,
    'kCEK': int,
}