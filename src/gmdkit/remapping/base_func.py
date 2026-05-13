# Imports
from typing import Optional, Any

# Package Imports
from gmdkit.models.object import Object
from gmdkit.models.prop.color import Color, ColorList
from gmdkit.models.prop.list import IntPairList
from gmdkit.mappings import obj_prop
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT


def get_collectible_default_item_id(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.collectible.PICKUP_ITEM) else None

def get_collectible_default_group_id(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None

def get_area_default_center(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None

def get_rotate_default_aim(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.rotate.AIM_MODE) else None

def get_gray_scale_default_color(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.shader.GRAY_SCALE_USE_TINT) else None

def get_effect_tint_channel(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.effect.ENABLE_HSV) else None

def get_move_default_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.move.DIRECTION_MODE) or
        obj.get(obj_prop.trigger.move.TARGET_MODE)
        ) else None

def get_song_default_volume_group(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.song.PLAYER_1) or 
        obj.get(obj_prop.trigger.song.PLAYER_2) or 
        obj.get(obj_prop.trigger.song.CAMERA)
        ) else None

def get_sfx_default_volume_group(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.sfx.PLAYER_1) or 
        obj.get(obj_prop.trigger.sfx.PLAYER_2) or 
        obj.get(obj_prop.trigger.sfx.CAMERA)
        ) else None

def get_rotate_default_aim_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.rotate.AIM_MODE) or 
        obj.get(obj_prop.trigger.rotate.FOLLOW_MODE)
        ) else None

def get_default_keyframe_group(obj:Object) -> Optional[int]:
    return 0 if obj.get(obj_prop.trigger.keyframe.INDEX,0) == 1 else None

def get_default_shockwave_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.shader.SHOCKWAVE_TARGET) 
        and not (
            obj.get(obj_prop.trigger.shader.SHOCKWAVE_PLAYER_1) or 
            obj.get(obj_prop.trigger.shader.SHOCKWAVE_PLAYER_2)
        )) else None

def get_default_shockline_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.shader.SHOCKLINE_TARGET) 
        and not (
            obj.get(obj_prop.trigger.shader.SHOCKLINE_PLAYER_1) or 
            obj.get(obj_prop.trigger.shader.SHOCKLINE_PLAYER_2)
        )) else None

def get_default_lens_circle_target(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.shader.LENS_CIRCLE_PLAYER_1) or 
        obj.get(obj_prop.trigger.shader.LENS_CIRCLE_PLAYER_2)
        ) else None

def get_default_radial_blur_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.shader.RADIAL_BLUR_TARGET) 
        and not (
            obj.get(obj_prop.trigger.shader.RADIAL_BLUR_PLAYER_1) or 
            obj.get(obj_prop.trigger.shader.RADIAL_BLUR_PLAYER_2)
        )) else None

def get_default_motion_blur_target(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.shader.MOTION_BLUR_PLAYER_1) or 
        obj.get(obj_prop.trigger.shader.MOTION_BLUR_PLAYER_2) or 
        obj.get(obj_prop.trigger.shader.MOTION_BLUR_CENTER)
        ) else None

def get_default_bulge_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.shader.BULGE_TARGET) 
        and not (
            obj.get(obj_prop.trigger.shader.BULGE_PLAYER_1) or 
            obj.get(obj_prop.trigger.shader.BULGE_PLAYER_2)
        )) else None

def get_default_pinch_target(obj:Object) -> Optional[int]:
    return 0 if (
        obj.get(obj_prop.trigger.shader.PINCH_TARGET) 
        and not (
            obj.get(obj_prop.trigger.shader.PINCH_PLAYER_1) or 
            obj.get(obj_prop.trigger.shader.PINCH_PLAYER_2)
            )) else None

def get_default_collision_block_a(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.collision.PLAYER_1) or 
        obj.get(obj_prop.trigger.collision.PLAYER_2) or 
        obj.get(obj_prop.trigger.collision.BETWEEN_PLAYERS)
        ) else None

def get_default_collision_block_b(obj:Object) -> Optional[int]:
    return 0 if not obj.get(obj_prop.trigger.collision.BETWEEN_PLAYERS) else None 

def get_default_instant_coll_block_a(obj:Object) -> Optional[int]:
    return 0 if not (
        obj.get(obj_prop.trigger.instant_collision.PLAYER_1) or 
        obj.get(obj_prop.trigger.instant_collision.PLAYER_2) or 
        obj.get(obj_prop.trigger.instant_collision.BETWEEN_PLAYERS)
        ) else None

def get_default_instant_coll_block_b(obj:Object) -> Optional[int]:
    return 0 if not obj.get(obj_prop.trigger.instant_collision.BETWEEN_PLAYERS) else None 

def get_default_gradient(obj:Object) -> Optional[int]:
    return 0 if not obj.get(obj_prop.trigger.gradient.DISABLE_ALL) else None
    
def custom_color(color_id:int) -> bool:
    if color_id is None:
        return False
    return (1 <= color_id <= 999)

def special_color(color_id:int) -> bool:
    if color_id is None:
        return False
    return not (1 <= color_id <= 999)

def get_one_color_channel(color:Color) -> Optional[int]:
    return (color.channel,)

def get_one_color_copy(color:Color) -> Optional[int]:
    return (color.copy_id,)

def get_color_channels(color_list:ColorList) -> set[int]:
    return color_list.unique_values(get_one_color_channel)    

def get_color_copies(color_list:ColorList) -> set[int]:
    return color_list.unique_values(get_one_color_copy)

def get_custom_color_channels(color_list:ColorList) -> set[int]:
    return {i for i in get_color_channels(color_list) if custom_color(i)}

def get_custom_color_copies(color_list:ColorList) -> set[int]:
    return {i for i in get_color_copies(color_list) if custom_color(i)}

def get_special_color_channels(color_list:ColorList) -> set[int]:
    return {i for i in get_color_channels(color_list) if special_color(i)}

def get_special_color_copies(color_list:ColorList) -> set[int]:
    return {i for i in get_color_channels(color_list) if special_color(i)}

def remap_custom_color_channels(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.channel
        if custom_color(i):
            color.channel = kvm.get(i,i)
    return color_list

def remap_custom_color_copies(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.copy_id
        if custom_color(i):
            color.copy_id = kvm.get(i,i)
    return color_list

def remap_special_color_channels(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.channel
        if special_color(i):
            color.channel = kvm.get(i,i)
    return color_list
           
def remap_special_base_color_copies(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.copy_id
        if special_color(i):
            color.copy_id = kvm.get(i,i)
    return color_list

def get_base_color(obj:Object) -> int:
    return COLOR_1_DEFAULT.get(obj.get(obj_prop.ID,0))

def get_secondary_color(obj:Object) -> int:
    return COLOR_2_DEFAULT.get(obj.get(obj_prop.ID,0))

def get_keys(obj:Object) -> list[int]:
    return obj.keys()

def get_values(obj:Object) -> list[int]:
    return obj.values()

def obj_can_be_spawned(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.SPAWN_TRIGGER, False)
    
def spawn_keep_remap(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.spawn.RESET_REMAP, False)

def instant_coll_keep_remap(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.instant_collision.DONT_RESET_REMAP, False)

def area_use_effect_id(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.effect.USE_EFFECT_ID, False)

def area_use_group_id(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.effect.USE_EFFECT_ID, False)

def pulse_target_channel(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.pulse.TARGET_TYPE, False)

def pulse_target_group(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.pulse.TARGET_TYPE, False)

def stop_use_group(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.stop.USE_CONTROL_ID, False)

def stop_use_control_id(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.stop.USE_CONTROL_ID, False)

def edit_adv_follow_use_group(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID, False)

def edit_adv_follow_use_control_id(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID, False)

def item_edit_target_is_item(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) in (0,1)

def item_edit_target_is_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) == 2

def item_edit_first_is_item(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) in (0,1)

def item_edit_first_is_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) == 2

def item_edit_second_is_item(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) in (0,1)

def item_edit_second_is_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) == 2

def item_label_display_item(obj:Object) -> bool:
    return not obj.get(obj_prop.item_label.TIME_COUNTER, False)

def item_label_display_timer(obj:Object) -> bool:
    return obj.get(obj_prop.item_label.TIME_COUNTER, False)

def item_compare_first_is_item(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) in (0,1)

def item_compare_first_is_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) == 2

def item_compare_second_is_item(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) in (0,1)

def item_compare_second_is_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) == 2

def item_persist_item(obj:Object) -> bool:
    return not obj.get(obj_prop.trigger.item_persist.TIMER, False)

def item_persist_timer(obj:Object) -> bool:
    return obj.get(obj_prop.trigger.item_persist.TIMER, False)

def remap(remappable:Any, kvm:dict[int,int]):
    remappable.remap(kvm)
    return remappable
    
def remap_pairs_keys(pairs:IntPairList, kvm:dict[int,int]):
    pairs.remap_keys(kvm)
    return pairs

def remap_pairs_vals(pairs:IntPairList, kvm:dict[int,int]):
    pairs.remap_vals(kvm)
    return pairs
    
