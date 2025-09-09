# Imports
from typing import Literal, Tuple

# Package Imports
from gmdkit.models.object import Object, ObjectList
from gmdkit.models.types import DictClass


def fnt_load(path) -> dict:
    
    result = {}
    
    file = open(path, "r")
        
    for line in file:
        
        tokens = line.split()
        first = tokens.pop(0)
        print(first, tokens)
        data = {}

        for t in tokens:

            k,v = t.split("=",maxsplit=1)
            
            if len(v) >= 2 and v[0] == v[-1] and v[0] in {'"', "'"}:
                v = v[1:-1]
            
            else:
                for cast in (int, float):
                    try:
                        v = cast(v)
                        break
                    except ValueError:
                        continue
            
            data[k] = v
        
        match first:
            case "page":
                pages = result.setdefault("pages",{})
                page_id = data.pop("id")
                pages[page_id] = data
            
            case "chars":
                result["chars_count"] = data.pop("count")
                
            case "char":
                chars = result.setdefault("chars",{})
                char_id = data.pop("id")
                chars[char_id] = data
            
            case "kernings":
                result["kernings_count"] = data.pop("count")
            
            case "kerning":
                kernings = result.setdefault("kernings",{})
                first_id = data.pop("first")
                second_id = data.pop("second")
                
                k_first = kernings.setdefault(first_id,{})
                k_first[second_id] = data.pop("amount")
                chars[char_id] = data
                
            case _:
                result[first] = data
                
    file.close()
        
    return result

font = fnt_load(r"D:\SteamLibrary\steamapps\common\Geometry Dash\Resources\bigFont-uhd.fnt")

def center(self, string):
    
    # individual text objects are center-left aligned
    pass


class TextObject:
    
    __slots__ = ("objects","len_x","len_y","center_x","center_y")


class FontObject(DictClass):
    
    def __init__(self, path):
        
        font_data = fnt_load(path)
        
        super().__init__(font_data)
        
    
    
    def render_text(self, string):
        
        cursor_x = 0
        cursor_y = 0
        line_height = self["common"]["lineHeight"]
        
        
        for c in string:
            
            
                    
    
    def split_text_object(obj:Object, split_len:int=1) -> ObjectList:
        
        pass
    
    
    def create_text_objects(
            string, 
            groups:Literal[],
            
            max_len:int=None,
            max_wrap_len:int=None
            kerning:int=0,            
            position:Tuple[float,float]=(0,0),
            anchor_x:Literal["left","center","right"]=None,
            anchor_y:Literal["top","middle","bottom"]=None
            align_x:Literal["left","center","right","justify"]="left",
            align_y:Literal["top","middle","bottom"]="center", 
            ) -> ObjectList:
        
        anchor_x = anchor_x or "center" if align_x == "justify" else align_x
        
        anchor_y = anchor_y or align_y
        
        
        
        
            
    