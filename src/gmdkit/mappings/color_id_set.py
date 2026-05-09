from . import color_id

PRESET = frozenset((
    color_id.BLACK, 
    color_id.WHITE, 
    color_id.LIGHTER, 
    color_id.LIGHT_BG, 
    color_id.PLAYER_1, 
    color_id.PLAYER_2
    ))

LEVEL = frozenset((
    color_id.BACKGROUND, 
    color_id.GROUND, 
    color_id.LINE, 
    color_id.LINE_3D, 
    color_id.OBJECT, 
    color_id.GROUND_2, 
    color_id.MIDDLEGROUND, 
    color_id.MIDDLEGROUND_2
    ))