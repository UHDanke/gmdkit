# Package Imports
from gmdkit.mappings import obj_prop, color_id, obj_id, color_prop
from gmdkit.models.object import ObjectList, Object
from gmdkit.models.prop.color import Color, ColorList
from gmdkit.defaults.color_ids import default_color


RGBA = tuple[int,int,int,float]

MAP_COLOR_TO_TRIGGER = {
    color_prop.RED: obj_prop.trigger.color.RED,
    color_prop.GREEN: obj_prop.trigger.color.GREEN,
    color_prop.BLUE: obj_prop.trigger.color.BLUE,
    color_prop.BLENDING: obj_prop.trigger.color.BLENDING,
    color_prop.CHANNEL: obj_prop.trigger.color.CHANNEL,
    color_prop.COPY_ID: obj_prop.trigger.color.COPY_ID,
    color_prop.OPACITY: obj_prop.trigger.color.OPACITY,
    color_prop.HSV: obj_prop.trigger.color.HSV,
    color_prop.COPY_OPACITY: obj_prop.trigger.color.COPY_OPACITY,
    }

def color_is_editable(color:Color) -> bool:
    return color.get(color_prop.CHANNEL) not in color_id.PRESET


def color_fade(color_1:Color, color_2:Color, percent:float) -> RGBA:
    r1, g1, b1, a1 = color_1.get_rgba()
    r2, g2, b2, a2 = color_2.get_rgba()

    r = round(r1 + (r2 - r1) * percent)
    g = round(g1 + (g2 - g1) * percent)
    b = round(b1 + (b2 - b1) * percent)
    a = a1 + (a2 - a1) * percent

    return (r,g,b,a)



def color_to_trigger(color:Color) -> Object:
    obj = Object.default(obj_id.trigger.COLOR)
    
    for color_key, obj_key in MAP_COLOR_TO_TRIGGER.items():
        if color_key in color:
            obj[obj_key] = color[color_key]
        
    match color.get(color_prop.PLAYER):
        case 1: obj[obj_prop.trigger.color.PLAYER_1] = True
        case 2: obj[obj_prop.trigger.color.PLAYER_2] = True
        case _: pass
    
    obj[obj_prop.trigger.color.DURATION] = 0

    return obj


def trigger_to_color(obj:Object) -> Color:
    
    if obj.get(obj_prop.ID) != obj_id.trigger.COLOR:
        return
    
    color = Color.default(obj.get(color_prop.CHANNEL, 0))
    
    for color_key, obj_key in MAP_COLOR_TO_TRIGGER.items():
        if obj_key in obj:
            color[color_key] = obj[obj_key]
    
    
    match obj.get(color_prop.PLAYER):
        case 1: obj[obj_prop.trigger.color.PLAYER_1] = True
        case 2: obj[obj_prop.trigger.color.PLAYER_2] = True
        case _: pass
            
    return color

def color_is_default(color:Color) -> bool:
    cid = color.get(color_prop.CHANNEL)
    return dict(color) == default_color(cid)
    
def create_color_triggers(
        color_list:ColorList, 
        ignore_defaults:bool=True, 
        pos_x:float=0, 
        pos_y:float=0
        ) -> ObjectList:
    """
    Converts a colors into color triggers.

    Parameters
    ----------
    color_list : 
        A list to retrieve colors from.
    offset_x : float, optional
        Horizontal offset between triggers. The default is 0.
    offset_y : float, optional
        Vertical offset between triggers. The default is -30.

    Returns
    -------
    ObjectList
        An ObjectList containing the generated color triggers.
    """
    objs = ObjectList()
    
    y = pos_y
    x = pos_x
        
    for color in color_list:
        
        if ignore_defaults and color_is_default(color):
            continue
            
        obj = color_to_trigger(color)
            
        objs.append(obj)
        obj.update({
            obj_prop.X: x,
            obj_prop.Y: y
            })
        y += -30
    
    return objs

#def compile_color_

#def reset_unused_colors(level:Level)
        
        