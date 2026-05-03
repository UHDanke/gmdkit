# Package Imports
from gmdkit.mappings import obj_prop, color_id, obj_id
from gmdkit.models.object import ObjectList, Object
from gmdkit.models.prop.color import Color, ColorList
from gmdkit import enums
from gmdkit.models.prop.hsv import HSV


RGBA = tuple[int,int,int,float]


def color_is_editable(color:Color) -> bool:
    """
    Checks if the color can have its values overriden.

    Parameters
    ----------
    color : Color
        The color to check.

    Returns
    -------
    bool

    """
    return color.channel not in color_id.PRESET


def color_fade(color_1:Color, color_2:Color, percent:float) -> RGBA:
    """
    Calculates an intermediary color between two colors.

    Parameters
    ----------
    color_1 : Color
        The original color.
    color_2 : Color
        The new color.
    percent : float
        How much of the new color will be mixed in with the original one.

    Returns
    -------
    RGBA
        DESCRIPTION.

    """
    r1, g1, b1, a1 = color_1.get_rgba()
    r2, g2, b2, a2 = color_2.get_rgba()

    r = round(r1 + (r2 - r1) * percent)
    g = round(g1 + (g2 - g1) * percent)
    b = round(b1 + (b2 - b1) * percent)
    a = a1 + (a2 - a1) * percent

    return (r,g,b,a)


def color_to_trigger(color:Color) -> Object:
    """
    Converts a Color to a Color 

    Parameters
    ----------
    color : Color
        The color to convert.

    Returns
    -------
    Object

    """
    obj = Object.default(obj_id.trigger.COLOR)
    obj[obj_prop.trigger.color.RED] = color.red
    obj[obj_prop.trigger.color.GREEN] = color.green
    obj[obj_prop.trigger.color.BLUE] = color.blue
        
    match color.player:
        case 1: obj[obj_prop.trigger.color.PLAYER_1] = True
        case 2: obj[obj_prop.trigger.color.PLAYER_2] = True
        case _: pass
    
    if (v:=color.blending): obj[obj_prop.trigger.color.BLENDING] = v
    if (v:=color.channel): obj[obj_prop.trigger.color.CHANNEL] = v
    
    obj[obj_prop.trigger.color.OPACITY] = color.opacity
    
    if (v:=color.copy_id): obj[obj_prop.trigger.color.COPY_ID] = v
    
    if not Color.CONDITION(v:=color.hsv): obj[obj_prop.trigger.color.HSV] = v
    
    obj[obj_prop.trigger.color.DURATION] = 0
    
    if (v:=color.copy_opacity): obj[obj_prop.trigger.color.COPY_OPACITY] = v
    
    return obj


def trigger_to_color(obj:Object) -> Color:
    """
    Converts a color trigger to a Color.

    Parameters
    ----------
    obj : Object
        The color object to convert.

    Returns
    -------
    Color

    """
    
    if obj[obj_prop.ID] != obj_id.trigger.COLOR: return
    
    color = Color.default(obj.get(obj_prop.trigger.color.CHANNEL, 0))
    color.red = obj.get(obj_prop.trigger.color.RED,0)
    color.green = obj.get(obj_prop.trigger.color.GREEN,0)
    color.blue = obj.get(obj_prop.trigger.color.BLUE,0)
    
    p_1 = obj[obj_prop.trigger.color.PLAYER_1]
    p_2 = obj[obj_prop.trigger.color.PLAYER_1]
    
    if p_1 and p_2:
        color.player = enums.TargetPlayer.ALL
    elif not p_1 and not p_2:
        color.player = enums.TargetPlayer.NONE
    elif p_1:
        color.player = enums.TargetPlayer.P1
    elif p_2:
        color.player = enums.TargetPlayer.P2
        
    color.blending = obj.get(obj_prop.trigger.color.BLENDING,False)
    color.channel = obj.get(obj_prop.trigger.color.CHANNEL,0)
    color.opacity = obj.get(obj_prop.trigger.color.OPACITY,0)
    color.copy_id = obj.get(obj_prop.trigger.color.COPY_ID,0)
    color.hsv = obj.get(obj_prop.trigger.color.HSV,HSV())
    color.copy_opacity = obj.get(obj_prop.trigger.color.COPY_OPACITY,False)
    
    return color


def create_color_triggers(
        color_list:ColorList, 
        ignore_default:bool=True, 
        pos_x:float=0, 
        pos_y:float=0
        ) -> ObjectList:
    """
    Converts a list of colors into color triggers.

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
    ObjectListx
        An ObjectList containing the generated color triggers.
    """
    obj_list = ObjectList()
    
    y = pos_y
    x = pos_x
        
    for color in color_list:
        
        if ignore_default and color.is_default():
            continue
            
        obj = color_to_trigger(color)
            
        obj_list.append(obj)
        obj.update({
            obj_prop.X: x,
            obj_prop.Y: y
            })
        y += -30
    
    return obj_list
