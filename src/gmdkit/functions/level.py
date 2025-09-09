# Package Imports
from gmdkit.mappings import prop_id, color_id, obj_id, color_prop
from gmdkit.models.level import Level
from gmdkit.models.prop.color import Color
from gmdkit.models.object import ObjectList, Object


def create_color_triggers(level:Level, offset_x:float=0, offset_y:float=-30, color_filter:callable=None) -> ObjectList:
    """
    Converts a level's default colors into color triggers.

    Parameters
    ----------
    level : Level
        The level to retrieve colors from.
    offset_x : float, optional
        Horizontal offset between triggers. The default is 0.
    offset_y : float, optional
        Vertical offset between triggers. The default is -30.

    Returns
    -------
    ObjectList
        An ObjectList containing the generated color triggers.
    """

    mapping = {
        color_prop.red: prop_id.trigger.color.red,
        color_prop.green: prop_id.trigger.color.green,
        color_prop.blue: prop_id.trigger.color.blue,
        color_prop.blending: prop_id.trigger.color.blending,
        color_prop.channel: prop_id.trigger.color.channel,
        color_prop.copy_id: prop_id.trigger.color.copy_id,
        color_prop.opacity: prop_id.trigger.color.opacity,
        color_prop.hsv: prop_id.trigger.color.hsv,
        color_prop.copy_opacity: prop_id.trigger.color.copy_opacity,
        }
    
    filter_predefined = lambda color: color[color_prop.channel] not in [color_id.black, color_id.white, color_id.lighter, color_id.player_1, color_id.player_2]
        
    pool = ObjectList()
    
    x = y = 0
    
    if (colors := level.start.get(prop_id.level.colors)) is not None:
        
        color_filter = color_filter or filter_predefined
        
        for color in colors.where(color_filter):
            
            obj = Object.default(obj_id.trigger.color)
            
            pool.append(obj)
            
            for color_key, obj_key in mapping.items():
                
                if color_key in color:
                    obj[obj_key] = color[color_key]
                
                match color.get(color_prop.copy_id):
                    case 1:
                        obj[prop_id.trigger.color.player_1] = True
                    
                    case 2:
                        obj[prop_id.trigger.color.player_2] = True
                    
                    case _:
                        pass
            
            obj[prop_id.trigger.color.duration] = 0
            
            obj[prop_id.x] = x
            obj[prop_id.y] = y
            
            x += offset_x
            y += offset_y
    
    
    return pool