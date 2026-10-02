# Package Imports
from gmdkit.models.level import Level
from gmdkit.models.object import ObjectList
from gmdkit.models.prop.color import Color, ColorList
from gmdkit import remapping
from gmdkit.models import interfaces

RGBA = tuple[int,int,int,float]

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


def create_color_triggers(
        color_list:ColorList,
        ignore_default:bool=True,
        ignore_ids:None=None,
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

        if ignore_ids is not None and color.channel in ignore_ids:
            continue

        if ignore_default and color.is_default():
            continue
        
        intf = interfaces.ColorTrigger.from_color(color)
        intf.x = x
        intf.y = y
        y += -30
        obj_list.append(intf.obj)

    return obj_list


def create_lvl_color_triggers(
        lvl:Level,
        ignore_default:bool=True,
        pos_x:float=0,
        pos_y:float=0
        ) -> ObjectList:
    intf = lvl.start.require_interface(interfaces.LevelSettings)
    lvl.objects += create_color_triggers(intf.colors,ignore_default,pos_x,pos_y)


def set_used_colors(lvl:Level):
    used = remapping.rules.COLOR_ID_HANDLER.compile_ids(lvl).filter_values(reference=True).get_ids()
    intf = lvl.start.require_interface(interfaces.LevelSettings)
    intf.colors.set_defaults(*used)


def free_unused_colors(lvl:Level, ignore_ids:dict):
    ignore_ids = ignore_ids or {}

    rules = remapping.rules.BASE_ID_HANDLER.compile_rules(id_types=(remapping.IDType.COLOR_ID,))

    ids = rules.compile_ids(lvl.objects, by_type=False).filter_values(fixed=False)
    id_base = ids.filter_values(reference=False).get_ids()
    id_ref = ids.filter_values(reference=True).get_ids()
    unused = id_base - id_ref - ignore_ids
    
    intf = lvl.start.require_interface(interfaces.LevelSettings)
    intf.colors.exclude(lambda color: color.channel in unused)
