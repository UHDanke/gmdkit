# Package Imports
from gmdkit.mappings import obj_prop, color_id, obj_id, color_prop
from gmdkit.models.level import Level
from gmdkit.models.prop.color import Color
from gmdkit.models.object import ObjectList, Object


def create_color_triggers(level:Level, pos_x:float=0, pos_y:float=0, offset_x:float=0, offset_y:float=-30, color_filter:callable=None) -> ObjectList:
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
    
    filter_predefined = lambda color: color[color_prop.CHANNEL] not in [color_id.BLACK, color_id.WHITE, color_id.LIGHTER, color_id.PLAYER_1, color_id.PLAYER_2]
        
    pool = ObjectList()
    
    x = pos_x
    y = pos_y
    
    if (colors := level.start.get(obj_prop.level.COLORS)) is not None:
        
        color_filter = color_filter or filter_predefined
        
        for color in colors.where(color_filter):
            
            obj = Object.default(obj_id.trigger.COLOR)
            
            pool.append(obj)
            
            for color_key, obj_key in mapping.items():
                
                if color_key in color:
                    obj[obj_key] = color[color_key]
                
                match color.get(color_prop.COPY_ID):
                    case 1:
                        obj[obj_prop.trigger.color.PLAYER_1] = True
                    
                    case 2:
                        obj[obj_prop.trigger.color.PLAYER_2] = True
                    
                    case _:
                        pass
            
            obj[obj_prop.trigger.color.DURATION] = 0
            
            obj[obj_prop.X] = x
            obj[obj_prop.Y] = y
            
            x += offset_x
            y += offset_y
    
    
    return pool
        
        
        
        