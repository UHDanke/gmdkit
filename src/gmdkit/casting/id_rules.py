# Imports
from typing import Callable
from dataclasses import dataclass

# Package Imports
from gmdkit.mappings import obj_id, obj_prop, color_prop
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT

@dataclass(frozen=True)
class IDRule:
    type: str
    prop: int
    min: int = -2147483648
    max: int = 2147483647
    remappable: bool = False
    iterable: bool = False
    reference: bool = False
    function: Callable = None
    condition: Callable = None
    fallback: Callable = None
    default: int = None
    replace: Callable = None


ID_TYPES = ['color_id', 'group_id', 'item_id', 'time_id', 'collision_id', 'link_id', 'trigger_channel', 'gradient_id', 'effect_id', 'enter_channel', 'keyframe_id', 'song_id', 'sfx_id', 'unique_sfx_id', 'song_channel', 'sfx_group', 'force_id', 'material_id', 'control_id', 'remap_base', 'remap_target']


ID_RULES = {
    obj_id.trigger.COLOR: [
            IDRule(type='color_id', prop=obj_prop.trigger.color.CHANNEL, min=1.0, max=1101.0),
            IDRule(type='color_id', prop=obj_prop.trigger.color.COPY_ID, min=1.0, max=1101.0, reference=True)
        ],
    obj_id.trigger.shader.GRAY_SCALE: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.GRAY_SCALE_TINT_CHANNEL, default=lambda x: 0 if x.get(obj_prop.trigger.shader.GRAY_SCALE_USE_TINT) else None, min=1.0, max=1101.0, remappable=True, reference=True)
        ],
    obj_id.trigger.shader.LENS_CIRCLE: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.LENS_CIRCLE_TINT_CHANNEL, default=0, min=1.0, max=1101.0, remappable=True, reference=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.LENS_CIRCLE_CENTER_ID, default=lambda x: 0 if not (x.get(obj_prop.trigger.shader.LENS_CIRCLE_PLAYER_1) or x.get(obj_prop.trigger.shader.LENS_CIRCLE_PLAYER_2)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.shader.RADIAL_BLUR: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.RADIAL_BLUR_REF_CHANNEL, default=0, min=1.0, max=1101.0, remappable=True, reference=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.RADIAL_BLUR_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.shader.RADIAL_BLUR_TARGET) and not (x.get(obj_prop.trigger.shader.RADIAL_BLUR_PLAYER_1) or x.get(obj_prop.trigger.shader.RADIAL_BLUR_PLAYER_2)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.shader.MOTION_BLUR: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.MOTION_BLUR_REF_CHANNEL, default=0, min=1.0, max=1101.0, remappable=True, reference=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.MOTION_BLUR_CENTER_ID, default=lambda x: 0 if not (x.get(obj_prop.trigger.shader.MOTION_BLUR_PLAYER_1) or x.get(obj_prop.trigger.shader.MOTION_BLUR_PLAYER_2) or x.get(obj_prop.trigger.shader.MOTION_BLUR_CENTER)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    None: [
            IDRule(type='color_id', prop=obj_prop.COLOR_1, fallback=lambda x: COLOR_1_DEFAULT.get(x.get(obj_prop.ID,0)), default=0, min=1.0, max=1101.0, reference=True),
            IDRule(type='color_id', prop=obj_prop.COLOR_2, fallback=lambda x: COLOR_2_DEFAULT.get(x.get(obj_prop.ID,0)), default=0, min=1.0, max=1101.0, reference=True),
            IDRule(type='group_id', prop=obj_prop.GROUPS, replace=lambda x, kvm: x.remap(kvm), min=1.0, max=9999.0, iterable=True, reference=True),
            IDRule(type='group_id', prop=obj_prop.PARENT_GROUPS, replace=lambda x, kvm: x.remap(kvm), min=1.0, max=9999.0, iterable=True, reference=True),
            IDRule(type='link_id', prop=obj_prop.LINKED_GROUP, min=1.0, reference=True),
            IDRule(type='trigger_channel', prop=obj_prop.trigger.CHANNEL, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, reference=True),
            IDRule(type='material_id', prop=obj_prop.MATERIAL, default=0, min=-32768.0, max=32767.0, reference=True),
            IDRule(type='control_id', prop=obj_prop.trigger.CONTROL_ID, default=0, remappable=True, reference=True)
        ],
    obj_id.trigger.PULSE: [
            IDRule(type='color_id', prop=obj_prop.trigger.pulse.COPY_ID, min=1.0, max=1101.0, reference=True),
            IDRule(type='color_id', prop=obj_prop.trigger.pulse.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 0, default=0, min=1.0, max=1101.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.pulse.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 1, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.area.TINT: [
            IDRule(type='color_id', prop=obj_prop.trigger.effect.TINT_CHANNEL, default=lambda x: 0 if not x.get(obj_prop.trigger.effect.ENABLE_HSV) else None, min=1.0, max=1101.0, reference=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ],
    obj_id.trigger.enter.TINT: [
            IDRule(type='color_id', prop=obj_prop.trigger.effect.TINT_CHANNEL, default=lambda x: 0 if not x.get(obj_prop.trigger.effect.ENABLE_HSV) else None, min=1.0, max=1101.0, reference=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.LEVEL_START: [
            IDRule(type='color_id', prop=obj_prop.level.COLORS, function=lambda x: [i for i in x.get_channels() if 0 < i <= 999], replace=lambda x, kvm: x.remap(kvm), min=1.0, max=1101.0, iterable=True),
            IDRule(type='color_id', prop=obj_prop.level.COLORS, function=lambda x: [i for i in x.get_channels() if i > 999], replace=lambda x, kvm: None, min=1.0, max=1101.0, iterable=True, reference=True),
            IDRule(type='group_id', prop=obj_prop.level.PLAYER_SPAWN, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_POS, default=lambda x: 0 if x.get(obj_prop.trigger.move.DIRECTION_MODE) or x.get(obj_prop.trigger.move.TARGET_MODE) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.move.DIRECTION_MODE) or x.get(obj_prop.trigger.move.TARGET_MODE) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.ALPHA: [
            IDRule(type='group_id', prop=obj_prop.trigger.alpha.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.TOGGLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.TOGGLE_BLOCK: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle_block.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.orb.TOGGLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle_block.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.ON_DEATH: [
            IDRule(type='group_id', prop=obj_prop.trigger.on_death.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.SPAWN: [
            IDRule(type='group_id', prop=obj_prop.trigger.spawn.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='remap_base', prop=obj_prop.trigger.spawn.REMAPS, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), iterable=True),
            IDRule(type='remap_target', prop=obj_prop.trigger.spawn.REMAPS, condition=lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 1, function=lambda x: x.values(), replace=lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), iterable=True),
            IDRule(type='remap_target', prop=obj_prop.trigger.spawn.REMAPS, condition=lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 0, function=lambda x: x.values(), replace=lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), remappable=True, iterable=True)
        ],
    obj_id.trigger.TELEPORT: [
            IDRule(type='group_id', prop=obj_prop.trigger.teleport.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.EDIT_SONG: [
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_1, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_2, default=lambda x: 0 if not (x.get(obj_prop.trigger.song.PLAYER_1) or x.get(obj_prop.trigger.song.PLAYER_2) or x.get(obj_prop.trigger.song.CAMERA)) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='song_channel', prop=obj_prop.trigger.song.CHANNEL, default=0, min=0.0, max=4.0, remappable=True)
        ],
    obj_id.trigger.SFX: [
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_1, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_2, default=lambda x: 0 if not (x.get(obj_prop.trigger.sfx.PLAYER_1) or x.get(obj_prop.trigger.sfx.PLAYER_2) or x.get(obj_prop.trigger.sfx.CAMERA)) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='sfx_id', prop=obj_prop.trigger.sfx.SFX_ID, default=0, remappable=True, reference=True),
            IDRule(type='unique_sfx_id', prop=obj_prop.trigger.sfx.UNIQUE_ID, default=0, remappable=True, reference=True),
            IDRule(type='sfx_group', prop=obj_prop.trigger.sfx.GROUP_ID, default=0, remappable=True)
        ],
    obj_id.trigger.EDIT_SFX: [
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_1, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_2, default=lambda x: 0 if not (x.get(obj_prop.trigger.sfx.PLAYER_1) or x.get(obj_prop.trigger.sfx.PLAYER_2) or x.get(obj_prop.trigger.sfx.CAMERA)) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='unique_sfx_id', prop=obj_prop.trigger.sfx.UNIQUE_ID, default=0, remappable=True),
            IDRule(type='sfx_group', prop=obj_prop.trigger.sfx.GROUP_ID, default=0, remappable=True)
        ],
    obj_id.trigger.ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.CENTER_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.AIM_TARGET, default=lambda x: 0 if x.get(obj_prop.trigger.rotate.AIM_MODE) or x.get(obj_prop.trigger.rotate.FOLLOW_MODE) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MIN_X_ID, default=lambda x: 0 if x.get(obj_prop.trigger.rotate.AIM_MODE) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MIN_Y_ID, default=lambda x: 0 if x.get(obj_prop.trigger.rotate.AIM_MODE) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MAX_X_ID, default=lambda x: 0 if x.get(obj_prop.trigger.rotate.AIM_MODE) else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MAX_Y_ID, default=lambda x: 0 if x.get(obj_prop.trigger.rotate.AIM_MODE) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.follow.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.follow.FOLLOW_TARGET, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.ANIMATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.animate.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.TOUCH: [
            IDRule(type='group_id', prop=obj_prop.trigger.touch.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.COUNT: [
            IDRule(type='group_id', prop=obj_prop.trigger.count.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.count.ITEM_ID, default=0, min=0.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.INSTANT_COUNT: [
            IDRule(type='group_id', prop=obj_prop.trigger.instant_count.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.instant_count.ITEM_ID, default=0, min=0.0, max=9999.0, remappable=True, reference=True)
        ],
    obj_id.trigger.FOLLOW_PLAYER_Y: [
            IDRule(type='group_id', prop=obj_prop.trigger.follow_player_y.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.COLLISION: [
            IDRule(type='group_id', prop=obj_prop.trigger.collision.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.collision.BLOCK_A, default=lambda x: 0 if not (x.get(obj_prop.trigger.collision.PLAYER_1) or x.get(obj_prop.trigger.collision.PLAYER_2) or x.get(obj_prop.trigger.collision.BETWEEN_PLAYERS)) else None , min=1.0, max=9999.0, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.collision.BLOCK_B, default=lambda x: 0 if not x.get(obj_prop.trigger.collision.BETWEEN_PLAYERS) else None , min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.RANDOM: [
            IDRule(type='group_id', prop=obj_prop.trigger.random.TRUE_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.random.FALSE_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.END_WALL: [
            IDRule(type='group_id', prop=obj_prop.trigger.end_wall.GROUP_ID, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.CAMERA_EDGE: [
            IDRule(type='group_id', prop=obj_prop.trigger.camera_edge.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.CHECKPOINT: [
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.SPAWN_ID, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.TARGET_POS, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.RESPAWN_ID, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.scale.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.scale.CENTER_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.FOLLOW_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.MAX_RANGE_REF, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.START_SPEED_REF, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.START_DIR_REF, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.KEYFRAME: [
            IDRule(type='group_id', prop=obj_prop.trigger.keyframe.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.keyframe.INDEX,0) == 1 else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.keyframe.SPAWN_ID, default=0, min=1.0, max=9999.0),
            IDRule(type='keyframe_id', prop=obj_prop.trigger.keyframe.KEY_ID, default=0, min=0.0, reference=True)
        ],
    obj_id.trigger.ANIMATE_KEYFRAME: [
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.PARENT_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.ANIMATION_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.END: [
            IDRule(type='group_id', prop=obj_prop.trigger.end.SPAWN_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.end.TARGET_POS, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.EVENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.event.SPAWN_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='material_id', prop=obj_prop.trigger.event.EXTRA_ID_1, default=0, remappable=True)
        ],
    obj_id.trigger.SPAWN_PARTICLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.spawn_particle.PARTICLE_GROUP, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.spawn_particle.POSITION_GROUP, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.INSTANT_COLLISION: [
            IDRule(type='group_id', prop=obj_prop.trigger.instant_collision.TRUE_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.instant_collision.FALSE_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.instant_collision.BLOCK_A, default=lambda x: 0 if not (x.get(obj_prop.trigger.instant_collision.PLAYER_1) or x.get(obj_prop.trigger.instant_collision.PLAYER_2) or x.get(obj_prop.trigger.instant_collision.BETWEEN_PLAYERS)) else None , min=1.0, max=9999.0, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.instant_collision.BLOCK_B, default=lambda x: 0 if not x.get(obj_prop.trigger.instant_collision.BETWEEN_PLAYERS) else None , min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.UI: [
            IDRule(type='group_id', prop=obj_prop.trigger.ui.GROUP_ID, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.ui.UI_TARGET, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.TIME: [
            IDRule(type='group_id', prop=obj_prop.trigger.time.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.time.ITEM_ID, default=0, remappable=True, reference=True)
        ],
    obj_id.trigger.TIME_EVENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.time_event.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.time_event.ITEM_ID, default=0, remappable=True, reference=True)
        ],
    obj_id.trigger.RESET: [
            IDRule(type='group_id', prop=obj_prop.trigger.reset.GROUP_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.OBJECT_CONTROL: [
            IDRule(type='group_id', prop=obj_prop.trigger.object_control.TARGET_ID, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.LINK_VISIBLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.link_visible.GROUP_ID, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.ITEM_COMPARE: [
            IDRule(type='group_id', prop=obj_prop.trigger.item_compare.TRUE_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.item_compare.FALSE_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_compare.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) in (0,1), default=0, min=0.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_compare.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) == 2, default=0, min=0.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_compare.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) in (0,1), default=0, min=1.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_compare.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) == 2, default=0, min=1.0, max=9999.0, remappable=True, reference=True)
        ],
    obj_id.trigger.STATE_BLOCK: [
            IDRule(type='group_id', prop=obj_prop.trigger.state_block.STATE_ON, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.state_block.STATE_OFF, default=0, min=1.0, max=9999.0)
        ],
    obj_id.trigger.STATIC_CAMERA: [
            IDRule(type='group_id', prop=obj_prop.trigger.static_camera.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.GRADIENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.U, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.D, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.L, default=0, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.R, default=0, min=1.0, max=9999.0),
            IDRule(type='gradient_id', prop=obj_prop.trigger.gradient.GRADIENT_ID, default=0, min=0.0, max=1000.0, reference=True)
        ],
    obj_id.trigger.shader.SHOCKWAVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.SHOCKWAVE_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.shader.SHOCKWAVE_TARGET) and not (x.get(obj_prop.trigger.shader.SHOCKWAVE_PLAYER_1) or x.get(obj_prop.trigger.shader.SHOCKWAVE_PLAYER_2)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.shader.SHOCKLINE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.SHOCKLINE_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.shader.SHOCKLINE_TARGET) and not (obj_prop.trigger.shader.SHOCKLINE_PLAYER_1 or obj_prop.trigger.shader.SHOCKLINE_PLAYER_2) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.shader.BULGE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.BULGE_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.shader.BULGE_TARGET) and not (x.get(obj_prop.trigger.shader.BULGE_PLAYER_1) or x.get(obj_prop.trigger.shader.BULGE_PLAYER_2)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.shader.PINCH: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.PINCH_CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.shader.PINCH_TARGET) and not (x.get(obj_prop.trigger.shader.PINCH_PLAYER_1) or x.get(obj_prop.trigger.shader.PINCH_PLAYER_2)) else None, min=1.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.STOP: [
            IDRule(type='group_id', prop=obj_prop.trigger.stop.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0)== 0, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.stop.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.SEQUENCE: [
            IDRule(type='group_id', prop=obj_prop.trigger.sequence.SEQUENCE, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), min=1.0, max=9999.0, iterable=True)
        ],
    obj_id.trigger.ADV_RANDOM: [
            IDRule(type='group_id', prop=obj_prop.trigger.adv_random.TARGETS, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), min=1.0, max=9999.0, iterable=True)
        ],
    obj_id.trigger.EDIT_ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.SPEED_REF, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.DIR_REF, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.RETARGET_ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.FOLLOW_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.collectible.USER_COIN: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    obj_id.collectible.KEY: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    1587: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    1589: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    1598: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    obj_id.collectible.SMALL_COIN: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    3601: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4401: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4402: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4403: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4404: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4405: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4406: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4407: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4408: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4409: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4410: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4411: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4412: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4413: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4414: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4415: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4416: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4417: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4418: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4419: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4420: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4421: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4422: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4423: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4424: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4425: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4426: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4427: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4428: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4429: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4430: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4431: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4432: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4433: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4434: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4435: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4436: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4437: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4438: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4439: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4440: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4441: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4442: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4443: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4444: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4445: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4446: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4447: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4448: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4449: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4450: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4451: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4452: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4453: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4454: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4455: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4456: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4457: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4458: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4459: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4460: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4461: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4462: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4463: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4464: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4465: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4466: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4467: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4468: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4469: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4470: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4471: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4472: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4473: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4474: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4475: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4476: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4477: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4478: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4479: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4480: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4481: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4482: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4483: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4484: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4485: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4486: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4487: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4488: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4538: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4489: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4490: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4491: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4492: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4493: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4494: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4495: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4496: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4497: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4537: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4498: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4499: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4500: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4501: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4502: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4503: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4504: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4505: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4506: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4507: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4508: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4509: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4510: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4511: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4512: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4513: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4514: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4515: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4516: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4517: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4518: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4519: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4520: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4521: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4522: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4523: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4524: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4525: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4526: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4527: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4528: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4529: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4530: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4531: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4532: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4533: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4534: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4535: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4536: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    4539: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, default=lambda x: 0 if x.get(obj_prop.trigger.collectible.TOGGLE_TRIGGER) else None, min=1.0, max=9999.0),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , default=0, min=1.0, max=9999.0),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0.0, max=9999.0)
        ],
    obj_id.trigger.area.MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ],
    obj_id.trigger.area.SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ],
    obj_id.trigger.area.ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ],
    obj_id.trigger.area.FADE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, default=lambda x: 0 if x.get(obj_prop.trigger.effect.SPECIAL_CENTER) is None else None, min=1.0, max=9999.0, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ],
    obj_id.trigger.area.EDIT_MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 0, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 2, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_FADE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 3, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_TINT: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 4, default=0, min=1.0, max=9999.0, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.ITEM_EDIT: [
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) in (0,1), min=1.0, max=9999.0, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) == 2, min=1.0, max=9999.0, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) in (0,1), min=1.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) == 2, min=1.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) in (0,1), min=1.0, max=9999.0, remappable=True, reference=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) == 2, min=1.0, max=9999.0, remappable=True, reference=True)
        ],
    obj_id.ITEM_LABEL: [
            IDRule(type='item_id', prop=obj_prop.item_label.ITEM_ID, condition=lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 0, default=0, min=0.0, max=9999.0, reference=True),
            IDRule(type='time_id', prop=obj_prop.item_label.ITEM_ID, condition=lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 1, default=0, min=0.0, max=9999.0, reference=True)
        ],
    obj_id.trigger.PICKUP: [
            IDRule(type='item_id', prop=obj_prop.trigger.pickup.ITEM_ID, default=0, min=0.0, max=9999.0, remappable=True)
        ],
    obj_id.trigger.TIME_CONTROL: [
            IDRule(type='time_id', prop=obj_prop.trigger.time_control.ITEM_ID, default=0, remappable=True)
        ],
    obj_id.trigger.ITEM_PERSIST: [
            IDRule(type='item_id', prop=obj_prop.trigger.item_persist.ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 0, default=0, min=0.0, max=9999.0, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_persist.ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.COLLISION_BLOCK: [
            IDRule(type='collision_id', prop=obj_prop.trigger.collision_block.BLOCK_ID, default=0, min=1.0, max=9999.0, reference=True)
        ],
    obj_id.trigger.ARROW: [
            IDRule(type='trigger_channel', prop=obj_prop.trigger.arrow.TARGET_CHANNEL, default=0, reference=True)
        ],
    obj_id.trigger.START_POSITION: [
            IDRule(type='trigger_channel', prop=obj_prop.start_pos.TARGET_CHANNEL, default=0)
        ],
    obj_id.trigger.area.STOP: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, remappable=True, reference=True)
        ],
    obj_id.trigger.enter.MOVE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.trigger.enter.SCALE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.trigger.enter.ROTATE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.trigger.enter.FADE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.trigger.enter.STOP: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    22: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    24: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    23: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    25: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    26: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    27: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    28: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    55: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    56: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    57: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    58: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    59: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    1915: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768.0, max=32767.0, remappable=True)
        ],
    obj_id.trigger.SONG: [
            IDRule(type='song_id', prop=obj_prop.trigger.song.SONG_ID, default=0, remappable=True, reference=True),
            IDRule(type='song_channel', prop=obj_prop.trigger.song.CHANNEL, default=0, min=0.0, max=4.0, remappable=True, reference=True)
        ],
    obj_id.trigger.FORCE_BLOCK: [
            IDRule(type='force_id', prop=obj_prop.trigger.force_block.FORCE_ID, default=0, reference=True)
        ],
    obj_id.trigger.FORCE_CIRCLE: [
            IDRule(type='force_id', prop=obj_prop.trigger.force_block.FORCE_ID, default=0, min=-32768.0, max=32767.0, reference=True)
        ]
    }
