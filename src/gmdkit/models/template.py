# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.type_cast import to_numkey, get_string
from gmdkit.serialization.mixins import (
    PlistDecoderMixin, 
    FilePathMixin, 
    DataclassDecoderMixin,
    LoadPlistContentMixin
    )
from gmdkit.serialization.functions import (
    dict_cast, 
    from_node_dict, to_node_dict, 
    read_plist, write_plist, 
    dataclass_decoder,
    kv_wrap,
    get_load_keys
    )
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


PREFAB_DECODERS = {smart_prefab.OBJECT_STRING: ObjectGroup}
PREFAB_ENCODERS = {smart_prefab.OBJECT_STRING: get_string}
PREFAB_TYPES = {smart_prefab.OBJECT_STRING: ObjectGroup}
PREFAB_KWARGS = {smart_prefab.OBJECT_STRING}


class SmartPrefab(LoadPlistContentMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(from_node_dict(PREFAB_DECODERS),key_start=to_numkey,default=read_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(PREFAB_ENCODERS),key_end=str,default=write_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER_KEY = 11
    SELECTORS = get_load_keys(PREFAB_TYPES)


class SmartPrefabList(LoadPlistContentMixin,PlistDecoderMixin,ListClass):
    DECODER = SmartPrefab.from_node
    ENCODER = SmartPrefab.to_node
    IS_ARRAY = True   


class SmartPrefabLayout(LoadPlistContentMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(kv_wrap(value_func=SmartPrefabList.from_node))
    ENCODER = staticmethod(kv_wrap(value_func=SmartPrefabList.to_node))


TEMPLATE_DECODERS = {smart_template.VARIATIONS: SmartPrefabLayout.from_node}
TEMPLATE_ENCODERS = {smart_template.VARIATIONS: SmartPrefabLayout.to_node}
TEMPLATE_TYPES = {smart_template.VARIATIONS: SmartPrefabLayout}
TEMPLATE_KWARGS = {smart_template.VARIATIONS}


class SmartTemplate(LoadPlistContentMixin,FilePathMixin,PlistDecoderMixin,DictClass):
    DECODER = staticmethod(dict_cast(TEMPLATE_DECODERS,key_start=to_numkey,default=read_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER = staticmethod(dict_cast(TEMPLATE_ENCODERS,key_end=str,default=write_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER_KEY = 10
    EXTENSION = "gmdt"
    SELECTORS = get_load_keys(TEMPLATE_TYPES)
    
    def _name_fallback_(self):
        container = self.CONTAINER
        data = self if container is None else getattr(self, container)
        return data[smart_template.NAME]   


class SmartTemplateList(LoadPlistContentMixin,FilePathMixin,PlistDecoderMixin,ListClass):
    DECODER = SmartTemplate.from_node
    ENCODER = SmartTemplate.to_node
    IS_ARRAY = True
    EXTENSION = "plist"
    LOAD_CONTENT = False