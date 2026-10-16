# Package Imports
from gmdkit.serialization.mixins import DictDecoderMixin
from gmdkit.utils.types import DictClass
from gmdkit.models.prop.groups import IDList 
from gmdkit.utils import enums

class NameDict(DictDecoderMixin,DictClass[int,str]):
    SEPARATOR = "^"
    PAIR_SEPARATOR = "~"
    DECODER = staticmethod(lambda k, v: (int(k),v))
    ENCODER = staticmethod(lambda k, v: (str(k),str(v)))

class NamedGroupsDict(DictDecoderMixin,DictClass[enums.NamedGroupsType,NameDict]):
    SEPARATOR = "|"
    PAIR_SEPARATOR = ":"
    DECODER = staticmethod(lambda k, v: (enums.NamedGroupsType.from_string(k),NameDict.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k),v.to_string()))

class NamedIDList(IDList):
    SEPARATOR = "^"

class NamedGroupsList(DictDecoderMixin,DictClass[enums.NamedGroupsType,NamedIDList]):
    SEPARATOR = "|"
    PAIR_SEPARATOR = ":"
    DECODER = staticmethod(lambda k, v: (enums.NamedGroupsType.from_string(k),NamedIDList.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k),v.to_string()))
