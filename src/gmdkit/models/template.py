# Imports
from typing import Any, Self, overload
from enum import Enum, IntEnum

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.type_cast import get_string, to_string
from gmdkit.serialization.mixins import ( 
    FilePathMixin, 
    DataclassDecoderMixin,
    PlistLoaderMixin,
    FolderLoaderMixin
    )
from gmdkit.serialization.functions import (
    dict_cast, 
    from_node_dict, to_node_dict, 
    read_plist, write_plist, 
    dataclass_decoder,
    kv_wrap, args_wrap,
    get_load_keys, set_field, get_field
    )
from gmdkit.mappings import smart_prefab, smart_template, obj_prop
from gmdkit.models.object import Object, ObjectGroup
from gmdkit.utils.enums import ArrowDir
from gmdkit.utils.misc import get_enum_values, normalize_orientation, typed_cache

class TemplatePosition(IntEnum):
    CENTER = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8
    
class TemplateType(Enum):
    NONE = "0"
    SQUARE = "1"
    SLOPE_BOTTOM_RIGHT = "2"
    SLOPE_BOTTOM_LEFT = "3"
    SLOPE_TOP_RIGHT = "4"
    SLOPE_TOP_LEFT = "5"
    LONG_SLOPE_CENTER_BOTTOM_RIGHT = "6"
    LONG_SLOPE_SIDE_BOTTOM_RIGHT = "7"
    LONG_SLOPE_CENTER_BOTTOM_LEFT = "8"
    LONG_SLOPE_SIDE_BOTTOM_LEFT = "9"
    LONG_SLOPE_CENTER_TOP_RIGHT = "A"
    LONG_SLOPE_SIDE_TOP_RIGHT = "B"
    LONG_SLOPE_CENTER_TOP_LEFT = "C"
    LONG_SLOPE_SIDE_TOP_LEFT = "D"
    LONG_SLOPE_CENTER_RIGHT_TOP = "E"
    LONG_SLOPE_SIDE_RIGHT_TOP = "F"
    LONG_SLOPE_CENTER_RIGHT_BOTTOM = "G"
    LONG_SLOPE_SIDE_RIGHT_BOTTOM = "H"
    LONG_SLOPE_CENTER_LEFT_BOTTOM = "I"
    LONG_SLOPE_SIDE_LEFT_BOTTOM = "J"
    LONG_SLOPE_CENTER_LEFT_TOP = "K"
    LONG_SLOPE_SIDE_LEFT_TOP = "L"
    
    def to_object(self):
        cls = type(self)
        
        match self:
            
            case cls.NONE:
                return None

            case cls.SQUARE:
                obj = Object.default(2895)

            case cls.SLOPE_BOTTOM_RIGHT:
                obj = Object.default(2896)

            case cls.SLOPE_BOTTOM_LEFT:
                obj = Object.default(2896)
                obj[obj_prop.ROTATION] = 90

            case cls.SLOPE_TOP_RIGHT:
                obj = Object.default(2896)
                obj[obj_prop.ROTATION] = 270

            case cls.SLOPE_TOP_LEFT:
                obj = Object.default(2896)
                obj[obj_prop.ROTATION] = 180

            case cls.LONG_SLOPE_CENTER_BOTTOM_RIGHT:
                obj = Object.default(2897)

            case cls.LONG_SLOPE_SIDE_BOTTOM_RIGHT:
                obj = Object.default(2897)
                obj[obj_prop.X] = -30

            case cls.LONG_SLOPE_CENTER_BOTTOM_LEFT:
                obj = Object.default(2896)
                obj[obj_prop.FLIP_X] = True

            case cls.LONG_SLOPE_SIDE_BOTTOM_LEFT:
                obj = Object.default(2896)
                obj[obj_prop.FLIP_X] = True
                obj[obj_prop.X] = 30

            case cls.LONG_SLOPE_CENTER_TOP_RIGHT:
                obj = Object.default(2897)
                obj[obj_prop.FLIP_Y] = True

            case cls.LONG_SLOPE_SIDE_TOP_RIGHT:
                obj = Object.default(2897)
                obj[obj_prop.FLIP_Y] = True
                obj[obj_prop.X] = -30

            case cls.LONG_SLOPE_CENTER_TOP_LEFT:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 180
                
            case cls.LONG_SLOPE_SIDE_TOP_LEFT:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 180
                obj[obj_prop.X] = 30
                
            case cls.LONG_SLOPE_CENTER_RIGHT_TOP:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 270
                
            case cls.LONG_SLOPE_SIDE_RIGHT_TOP:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 270
                obj[obj_prop.Y] = -30
                
            case cls.LONG_SLOPE_CENTER_RIGHT_BOTTOM:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 270
                obj[obj_prop.FLIP_Y] = True
                
            case cls.LONG_SLOPE_SIDE_RIGHT_BOTTOM:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 270
                obj[obj_prop.FLIP_Y] = True
                obj[obj_prop.Y] = 30
                
            case cls.LONG_SLOPE_CENTER_LEFT_BOTTOM:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 90
                
            case cls.LONG_SLOPE_SIDE_LEFT_BOTTOM:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 90
                obj[obj_prop.Y] = 30
                
            case cls.LONG_SLOPE_CENTER_LEFT_TOP:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 90
                obj[obj_prop.FLIP_Y] = True
                
            case cls.LONG_SLOPE_SIDE_LEFT_TOP:
                obj = Object.default(2897)
                obj[obj_prop.ROTATION] = 90
                obj[obj_prop.FLIP_Y] = True
                obj[obj_prop.Y] = -30
                
        return obj
            
    @classmethod
    def from_object(cls, obj:Object) -> Self | tuple[Self, Self]: 
        
        obj_id = obj.get(obj_prop.ID)
        
        match obj_id:
            case 2895:
                return cls.SQUARE
            
            case 2896:
                rotation = obj.get(obj_prop.ROTATION)
                flip_x = obj.get(obj_prop.FLIP_X)
                flip_y = obj.get(obj_prop.FLIP_Y)
                x_dir, y_dir = normalize_orientation(rotation,flip_x,flip_y)
                
                match (x_dir,y_dir):
                    case (ArrowDir.RIGHT,ArrowDir.DOWN)|(ArrowDir.DOWN,ArrowDir.RIGHT):
                        return cls.SLOPE_BOTTOM_RIGHT
                    case (ArrowDir.LEFT,ArrowDir.DOWN)|(ArrowDir.DOWN,ArrowDir.LEFT):
                        return cls.SLOPE_BOTTOM_LEFT
                    case (ArrowDir.RIGHT,ArrowDir.UP)|(ArrowDir.UP,ArrowDir.RIGHT):
                        return cls.SLOPE_TOP_RIGHT
                    case (ArrowDir.LEFT,ArrowDir.UP)|(ArrowDir.UP,ArrowDir.LEFT):
                        return cls.SLOPE_TOP_LEFT
                    
            case 2897:
                rotation = obj.get(obj_prop.ROTATION)
                flip_x = obj.get(obj_prop.FLIP_X)
                flip_y = obj.get(obj_prop.FLIP_Y)
                x_dir, y_dir = normalize_orientation(rotation,flip_x,flip_y)
                
                match (x_dir, y_dir):
                    case (ArrowDir.RIGHT, ArrowDir.DOWN):
                        return (cls.LONG_SLOPE_CENTER_BOTTOM_RIGHT, cls.LONG_SLOPE_SIDE_BOTTOM_RIGHT)
                    case (ArrowDir.LEFT, ArrowDir.DOWN):
                        return (cls.LONG_SLOPE_CENTER_BOTTOM_LEFT, cls.LONG_SLOPE_SIDE_BOTTOM_LEFT)
                    case (ArrowDir.RIGHT, ArrowDir.UP):
                        return (cls.LONG_SLOPE_CENTER_TOP_RIGHT, cls.LONG_SLOPE_SIDE_TOP_RIGHT)
                    case (ArrowDir.LEFT, ArrowDir.UP):
                        return (cls.LONG_SLOPE_CENTER_TOP_LEFT, cls.LONG_SLOPE_SIDE_TOP_LEFT)
                    case (ArrowDir.UP, ArrowDir.RIGHT):
                        return (cls.LONG_SLOPE_CENTER_RIGHT_TOP, cls.LONG_SLOPE_SIDE_RIGHT_TOP)
                    case (ArrowDir.DOWN, ArrowDir.RIGHT):
                        return (cls.LONG_SLOPE_CENTER_RIGHT_BOTTOM, cls.LONG_SLOPE_SIDE_RIGHT_BOTTOM)
                    case (ArrowDir.UP, ArrowDir.LEFT):
                        return (cls.LONG_SLOPE_CENTER_LEFT_TOP, cls.LONG_SLOPE_SIDE_LEFT_TOP)
                    case (ArrowDir.DOWN, ArrowDir.LEFT):
                        return (cls.LONG_SLOPE_CENTER_LEFT_BOTTOM, cls.LONG_SLOPE_SIDE_LEFT_BOTTOM)   

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
    
    @staticmethod
    @typed_cache(maxsize=256)
    def validate_string(key:str):
        if len(key) != 9:
            raise ValueError(f"layout expected 9 characters, got {len(key)}")
            
        chars = get_enum_values(TemplateType)
        
        for s in key:
            if s not in chars:
                raise ValueError(f"expected layout key between 0-9 and A-L, got key {s} instead")
    
    @staticmethod
    @typed_cache(maxsize=32)
    def get_slot_name(slot:str|int, offset:ArrowDir=ArrowDir.NONE):
        if isinstance(slot, int):
            if slot not in range(1,10):
                raise ValueError(f"slot out of range, expected 1-9 got {slot} instead") 
         
        slot = slot.lower()
        
        opposites = {
            "left_top":"top_left",
            "right_top":"top_right",
            "left_bottom":"bottom_left",
            "right_bottom":"bottom_right"
            }

        slot = opposites.get(slot,slot)
        
        if offset == ArrowDir.NONE:
            return slot
        
        OFFSET_MAP = {
            "center":       {ArrowDir.UP: "top",        ArrowDir.DOWN: "bottom",      ArrowDir.LEFT: "left",         ArrowDir.RIGHT: "right"},
            "top":          {ArrowDir.UP: None,          ArrowDir.DOWN: "center",      ArrowDir.LEFT: "top_left",     ArrowDir.RIGHT: "top_right"},
            "bottom":       {ArrowDir.UP: "center",      ArrowDir.DOWN: None,          ArrowDir.LEFT: "bottom_left",  ArrowDir.RIGHT: "bottom_right"},
            "left":         {ArrowDir.UP: "top_left",    ArrowDir.DOWN: "bottom_left", ArrowDir.LEFT: None,           ArrowDir.RIGHT: "center"},
            "right":        {ArrowDir.UP: "top_right",   ArrowDir.DOWN: "bottom_right",ArrowDir.LEFT: "center",       ArrowDir.RIGHT: None},
            "top_left":     {ArrowDir.UP: None,          ArrowDir.DOWN: "left",        ArrowDir.LEFT: None,           ArrowDir.RIGHT: "top"},
            "top_right":    {ArrowDir.UP: None,          ArrowDir.DOWN: "right",       ArrowDir.LEFT: "top",          ArrowDir.RIGHT: None},
            "bottom_left":  {ArrowDir.UP: "left",        ArrowDir.DOWN: None,          ArrowDir.LEFT: None,           ArrowDir.RIGHT: "bottom"},
            "bottom_right": {ArrowDir.UP: "right",       ArrowDir.DOWN: None,          ArrowDir.LEFT: "bottom",       ArrowDir.RIGHT: None},
        }
        
        return OFFSET_MAP[slot].get(offset)
    
    def set_slot(self, slot:str|int, value:TemplateType, offset:ArrowDir=ArrowDir.NONE):        
        set_field(self, self.get_slot_name(slot,offset), value)
    
    def get_slot(self, slot:str|int, offset:ArrowDir=ArrowDir.NONE):       
        get_field(self, self.get_slot_name(slot,offset))
    
    def add_smart_object(self, slot:str|int, obj:Object):
        
        obj_id = obj.get(obj_prop.ID)
        
        key = TemplateType.from_object(obj)
        
        match obj_id:
            case 2895|2896:
                self.set_slot(slot, key)
            case 2897:
                center, side = key
                self.set_slot(slot, center)
                
                match side:
                    case TemplateType.LONG_SLOPE_SIDE_BOTTOM_RIGHT|TemplateType.LONG_SLOPE_SIDE_TOP_RIGHT:
                        offset = ArrowDir.RIGHT
                    case TemplateType.LONG_SLOPE_SIDE_BOTTOM_LEFT|TemplateType.LONG_SLOPE_SIDE_TOP_LEFT:
                        offset = ArrowDir.LEFT
                    case TemplateType.LONG_SLOPE_SIDE_RIGHT_TOP|TemplateType.LONG_SLOPE_SIDE_LEFT_TOP:
                        offset = ArrowDir.UP
                    case TemplateType.LONG_SLOPE_SIDE_RIGHT_BOTTOM|TemplateType.LONG_SLOPE_SIDE_LEFT_BOTTOM:
                        offset = ArrowDir.DOWN
                
                if self.get_slot(slot, offset) is TemplateType.NONE:
                    self.set_slot(slot, side, offset)
            case _:
                raise ValueError("object is not a smart template")

def layout_string(layout:Any) -> str:
    string = to_string(layout)
    SmartLayout.validate_string(string)
    return string

PREFAB_DECODERS = {smart_prefab.OBJECT_STRING: ObjectGroup}
PREFAB_ENCODERS = {smart_prefab.OBJECT_STRING: get_string}
PREFAB_TYPES = {smart_prefab.OBJECT_STRING: ObjectGroup}
PREFAB_KWARGS = {smart_prefab.OBJECT_STRING}


class SmartPrefab(PlistLoaderMixin,DictClass[int,Any]):
    DECODER = staticmethod(dict_cast(from_node_dict(PREFAB_DECODERS),key_start=int,default=read_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER = staticmethod(dict_cast(to_node_dict(PREFAB_ENCODERS),key_end=str,default=write_plist,allow_kwargs=PREFAB_KWARGS))
    ENCODER_KEY = 11
    SELECTORS = get_load_keys(PREFAB_TYPES)


class SmartPrefabList(PlistLoaderMixin,ListClass[SmartPrefab]):
    DECODER = SmartPrefab.from_node
    ENCODER = SmartPrefab.to_node
    IS_ARRAY = True   


class SmartPrefabLayout(PlistLoaderMixin,DictClass[str,SmartPrefabList]):
    DECODER = staticmethod(kv_wrap(value_func=SmartPrefabList.from_node))
    ENCODER = staticmethod(kv_wrap(value_func=SmartPrefabList.to_node))
    
    def get_layout(self, key:str) -> SmartLayout:
        return SmartLayout.from_string(key)
        
    
    def get_layout(self, key:str) -> SmartLayout:
        return SmartLayout.from_string(key)
    
    @overload
    def add_prefabs(self, key:str, prefabs:SmartPrefab) -> None: ...
    
    @overload
    def add_prefabs(self, key:str, prefabs:SmartPrefabList) -> None: ...
    
    def add_prefabs(self, key:str, prefabs:SmartPrefab|SmartPrefabList) -> None:
        SmartLayout.validate_string(key)
        prefab_list = self.setdefault(key, SmartPrefabList())
        
        if isinstance(prefabs, SmartPrefab):
            prefab_list.append(prefabs)
        elif isinstance(prefabs, SmartPrefabList):
            prefab_list.extend(prefabs)
    
    def update_prefabs(self, prefab_dict:dict[str,SmartPrefabList]):
        for key, prefabs in prefab_dict.items():
            self.add_prefabs(key, prefabs)

TEMPLATE_DECODERS = {smart_template.VARIATIONS: SmartPrefabLayout.from_node}
TEMPLATE_ENCODERS = {smart_template.VARIATIONS: SmartPrefabLayout.to_node}
TEMPLATE_TYPES = {smart_template.VARIATIONS: SmartPrefabLayout}
TEMPLATE_KWARGS = {smart_template.VARIATIONS}


class SmartTemplate(FilePathMixin,PlistLoaderMixin,DictClass[int,Any]):
    DECODER = staticmethod(dict_cast(TEMPLATE_DECODERS,key_start=int,default=read_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER = staticmethod(dict_cast(TEMPLATE_ENCODERS,key_end=str,default=write_plist,allow_kwargs=TEMPLATE_KWARGS))
    ENCODER_KEY = 10
    EXTENSION = "gmdt"
    SELECTORS = get_load_keys(TEMPLATE_TYPES)
    
    def _name_fallback_(self):
        container = self.CONTAINER
        data = self if container is None else getattr(self, container)
        return data[smart_template.NAME]   


class SmartTemplateList(FolderLoaderMixin,FilePathMixin,PlistLoaderMixin,ListClass[SmartTemplate]):
    DECODER = SmartTemplate.from_node
    ENCODER = SmartTemplate.to_node
    IS_ARRAY = True
    EXTENSION = "plist"
    LOAD_CONTENT = False
    FOLDER_DECODER = staticmethod(args_wrap(SmartTemplate.from_file,1))
    FOLDER_ENCODER = staticmethod(args_wrap(SmartTemplate.to_file,2))
    FOLDER_EXTENSION = SmartTemplate.EXTENSION
    