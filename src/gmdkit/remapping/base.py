# Imports
from typing import Optional, Any

# Package Imports
from gmdkit.models import interfaces as I
from gmdkit.models.interfaces.enter import EnterTrigger
from gmdkit.models.interfaces.base import LevelSettings
from gmdkit.models.interfaces.audio import VolumeInterface
from gmdkit.remapping.classes import RuleHandler
from gmdkit.remapping.types import IDType, IDActions
from gmdkit.models.object import Object
from gmdkit.models.prop.color import Color, ColorList
from gmdkit.models.prop.list import IntPairList
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT
from gmdkit.remapping.types import AutoID
 

ID_RULES = RuleHandler()
register = ID_RULES.register_rule
 
 
# BaseObject
def _get_base_color(intf:I.BaseObject) -> int:
    return COLOR_1_DEFAULT.get(intf.obj_id)
 
def _special_color(color_id:int) -> bool:
    if color_id is None:
        return False
    elif isinstance(color_id, AutoID):
        return False
    return not (1 <= color_id <= 999)
 
def _get_secondary_color(intf:I.BaseObject) -> int:
    return COLOR_2_DEFAULT.get(intf.obj_id)
 
def _remap(remappable:Any, kvm:dict[int,int]):
    remappable.remap(kvm)
    return remappable
 
register(I.BaseObject, 'color_1', id_type=IDType.COLOR_ID, fallback=_get_base_color, fixed=_special_color, when_unset=True, reference=True, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
register(I.BaseObject, 'color_2', id_type=IDType.COLOR_ID, fallback=_get_secondary_color, fixed=_special_color, when_unset=True, reference=True, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
register(I.BaseObject, 'groups', id_type=IDType.GROUP_ID, replace=_remap, iterable=True, reference=True, id_min=1, id_max=9999)
register(I.BaseObject, 'parent_groups', id_type=IDType.GROUP_ID, replace=_remap, iterable=True, reference=True, id_min=1, id_max=9999)
register(I.BaseObject, 'linked_group', id_type=IDType.LINK_ID, reference=True, id_min=1)
register(I.BaseObject, 'enter_channel', id_type=IDType.ENTER_CHANNEL, when_unset=True, reference=True, id_min=-32768, id_max=32767)
register(I.BaseObject, 'material', id_type=IDType.MATERIAL_ID, when_unset=True, reference=True, id_min=-32768, id_max=32767)
 
 
# LevelSettings
def _custom_color(color_id:int) -> bool:
    if color_id is None:
        return False
    elif isinstance(color_id, AutoID):
        return True
    return (1 <= color_id <= 999)
 
def _get_one_color_channel(color:Color) -> Optional[int]:
    return (color.channel,)
 
def _get_color_channels(color_list:ColorList) -> set[int]:
    return color_list.unique_values(_get_one_color_channel)
 
def _get_custom_color_channels(color_list:ColorList) -> set[int]:
    return {i for i in _get_color_channels(color_list) if _custom_color(i)}
 
def _remap_custom_color_channels(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.channel
        if _custom_color(i):
            color.channel = kvm.get(i,i)
    return color_list
 
def _get_one_color_copy(color:Color) -> Optional[int]:
    return (color.copy_id,)
 
def _get_color_copies(color_list:ColorList) -> set[int]:
    return color_list.unique_values(_get_one_color_copy)
 
def _get_custom_color_copies(color_list:ColorList) -> set[int]:
    return {i for i in _get_color_copies(color_list) if _custom_color(i)}
 
def _remap_custom_color_copies(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.copy_id
        if _custom_color(i):
            color.copy_id = kvm.get(i,i)
    return color_list
 
def _get_special_color_channels(color_list:ColorList) -> set[int]:
    return {i for i in _get_color_channels(color_list) if _special_color(i)}
 
def _remap_special_color_channels(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.channel
        if _special_color(i):
            color.channel = kvm.get(i,i)
    return color_list
 
def _get_special_color_copies(color_list:ColorList) -> set[int]:
    return {i for i in _get_color_channels(color_list) if _special_color(i)}
 
def _remap_special_base_color_copies(color_list:ColorList, kvm:dict[int,int]):
    for color in color_list:
        i = color.copy_id
        if _special_color(i):
            color.copy_id = kvm.get(i,i)
    return color_list
 
register(LevelSettings, 'colors', id_type=IDType.COLOR_ID, function=_get_custom_color_channels, replace=_remap_custom_color_channels, iterable=True, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
register(LevelSettings, 'colors', id_type=IDType.COLOR_ID, function=_get_custom_color_copies, replace=_remap_custom_color_copies, iterable=True, reference=True, id_min=1, id_max=1101, actions=(IDActions.FOLLOW_ALPHA, IDActions.FOLLOW_COLOR,))
register(LevelSettings, 'colors', id_type=IDType.COLOR_ID, function=_get_special_color_channels, replace=_remap_special_color_channels, fixed=True, iterable=True, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
register(LevelSettings, 'colors', id_type=IDType.COLOR_ID, function=_get_special_color_copies, replace=_remap_special_base_color_copies, fixed=True, iterable=True, reference=True, id_min=1, id_max=1101, actions=(IDActions.FOLLOW_ALPHA, IDActions.FOLLOW_COLOR,))
register(LevelSettings, 'player_spawn', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# VolumeInterface
def _has_default_volume_group(intf) -> bool:
    # VolumeInterface (song and sfx triggers)
    return not (intf.player_1 or intf.player_2 or intf.camera)
 
register(VolumeInterface, 'group_id_1', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(VolumeInterface, 'group_id_2', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_volume_group, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# EffectObject
register(I.EffectObject, 'channel', id_type=IDType.TRIGGER_CHANNEL, when_unset=True, reference=True)
register(I.EffectObject, 'control_id', id_type=IDType.CONTROL_ID, remappable=True, when_unset=True, reference=True)
 
 
# StartPosition
register(I.StartPosition, 'target_channel', id_type=IDType.TRIGGER_CHANNEL, when_unset=True, actions=IDActions.SET_ITEM)
 
 
# AdvancedFollowTrigger
register(I.AdvancedFollowTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.MOVE)
register(I.AdvancedFollowTrigger, 'follow_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.AdvancedFollowTrigger, 'max_range_ref', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.AdvancedFollowTrigger, 'start_speed_ref', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_MOVE)
register(I.AdvancedFollowTrigger, 'start_dir_ref', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# AdvancedRandomTrigger
def _get_keys(obj:Object) -> list[int]:
    return obj.keys()
 
def _remap_pairs_keys(pairs:IntPairList, kvm:dict[int,int]):
    pairs.remap_keys(kvm)
    return pairs
 
register(I.AdvancedRandomTrigger, 'group_weights', id_type=IDType.GROUP_ID, function=_get_keys, replace=_remap_pairs_keys, iterable=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
 
 
# AlphaTrigger
register(I.AlphaTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.ALPHA)
 
 
# AnimateKeyframeTrigger
register(I.AnimateKeyframeTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.ROTATE, IDActions.SCALE, IDActions.MOVE,))
register(I.AnimateKeyframeTrigger, 'parent_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.FOLLOW_SCALE, IDActions.FOLLOW_ROTATE,))
register(I.AnimateKeyframeTrigger, 'animation_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.KEYFRAME)
 
 
# AnimateTrigger
register(I.AnimateTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.ANIMATE)
 
 
# BulgeShader
def _has_default_bulge_target(intf) -> bool:
    return bool(intf.target) and not (intf.player_1 or intf.player_2)
 
register(I.BulgeShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_bulge_target, id_min=1, id_max=9999)
 
 
# CameraEdgeTrigger
register(I.CameraEdgeTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# CheckpointTrigger
register(I.CheckpointTrigger, 'spawn_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.CheckpointTrigger, 'target_pos', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.CheckpointTrigger, 'respawn_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
 
 
# CollectibleObject
def _has_collectible_default_group_id(intf) -> bool:
    return bool(intf.toggle_trigger)
 
def _has_collectible_default_item_id(intf) -> bool:
    return bool(intf.pickup_item)
 
register(I.CollectibleObject, 'group_id', id_type=IDType.GROUP_ID, when_unset=_has_collectible_default_group_id, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
register(I.CollectibleObject, 'particle', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.PARTICLES)
register(I.CollectibleObject, 'item_id', id_type=IDType.ITEM_ID, when_unset=_has_collectible_default_item_id, id_min=0, id_max=9999, actions=IDActions.SET_ITEM)
 
 
# CollisionBlock
register(I.CollisionBlock, 'block_id', id_type=IDType.COLLISION_ID, when_unset=True, reference=True, id_min=0, id_max=9999)
 
 
# CollisionTrigger
def _has_default_collision_block_a(intf) -> bool:
    return not (intf.player_1 or intf.player_2 or intf.between_players)
 
def _has_default_collision_block_b(intf) -> bool:
    return not intf.between_players
 
register(I.CollisionTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
register(I.CollisionTrigger, 'block_a', id_type=IDType.COLLISION_ID, remappable=True, when_unset=_has_default_collision_block_a, id_min=0, id_max=9999, actions=IDActions.TRACK_COLLISION)
register(I.CollisionTrigger, 'block_b', id_type=IDType.COLLISION_ID, remappable=True, when_unset=_has_default_collision_block_b, id_min=0, id_max=9999, actions=IDActions.TRACK_COLLISION)
 
 
# ColorTrigger
register(I.ColorTrigger, 'color_channel', id_type=IDType.COLOR_ID, fixed=_special_color, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
register(I.ColorTrigger, 'copy_id', id_type=IDType.COLOR_ID, fixed=_special_color, reference=True, id_min=1, id_max=1101, actions=(IDActions.ALPHA, IDActions.COLOR,))
 
 
# CountTrigger
register(I.CountTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
register(I.CountTrigger, 'item_id', id_type=IDType.ITEM_ID, remappable=True, when_unset=True, id_min=0, id_max=9999, actions=IDActions.TRACK_ITEM)
 
 
# EditAdvancedFollowTrigger
def _edit_adv_follow_use_group(intf:I.EditAdvancedFollowTrigger) -> bool:
    return not intf.use_control_id
 
def _edit_adv_follow_use_control_id(intf:I.EditAdvancedFollowTrigger) -> bool:
    return intf.use_control_id
 
register(I.EditAdvancedFollowTrigger, 'target_id', id_type=IDType.GROUP_ID, condition=_edit_adv_follow_use_group, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.EditAdvancedFollowTrigger, 'speed_ref', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.EditAdvancedFollowTrigger, 'dir_ref', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.EditAdvancedFollowTrigger, 'target_id', id_type=IDType.CONTROL_ID, condition=_edit_adv_follow_use_control_id, remappable=True, when_unset=True)
 
 
# EndTrigger
register(I.EndTrigger, 'spawn_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.EndTrigger, 'target_pos', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# EndWallTrigger
register(I.EndWallTrigger, 'group_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999)
 
 
# EnterPreset
register(I.EnterPreset, 'enter_channel', id_type=IDType.ENTER_CHANNEL, remappable=True, when_unset=True, id_min=-32768, id_max=32767)
 
 
# EventTrigger
register(I.EventTrigger, 'spawn_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.EventTrigger, 'extra_id_1', id_type=IDType.MATERIAL_ID, remappable=True, when_unset=True)
 
 
# FollowPlayerYTrigger
register(I.FollowPlayerYTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.MOVE)
 
 
# FollowTrigger
register(I.FollowTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.MOVE)
register(I.FollowTrigger, 'follow_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_MOVE)
 
 
# ForceBlock
register(I.ForceBlock, 'force_id', id_type=IDType.FORCE_ID, when_unset=True, reference=True, id_min=-32768, id_max=32767)
 
 
# GameplayArrow
register(I.GameplayArrow, 'target_channel', id_type=IDType.TRIGGER_CHANNEL, when_unset=True, reference=True, actions=IDActions.SET_ITEM)
 
 
# GradientTrigger
def _has_default_gradient(intf) -> bool:
    return not intf.disable_all
 
register(I.GradientTrigger, 'bl_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.GradientTrigger, 'br_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.GradientTrigger, 'tl_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.GradientTrigger, 'tr_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.GradientTrigger, 'gradient_id', id_type=IDType.GRADIENT_ID, when_unset=_has_default_gradient, reference=True, id_min=0, id_max=1000)
 
 
# GrayScaleShader
def _has_gray_scale_default_color(intf) -> bool:
    return bool(intf.use_tint)
 
register(I.GrayScaleShader, 'tint_channel', id_type=IDType.COLOR_ID, fixed=_special_color, remappable=True, when_unset=_has_gray_scale_default_color, reference=True, id_min=1, id_max=1101, actions=IDActions.COLOR)
 
 
# InstantCollisionTrigger
def _has_default_instant_coll_block_a(intf) -> bool:
    return not (intf.player_1 or intf.player_2 or intf.between_players)
 
def _has_default_instant_coll_block_b(intf) -> bool:
    return not intf.between_players
 
register(I.InstantCollisionTrigger, 'true_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.InstantCollisionTrigger, 'false_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.InstantCollisionTrigger, 'block_a', id_type=IDType.COLLISION_ID, remappable=True, when_unset=_has_default_instant_coll_block_a, id_min=0, id_max=9999, actions=IDActions.CHECK_COLLISION)
register(I.InstantCollisionTrigger, 'block_b', id_type=IDType.COLLISION_ID, remappable=True, when_unset=_has_default_instant_coll_block_b, id_min=0, id_max=9999, actions=IDActions.CHECK_COLLISION)
 
 
# InstantCountTrigger
register(I.InstantCountTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
register(I.InstantCountTrigger, 'item_id', id_type=IDType.ITEM_ID, remappable=True, when_unset=True, reference=True, id_min=0, id_max=9999, actions=IDActions.GET_ITEM)
 
 
# ItemCompareTrigger
def _item_compare_first_is_item(intf:I.ItemCompareTrigger) -> bool:
    return intf.item_type_1 in (0,1)
 
def _item_compare_first_is_timer(intf:I.ItemCompareTrigger) -> bool:
    return intf.item_type_1 == 2
 
def _item_compare_second_is_item(intf:I.ItemCompareTrigger) -> bool:
    return intf.item_type_2 in (0,1)
 
def _item_compare_second_is_timer(intf:I.ItemCompareTrigger) -> bool:
    return intf.item_type_2 == 2
 
register(I.ItemCompareTrigger, 'true_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.ItemCompareTrigger, 'false_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.ItemCompareTrigger, 'item_id_1', id_type=IDType.ITEM_ID, condition=_item_compare_first_is_item, remappable=True, when_unset=True, reference=True, id_min=0, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemCompareTrigger, 'item_id_1', id_type=IDType.TIME_ID, condition=_item_compare_first_is_timer, remappable=True, when_unset=True, reference=True, id_min=0, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemCompareTrigger, 'item_id_2', id_type=IDType.ITEM_ID, condition=_item_compare_second_is_item, remappable=True, when_unset=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemCompareTrigger, 'item_id_2', id_type=IDType.TIME_ID, condition=_item_compare_second_is_timer, remappable=True, when_unset=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
 
 
# ItemEditTrigger
def _item_edit_target_is_item(intf:I.ItemEditTrigger) -> bool:
    return intf.target_item_type in (0,1)
 
def _item_edit_target_is_timer(intf:I.ItemEditTrigger) -> bool:
    return intf.target_item_type == 2
 
def _item_edit_first_is_item(intf:I.ItemEditTrigger) -> bool:
    return intf.item_type_1 in (0,1)
 
def _item_edit_first_is_timer(intf:I.ItemEditTrigger) -> bool:
    return intf.item_type_1 == 2
 
def _item_edit_second_is_item(intf:I.ItemEditTrigger) -> bool:
    return intf.item_type_2 in (0,1)
 
def _item_edit_second_is_timer(intf:I.ItemEditTrigger) -> bool:
    return intf.item_type_2 == 2
 
register(I.ItemEditTrigger, 'target_item_id', id_type=IDType.ITEM_ID, condition=_item_edit_target_is_item, remappable=True, id_min=1, id_max=9999, actions=IDActions.SET_ITEM)
register(I.ItemEditTrigger, 'target_item_id', id_type=IDType.TIME_ID, condition=_item_edit_target_is_timer, remappable=True, id_min=1, id_max=9999, actions=IDActions.SET_ITEM)
register(I.ItemEditTrigger, 'item_id_1', id_type=IDType.ITEM_ID, condition=_item_edit_first_is_item, remappable=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemEditTrigger, 'item_id_1', id_type=IDType.TIME_ID, condition=_item_edit_first_is_timer, remappable=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemEditTrigger, 'item_id_2', id_type=IDType.ITEM_ID, condition=_item_edit_second_is_item, remappable=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
register(I.ItemEditTrigger, 'item_id_2', id_type=IDType.TIME_ID, condition=_item_edit_second_is_timer, remappable=True, reference=True, id_min=1, id_max=9999, actions=IDActions.GET_ITEM)
 
 
# ItemLabel
def _item_label_display_item(intf:I.ItemLabel) -> bool:
    return not intf.time_counter
 
def _item_label_display_timer(intf:I.ItemLabel) -> bool:
    return intf.time_counter
 
register(I.ItemLabel, 'item_id', id_type=IDType.ITEM_ID, condition=_item_label_display_item, when_unset=True, reference=True, id_min=0, id_max=9999, actions=IDActions.SET_ITEM)
register(I.ItemLabel, 'item_id', id_type=IDType.TIME_ID, condition=_item_label_display_timer, when_unset=True, reference=True, id_min=0, id_max=9999, actions=IDActions.SET_ITEM)
 
 
# ItemPersistTrigger
def _item_persist_item(intf:I.ItemPersistTrigger) -> bool:
    return not intf.timer
 
def _item_persist_timer(intf:I.ItemPersistTrigger) -> bool:
    return intf.timer
 
register(I.ItemPersistTrigger, 'item_id', id_type=IDType.ITEM_ID, condition=_item_persist_item, remappable=True, when_unset=True, id_min=0, id_max=9999, actions=IDActions.PERSIST_ITEM)
register(I.ItemPersistTrigger, 'item_id', id_type=IDType.TIME_ID, condition=_item_persist_timer, remappable=True, when_unset=True, actions=IDActions.PERSIST_ITEM)
 
 
# KeyframeObject
def _has_default_keyframe_group(intf) -> bool:
    return intf.index == 1
 
register(I.KeyframeObject, 'group_id', id_type=IDType.GROUP_ID, when_unset=_has_default_keyframe_group, id_min=1, id_max=9999, actions=(IDActions.ROTATE, IDActions.SCALE, IDActions.MOVE,))
register(I.KeyframeObject, 'spawn_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.KeyframeObject, 'key_id', id_type=IDType.KEYFRAME_ID, when_unset=True, reference=True, id_min=0)
 
 
# LensCircleShader
def _has_default_lens_circle_target(intf) -> bool:
    return not (intf.player_1 or intf.player_2)
 
register(I.LensCircleShader, 'tint_channel', id_type=IDType.COLOR_ID, fixed=_special_color, remappable=True, when_unset=True, reference=True, id_min=1, id_max=1101, actions=IDActions.COLOR)
register(I.LensCircleShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_lens_circle_target, id_min=1, id_max=9999)
 
 
# LinkVisibleTrigger
register(I.LinkVisibleTrigger, 'group_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999)
 
 
# MotionBlurShader
def _has_default_motion_blur_target(intf) -> bool:
    return not (intf.player_1 or intf.player_2 or intf.center)
 
register(I.MotionBlurShader, 'ref_channel', id_type=IDType.COLOR_ID, fixed=_special_color, remappable=True, when_unset=True, reference=True, id_min=1, id_max=1101, actions=IDActions.COLOR)
register(I.MotionBlurShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_motion_blur_target, id_min=1, id_max=9999)
 
 
# MoveTrigger
def _has_move_default_target(intf) -> bool:
    return bool(intf.direction_mode or intf.target_mode)
 
register(I.MoveTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.FOLLOW_POSITION, IDActions.MOVE,))
register(I.MoveTrigger, 'target_pos', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_move_default_target, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.MoveTrigger, 'target_center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_move_default_target, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# ObjectControlTrigger
register(I.ObjectControlTrigger, 'target_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999)
 
 
# OnDeathTrigger
register(I.OnDeathTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
 
 
# PickupTrigger
register(I.PickupTrigger, 'item_id', id_type=IDType.ITEM_ID, remappable=True, when_unset=True, id_min=0, id_max=9999, actions=IDActions.SET_ITEM)
 
 
# PinchShader
def _has_default_pinch_target(intf) -> bool:
    return bool(intf.target) and not (intf.player_1 or intf.player_2)
 
register(I.PinchShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_pinch_target, id_min=1, id_max=9999)
 
 
# PulseTrigger
def _pulse_target_channel(intf:I.PulseTrigger) -> bool:
    return not intf.target_type
 
def _pulse_target_group(intf:I.PulseTrigger) -> bool:
    return intf.target_type
 
register(I.PulseTrigger, 'copy_id', id_type=IDType.COLOR_ID, fixed=_special_color, reference=True, id_min=1, id_max=1101, actions=IDActions.COLOR)
register(I.PulseTrigger, 'target_id', id_type=IDType.COLOR_ID, condition=_pulse_target_channel, fixed=_special_color, remappable=True, when_unset=True, id_min=1, id_max=1101, actions=IDActions.FOLLOW_COLOR)
register(I.PulseTrigger, 'target_id', id_type=IDType.GROUP_ID, condition=_pulse_target_group, remappable=True, when_unset=True, id_min=1, id_max=9999)
 
 
# RadialBlurShader
def _has_default_radial_blur_target(intf) -> bool:
    return bool(intf.target) and not (intf.player_1 or intf.player_2)
 
register(I.RadialBlurShader, 'ref_channel', id_type=IDType.COLOR_ID, fixed=_special_color, remappable=True, when_unset=True, reference=True, id_min=1, id_max=1101, actions=IDActions.COLOR)
register(I.RadialBlurShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_radial_blur_target, id_min=1, id_max=9999)
 
 
# RandomTrigger
register(I.RandomTrigger, 'true_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.RandomTrigger, 'false_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
 
 
# ResetTrigger
register(I.ResetTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.RESET)
 
 
# RetargetAdvancedFollowTrigger
register(I.RetargetAdvancedFollowTrigger, 'target_id', id_type=IDType.GROUP_ID, condition=_edit_adv_follow_use_group, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.RetargetAdvancedFollowTrigger, 'follow_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.RetargetAdvancedFollowTrigger, 'target_id', id_type=IDType.CONTROL_ID, condition=_edit_adv_follow_use_control_id, remappable=True, when_unset=True)
 
 
# RotateTrigger
def _has_rotate_default_aim_target(intf) -> bool:
    return bool(intf.aim_mode or intf.follow_mode)
 
def _has_rotate_default_aim(intf) -> bool:
    return bool(intf.aim_mode)
 
register(I.RotateTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.FOLLOW_POSITION, IDActions.ROTATE, IDActions.MOVE,))
register(I.RotateTrigger, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.RotateTrigger, 'aim_target', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_rotate_default_aim_target, id_min=1, id_max=9999)
register(I.RotateTrigger, 'min_x_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_rotate_default_aim, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.RotateTrigger, 'min_y_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_rotate_default_aim, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.RotateTrigger, 'max_x_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_rotate_default_aim, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.RotateTrigger, 'max_y_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_rotate_default_aim, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# ScaleTrigger
register(I.ScaleTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SCALE, IDActions.MOVE,))
register(I.ScaleTrigger, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# SequenceTrigger
register(I.SequenceTrigger, 'sequence', id_type=IDType.GROUP_ID, function=_get_keys, replace=_remap_pairs_keys, iterable=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
 
 
# ShockLineShader
def _has_default_shockline_target(intf) -> bool:
    return bool(intf.target) and not (intf.player_1 or intf.player_2)
 
register(I.ShockLineShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_shockline_target, id_min=1, id_max=9999)
 
 
# ShockwaveShader
def _has_default_shockwave_target(intf) -> bool:
    return bool(intf.target) and not (intf.player_1 or intf.player_2)
 
register(I.ShockwaveShader, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_default_shockwave_target, id_min=1, id_max=9999)
 
 
# SongTrigger
register(I.SongTrigger, 'song_id', id_type=IDType.SONG_ID, remappable=True, when_unset=True, reference=True)
register(I.SongTrigger, 'channel', id_type=IDType.SONG_CHANNEL, remappable=True, when_unset=True, reference=True, id_min=0, id_max=4)
 
 
# SpawnParticleTrigger
register(I.SpawnParticleTrigger, 'particle_group', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.PARTICLES)
register(I.SpawnParticleTrigger, 'position_group', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# SpawnTrigger
def _get_values(obj:Object) -> list[int]:
    return obj.values()
 
def _remap_pairs_vals(pairs:IntPairList, kvm:dict[int,int]):
    pairs.remap_vals(kvm)
    return pairs
 
def _spawn_keep_remap(intf:I.SpawnTrigger) -> bool:
    return not intf.reset_remap
 
register(I.SpawnTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.SpawnTrigger, 'remaps', id_type=IDType.REMAP_BASE, function=_get_keys, replace=_remap_pairs_keys, iterable=True)
register(I.SpawnTrigger, 'remaps', id_type=IDType.REMAP_TARGET, function=_get_values, replace=_remap_pairs_vals, remappable=_spawn_keep_remap, iterable=True)
 
 
# StateBlock
register(I.StateBlock, 'state_on', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.StateBlock, 'state_off', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
 
 
# StaticCameraTrigger
register(I.StaticCameraTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
 
 
# StopAreaTrigger
register(I.StopAreaTrigger, 'effect_id', id_type=IDType.EFFECT_ID, remappable=True, when_unset=True, reference=True, actions=IDActions.STOP_EFFECT)
 
 
# StopEnterTrigger
register(I.StopEnterTrigger, 'effect_id', id_type=IDType.EFFECT_ID, when_unset=True, actions=IDActions.STOP_EFFECT)
register(I.StopEnterTrigger, 'enter_channel', id_type=IDType.ENTER_CHANNEL, remappable=True, when_unset=True, id_min=-32768, id_max=32767)
 
 
# StopTrigger
def _stop_use_group(intf:I.StopTrigger) -> bool:
    return not intf.use_control_id
 
def _stop_use_control_id(intf:I.StopTrigger) -> bool:
    return intf.use_control_id
 
register(I.StopTrigger, 'target_id', id_type=IDType.GROUP_ID, condition=_stop_use_group, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.STOP)
register(I.StopTrigger, 'target_id', id_type=IDType.CONTROL_ID, condition=_stop_use_control_id, remappable=True, when_unset=True, actions=IDActions.STOP)
 
 
# TimerControlTrigger
register(I.TimerControlTrigger, 'item_id', id_type=IDType.TIME_ID, remappable=True, when_unset=True)
 
 
# TimerEventTrigger
register(I.TimerEventTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.TimerEventTrigger, 'item_id', id_type=IDType.TIME_ID, remappable=True, when_unset=True, reference=True, actions=IDActions.TRACK_ITEM)
 
 
# TimerTrigger
register(I.TimerTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.SPAWN)
register(I.TimerTrigger, 'item_id', id_type=IDType.TIME_ID, remappable=True, when_unset=True, reference=True, actions=IDActions.SET_ITEM)
 
 
# ToggleBlock
register(I.ToggleBlock, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
 
 
# ToggleTrigger
register(I.ToggleTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.TOGGLE)
 
 
# TouchTrigger
register(I.TouchTrigger, 'group_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
 
 
# UITrigger
register(I.UITrigger, 'group_id', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.UITrigger, 'ui_target', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.UI, IDActions.MOVE,))
 
 
# AreaTrigger
def _has_area_default_center(intf:I.area.AreaTrigger) -> bool:
    return not intf.special_center
 
register(I.area.AreaTrigger, 'center_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=_has_area_default_center, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
register(I.area.AreaTrigger, 'effect_id', id_type=IDType.EFFECT_ID, when_unset=True, reference=True)
 
 
# EditAreaTrigger
def _area_use_group_id(intf:I.area.EditAreaTrigger) -> bool:
    return not intf.use_effect_id
 
def _area_use_effect_id(intf:I.area.EditAreaTrigger) -> bool:
    return intf.use_effect_id
 
register(I.area.EditAreaTrigger, 'target_id', id_type=IDType.GROUP_ID, condition=_area_use_group_id, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.EDIT_EFFECT)
register(I.area.EditAreaTrigger, 'target_id', id_type=IDType.EFFECT_ID, condition=_area_use_effect_id, remappable=True, when_unset=True, actions=IDActions.EDIT_EFFECT)
 
 
# EditSFXTrigger
register(I.EditSFXTrigger, 'sfx_group', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999)
register(I.EditSFXTrigger, 'unique_id', id_type=IDType.UNIQUE_SFX_ID, remappable=True, when_unset=True)
register(I.EditSFXTrigger, 'group_id', id_type=IDType.SFX_GROUP, remappable=True, when_unset=True)
 
 
# EditSongTrigger
register(I.EditSongTrigger, 'channel', id_type=IDType.SONG_CHANNEL, remappable=True, when_unset=True, id_min=0, id_max=4)
 
 
# EnterTrigger
register(EnterTrigger, 'effect_id', id_type=IDType.EFFECT_ID, when_unset=True, reference=True)
 
 
# SFXTrigger
register(I.SFXTrigger, 'sfx_id', id_type=IDType.SFX_ID, remappable=True, when_unset=True, reference=True)
register(I.SFXTrigger, 'unique_id', id_type=IDType.UNIQUE_SFX_ID, remappable=True, when_unset=True, reference=True)
 
 
# TeleportTrigger
register(I.TeleportTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# EnterTintTrigger
def _has_effect_tint_channel(intf) -> bool:
    return bool(intf.enable_hsv)
 
register(I.EnterTintTrigger, 'tint_channel', id_type=IDType.COLOR_ID, fixed=_special_color, when_unset=_has_effect_tint_channel, reference=True, id_min=1, id_max=1101, actions=IDActions.FOLLOW_COLOR)
 
 
# TeleportOrb
register(I.TeleportOrb, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# UnlinkedTeleportPortal
register(I.UnlinkedTeleportPortal, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.FOLLOW_POSITION)
 
 
# AreaFadeTrigger
register(I.AreaFadeTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.ALPHA)
 
 
# AreaTintTrigger
register(I.AreaTintTrigger, 'tint_channel', id_type=IDType.COLOR_ID, fixed=_special_color, when_unset=_has_effect_tint_channel, reference=True, id_min=1, id_max=1101, actions=IDActions.FOLLOW_COLOR)
register(I.AreaTintTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.COLOR)
 
 
# SmallCoin
register(I.SmallCoin, 'group_id', id_type=IDType.GROUP_ID, when_unset=_has_collectible_default_group_id, id_min=1, id_max=9999, actions=(IDActions.SPAWN, IDActions.TOGGLE,))
register(I.SmallCoin, 'particle', id_type=IDType.GROUP_ID, when_unset=True, id_min=1, id_max=9999, actions=IDActions.PARTICLES)
register(I.SmallCoin, 'item_id', id_type=IDType.ITEM_ID, when_unset=_has_collectible_default_item_id, id_min=0, id_max=9999, actions=IDActions.SET_ITEM)
 
 
# AreaMoveTrigger
register(I.AreaMoveTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=IDActions.MOVE)
 
 
# AreaRotateTrigger
register(I.AreaRotateTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.ROTATE, IDActions.MOVE,))
 
 
# AreaScaleTrigger
register(I.AreaScaleTrigger, 'target_id', id_type=IDType.GROUP_ID, remappable=True, when_unset=True, id_min=1, id_max=9999, actions=(IDActions.SCALE, IDActions.MOVE,))