# Package Imports
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.gzip import ObjectString, ReplayString


LEVEL_DECODERS = {
    'k104': IntList.from_string,
    'k105': IntList.from_string,
    'k109': IntList.from_string,
    'k110': IntList.from_string,
    'k15': lambda x: bool(int(x)),
    'k34': ReplayString,
    'k4': ObjectString,
    'k88': IntList.from_string,
    'k91': IntList.from_string,
}


LEVEL_ENCODERS = {
    'k104': lambda x: x.to_string(),
    'k105': lambda x: x.to_string(),
    'k109': lambda x: x.to_string(),
    'k110': lambda x: x.to_string(),
    'k15': lambda x: str(int(x)),
    'k34': str,
    'k4': str,
    'k88': lambda x: x.to_string(),
    'k91': lambda x: x.to_string(),
}


LIST_DECODERS = {
    'k15': lambda x: bool(int(x)),
    'k96': IntList.from_string,
}


LIST_ENCODERS = {
    'k15': lambda x: str(int(x)),
    'k96': lambda x: x.to_string(),
}
