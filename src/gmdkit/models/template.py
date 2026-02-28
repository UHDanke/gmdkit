# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.type_cast import to_string, to_numkey, to_node
from gmdkit.utils.typing import Element
from gmdkit.serialization.mixins import PlistDecoderMixin, FilePathMixin, DataclassDecoderMixin
from gmdkit.serialization.functions import dict_cast, from_node_dict, to_node_dict, read_plist, write_plist, dataclass_decoder
from gmdkit.mappings import smart_prefab, smart_template
from gmdkit.models.object import ObjectGroup
from gmdkit.utils.enums import TemplateType


@dataclass_decoder(slots=True, separator='', from_array=True)
class SmartLayout(DataclassDecoderMixin):
    center: TemplateType
    top: TemplateType
    bottom: TemplateType
    left: TemplateType
    right: TemplateType
    top_left: TemplateType
    top_right: TemplateType
    bottom_left: TemplateType
    bottom_right: TemplateType


PREFAB_DECODERS = {
    smart_prefab.OBJECT_STRING: ObjectGroup.from_string,
    }

PREFAB_ENCODERS = {
    smart_prefab.OBJECT_STRING: to_string,
    }

PREFAB_KWARGS = {smart_prefab.OBJECT_STRING}


class SmartPrefab(PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(from_node_dict(PREFAB_DECODERS),key_start=to_numkey,default=read_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(PREFAB_ENCODERS),key_end=str,default=write_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER_KEY = 11
    

def to_prefab(node:Element, **kwargs) -> SmartPrefab:
    return SmartPrefab.from_node(node=node, **kwargs)

def from_prefab(prefab:SmartPrefab, **kwargs) -> Element:
    return prefab.to_node(**kwargs)


class SmartPrefabList(PlistDecoderMixin,ListClass):
    DECODER = staticmethod(to_prefab)
    ENCODER = staticmethod(from_prefab)
    IS_ARRAY = True   

def to_prefab_list(key:str, node:Element, **kwargs) -> tuple[str,SmartPrefabList]:
    return key, SmartPrefabList.from_node(node=node, **kwargs)

def from_prefab_list(prefab_list:SmartPrefabList, **kwargs) -> tuple[str,Element]:
    return prefab_list.to_node(**kwargs)

class SmartPrefabLayout(PlistDecoderMixin,DictClass):
    DECODER = staticmethod(to_prefab_list)
    ENCODER = staticmethod(from_prefab_list)

TEMPLATE_DECODERS = {
    smart_template.VARIATIONS: SmartPrefabLayout.from_node
    }

TEMPLATE_ENCODERS = {
    smart_template.VARIATIONS: to_node
    }

TEMPLATE_KWARGS = {smart_template.VARIATIONS}

TEMPLATE_NODES = {smart_template.VARIATIONS}

class SmartTemplate(FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(from_node_dict(TEMPLATE_DECODERS,exclude=TEMPLATE_NODES),key_start=to_numkey,default=read_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(TEMPLATE_ENCODERS,exclude=TEMPLATE_NODES),key_end=str,default=write_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER_KEY = 10
    EXTENSION = "gmdt"

def to_template(node:Element, **kwargs) -> SmartTemplate:
    return SmartTemplate.from_node(node=node, **kwargs)

def from_template(template:SmartTemplate, **kwargs) -> Element:
    return template.to_node(**kwargs)

class SmartTemplateList(FilePathMixin,PlistDecoderMixin,ListClass):
    DECODER = staticmethod(to_template)
    ENCODER = staticmethod(from_template)
    IS_ARRAY = True
    EXTENSION = "plist"