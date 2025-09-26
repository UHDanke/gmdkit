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
    function: Callable = None
    condition: Callable = None
    default: Callable = None
    replace: Callable = None


ID_TYPES = ['color_id', 'group_id', 'item_id', 'time_id', 'collision_id', 'link_id', 'trigger_channel', 'gradient_id', 'effect_id', 'enter_channel', 'keyframe_id', 'song_id', 'sfx_id', 'unique_sfx_id', 'song_channel', 'sfx_group', 'force_id', 'material_id', 'control_id', 'remap_base', 'remap_target']


ID_RULES = {
    obj_id.trigger.COLOR: [
            IDRule(type='color_id', prop=obj_prop.trigger.color.CHANNEL, min=1, max=999),
            IDRule(type='color_id', prop=obj_prop.trigger.color.COPY_ID, min=1, max=999)
        ],
    obj_id.trigger.shader.GRAY_SCALE: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.GRAY_SCALE_TINT_CHANNEL, min=1, max=999, remappable=True)
        ],
    obj_id.trigger.shader.LENS_CIRCLE: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.LENS_CIRCLE_TINT_CHANNEL, min=1, max=999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.LENS_CIRCLE_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.shader.RADIAL_BLUR: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.RADIAL_BLUR_REF_CHANNEL, min=1, max=999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.RADIAL_BLUR_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.shader.MOTION_BLUR: [
            IDRule(type='color_id', prop=obj_prop.trigger.shader.MOTION_BLUR_REF_CHANNEL, min=1, max=999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.shader.MOTION_BLUR_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    None: [
            IDRule(type='color_id', prop=obj_prop.COLOR_1, default=lambda x: COLOR_1_DEFAULT.get(x,0), min=1, max=999),
            IDRule(type='color_id', prop=obj_prop.COLOR_2, default=lambda x: COLOR_2_DEFAULT.get(x,0), min=1, max=999),
            IDRule(type='group_id', prop=obj_prop.GROUPS, replace=lambda x, kvm: x.remap(kvm), min=1, max=9999, iterable=True),
            IDRule(type='group_id', prop=obj_prop.PARENT_GROUPS, replace=lambda x, kvm: x.remap(kvm), min=1, max=9999, iterable=True),
            IDRule(type='link_id', prop=obj_prop.LINKED_GROUP, min=1),
            IDRule(type='trigger_channel', prop=obj_prop.trigger.CHANNEL, default=0),
            IDRule(type='enter_channel', prop=obj_prop.ENTER_CHANNEL, default=0, min=-32768, max=32767),
            IDRule(type='material_id', prop=obj_prop.MATERIAL, default=0, min=-32768, max=32767),
            IDRule(type='control_id', prop=obj_prop.trigger.CONTROL_ID, default=0, remappable=True)
        ],
    obj_id.trigger.PULSE: [
            IDRule(type='color_id', prop=obj_prop.trigger.pulse.COPY_ID, min=1, max=999),
            IDRule(type='color_id', prop=obj_prop.trigger.pulse.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 0, min=1, max=999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.pulse.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.pulse.TARGET_TYPE,0) == 1, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.area.TINT: [
            IDRule(type='color_id', prop=obj_prop.trigger.effect.TINT_CHANNEL, min=1, max=999),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0)
        ],
    obj_id.trigger.enter.TINT: [
            IDRule(type='color_id', prop=obj_prop.trigger.effect.TINT_CHANNEL, min=1, max=999),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.LEVEL_START: [
            IDRule(type='color_id', prop=obj_prop.level.COLORS, function=lambda x: x.unique_values(lambda i: i.channels), replace=lambda x, kvm: x.apply(lambda i: i.remap(kvm)), min=1, max=999, iterable=True),
            IDRule(type='group_id', prop=obj_prop.level.PLAYER_SPAWN, min=1, max=9999)
        ],
    obj_id.trigger.MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_POS, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.move.TARGET_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.ALPHA: [
            IDRule(type='group_id', prop=obj_prop.trigger.alpha.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.TOGGLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.TOGGLE_BLOCK: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle_block.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.orb.TOGGLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.toggle_block.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.ON_DEATH: [
            IDRule(type='group_id', prop=obj_prop.trigger.on_death.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.SPAWN: [
            IDRule(type='group_id', prop=obj_prop.trigger.spawn.GROUP_ID, min=1, max=9999, remappable=True),
            IDRule(type='remap_base', prop=obj_prop.trigger.spawn.REMAPS, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), iterable=True),
            IDRule(type='remap_target', prop=obj_prop.trigger.spawn.REMAPS, condition=lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 1, function=lambda x: x.values(), replace=lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), iterable=True),
            IDRule(type='remap_target', prop=obj_prop.trigger.spawn.REMAPS, condition=lambda x: x.get(obj_prop.trigger.spawn.RESET_REMAP,0) == 0, function=lambda x: x.values(), replace=lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), remappable=True, iterable=True)
        ],
    obj_id.trigger.TELEPORT: [
            IDRule(type='group_id', prop=obj_prop.trigger.teleport.TARGET_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.SONG: [
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_1, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_2, min=1, max=9999, remappable=True),
            IDRule(type='song_id', prop=obj_prop.trigger.song.SONG_ID, default=0, remappable=True),
            IDRule(type='song_channel', prop=obj_prop.trigger.song.CHANNEL, default=0, min=0, max=4, remappable=True)
        ],
    obj_id.trigger.EDIT_SONG: [
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_1, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.song.GROUP_ID_2, min=1, max=9999, remappable=True),
            IDRule(type='song_channel', prop=obj_prop.trigger.song.CHANNEL, default=0, min=0, max=4, remappable=True)
        ],
    obj_id.trigger.SFX: [
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_1, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_2, min=1, max=9999, remappable=True),
            IDRule(type='sfx_id', prop=obj_prop.trigger.sfx.SFX_ID, default=0, remappable=True),
            IDRule(type='unique_sfx_id', prop=obj_prop.trigger.sfx.UNIQUE_ID, remappable=True),
            IDRule(type='sfx_group', prop=obj_prop.trigger.sfx.GROUP_ID, remappable=True)
        ],
    obj_id.trigger.EDIT_SFX: [
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_1, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP_ID_2, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.sfx.GROUP, min=1, max=9999, remappable=True),
            IDRule(type='unique_sfx_id', prop=obj_prop.trigger.sfx.UNIQUE_ID, remappable=True),
            IDRule(type='sfx_group', prop=obj_prop.trigger.sfx.GROUP_ID, remappable=True)
        ],
    obj_id.trigger.ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.ROTATE_TARGET, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.AIM_TARGET, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MIN_X_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MIN_Y_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MAX_X_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.rotate.MAX_Y_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.follow.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.follow.FOLLOW_TARGET, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.ANIMATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.animate.TARGET_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.TOUCH: [
            IDRule(type='group_id', prop=obj_prop.trigger.touch.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.COUNT: [
            IDRule(type='group_id', prop=obj_prop.trigger.count.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.count.ITEM_ID, default=0, min=0, max=9999, remappable=True)
        ],
    obj_id.trigger.INSTANT_COUNT: [
            IDRule(type='group_id', prop=obj_prop.trigger.instant_count.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.instant_count.ITEM_ID, default=0, min=0, max=9999, remappable=True)
        ],
    obj_id.trigger.FOLLOW_PLAYER_Y: [
            IDRule(type='group_id', prop=obj_prop.trigger.follow_player_y.TARGET_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.COLLISION: [
            IDRule(type='group_id', prop=obj_prop.trigger.collision.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.collision.BLOCK_A, min=1, max=9999, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.collision.BLOCK_B, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.RANDOM: [
            IDRule(type='group_id', prop=obj_prop.trigger.random.TRUE_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.random.FALSE_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.END_WALL: [
            IDRule(type='group_id', prop=obj_prop.trigger.end_wall.GROUP_ID, min=1, max=9999)
        ],
    obj_id.trigger.CAMERA_EDGE: [
            IDRule(type='group_id', prop=obj_prop.trigger.camera_edge.TARGET_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.CHECKPOINT: [
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.SPAWN_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.TARGET_POS, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.checkpoint.RESPAWN_ID, min=1, max=9999)
        ],
    obj_id.trigger.SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.scale.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.scale.CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.FOLLOW_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.MAX_RANGE_REF, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.START_SPEED_REF, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.adv_follow.START_DIR_REF, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.KEYFRAME: [
            IDRule(type='group_id', prop=obj_prop.trigger.keyframe.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.keyframe.SPAWN_ID, min=1, max=9999),
            IDRule(type='keyframe_id', prop=obj_prop.trigger.keyframe.KEY_ID, default=0, min=0)
        ],
    obj_id.trigger.ANIMATE_KEYFRAME: [
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.PARENT_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.animate_keyframe.ANIMATION_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.END: [
            IDRule(type='group_id', prop=obj_prop.trigger.end.SPAWN_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.end.TARGET_POS, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.EVENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.event.SPAWN_ID, min=1, max=9999, remappable=True),
            IDRule(type='material_id', prop=obj_prop.trigger.event.EXTRA_ID_1, default=0, remappable=True)
        ],
    obj_id.trigger.SPAWN_PARTICLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.spawn_particle.PARTICLE_GROUP, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.spawn_particle.POSITION_GROUP, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.INSTANT_COLLISION: [
            IDRule(type='group_id', prop=obj_prop.trigger.instant_collision.TRUE_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.instant_collision.FALSE_ID, min=1, max=9999, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.instant_collision.BLOCK_A, min=1, max=9999, remappable=True),
            IDRule(type='collision_id', prop=obj_prop.trigger.instant_collision.BLOCK_B, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.UI: [
            IDRule(type='group_id', prop=obj_prop.trigger.ui.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.ui.UI_TARGET, min=1, max=9999)
        ],
    obj_id.trigger.TIME: [
            IDRule(type='group_id', prop=obj_prop.trigger.time.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.time.ITEM_ID, default=0, remappable=True)
        ],
    obj_id.trigger.TIME_EVENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.time_event.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.time_event.ITEM_ID, default=0, remappable=True)
        ],
    obj_id.trigger.RESET: [
            IDRule(type='group_id', prop=obj_prop.trigger.reset.GROUP_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.OBJECT_CONTROL: [
            IDRule(type='group_id', prop=obj_prop.trigger.object_control.TARGET_ID, min=1, max=9999)
        ],
    obj_id.trigger.LINK_VISIBLE: [
            IDRule(type='group_id', prop=obj_prop.trigger.link_visible.GROUP_ID, min=1, max=9999)
        ],
    obj_id.trigger.ITEM_COMPARE: [
            IDRule(type='group_id', prop=obj_prop.trigger.item_compare.TRUE_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.item_compare.FALSE_ID, min=1, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_compare.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) in (0,1), default=0, min=0, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_compare.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_1,0) == 2, default=0, min=0, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_compare.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) in (0,1), default=0, min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_compare.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_compare.ITEM_TYPE_2,0) == 2, default=0, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.STATE_BLOCK: [
            IDRule(type='group_id', prop=obj_prop.trigger.state_block.STATE_ON, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.state_block.STATE_OFF, min=1, max=9999)
        ],
    obj_id.trigger.STATIC_CAMERA: [
            IDRule(type='group_id', prop=obj_prop.trigger.static_camera.TARGET_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.GRADIENT: [
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.U, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.D, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.L, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.gradient.R, min=1, max=9999),
            IDRule(type='gradient_id', prop=obj_prop.trigger.gradient.GRADIENT_ID, default=0)
        ],
    obj_id.trigger.shader.SHOCKWAVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.SHOCKWAVE_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.shader.SHOCKLINE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.SHOCKLINE_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.shader.BULGE: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.BULGE_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.shader.PINCH: [
            IDRule(type='group_id', prop=obj_prop.trigger.shader.PINCH_CENTER_ID, min=1, max=9999, remappable=True)
        ],
    obj_id.trigger.STOP: [
            IDRule(type='group_id', prop=obj_prop.trigger.stop.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0)== 0, min=1, max=9999, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.stop.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.stop.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.SEQUENCE: [
            IDRule(type='group_id', prop=obj_prop.trigger.sequence.SEQUENCE, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), min=1, max=9999, iterable=True)
        ],
    obj_id.trigger.ADV_RANDOM: [
            IDRule(type='group_id', prop=obj_prop.trigger.adv_random.TARGETS, function=lambda x: x.keys(), replace=lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), min=1, max=9999, iterable=True)
        ],
    obj_id.trigger.EDIT_ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.SPEED_REF, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.DIR_REF, min=1, max=9999, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.RETARGET_ADV_FOLLOW: [
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 0, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.edit_adv_follow.FOLLOW_ID, min=1, max=9999, remappable=True),
            IDRule(type='control_id', prop=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.edit_adv_follow.USE_CONTROL_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.collectible.USER_COIN: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    obj_id.collectible.KEY: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    1587: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    1589: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    1598: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    obj_id.collectible.SMALL_COIN: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    3601: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4401: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4402: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4403: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4404: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4405: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4406: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4407: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4408: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4409: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4410: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4411: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4412: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4413: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4414: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4415: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4416: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4417: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4418: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4419: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4420: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4421: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4422: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4423: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4424: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4425: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4426: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4427: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4428: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4429: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4430: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4431: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4432: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4433: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4434: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4435: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4436: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4437: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4438: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4439: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4440: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4441: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4442: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4443: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4444: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4445: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4446: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4447: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4448: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4449: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4450: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4451: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4452: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4453: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4454: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4455: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4456: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4457: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4458: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4459: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4460: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4461: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4462: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4463: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4464: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4465: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4466: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4467: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4468: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4469: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4470: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4471: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4472: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4473: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4474: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4475: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4476: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4477: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4478: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4479: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4480: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4481: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4482: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4483: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4484: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4485: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4486: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4487: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4488: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4538: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4489: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4490: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4491: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4492: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4493: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4494: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4495: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4496: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4497: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4537: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4498: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4499: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4500: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4501: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4502: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4503: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4504: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4505: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4506: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4507: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4508: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4509: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4510: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4511: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4512: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4513: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4514: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4515: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4516: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4517: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4518: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4519: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4520: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4521: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4522: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4523: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4524: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4525: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4526: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4527: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4528: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4529: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4530: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4531: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4532: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4533: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4534: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4535: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4536: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    4539: [
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.GROUP_ID, min=1, max=9999),
            IDRule(type='group_id', prop=obj_prop.trigger.collectible.PARTICLE   , min=1, max=9999),
            IDRule(type='item_id', prop=obj_prop.trigger.collectible.ITEM_ID, default=0, min=0, max=9999)
        ],
    obj_id.trigger.area.MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0)
        ],
    obj_id.trigger.area.SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0)
        ],
    obj_id.trigger.area.ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0)
        ],
    obj_id.trigger.area.FADE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.CENTER_ID, min=1, max=9999, remappable=True),
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0)
        ],
    obj_id.trigger.area.EDIT_MOVE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 0, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_SCALE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_ROTATE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 2, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_FADE: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 3, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.area.EDIT_TINT: [
            IDRule(type='group_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 4, min=1, max=9999, remappable=True),
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, condition=lambda x: x.get(obj_prop.trigger.effect.USE_EFFECT_ID,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.ITEM_EDIT: [
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) in (0,1), min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_3,0) == 2, min=1, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) in (0,1), min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.ITEM_ID_1, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_1,0) == 2, min=1, max=9999, remappable=True),
            IDRule(type='item_id', prop=obj_prop.trigger.item_edit.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) in (0,1), min=1, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_edit.ITEM_ID_2, condition=lambda x: x.get(obj_prop.trigger.item_edit.ITEM_TYPE_2,0) == 2, min=1, max=9999, remappable=True)
        ],
    obj_id.ITEM_LABEL: [
            IDRule(type='item_id', prop=obj_prop.item_label.ITEM_ID, condition=lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 0, default=0, min=0, max=9999),
            IDRule(type='time_id', prop=obj_prop.item_label.ITEM_ID, condition=lambda x: x.get(obj_prop.item_label.TIME_COUNTER,0) == 1, default=0, min=0, max=9999)
        ],
    obj_id.trigger.PICKUP: [
            IDRule(type='item_id', prop=obj_prop.trigger.pickup.ITEM_ID, default=0, min=0, max=9999, remappable=True)
        ],
    obj_id.trigger.TIME_CONTROL: [
            IDRule(type='time_id', prop=obj_prop.trigger.time_control.ITEM_ID, default=0, remappable=True)
        ],
    obj_id.trigger.ITEM_PERSIST: [
            IDRule(type='item_id', prop=obj_prop.trigger.item_persist.ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 0, default=0, min=0, max=9999, remappable=True),
            IDRule(type='time_id', prop=obj_prop.trigger.item_persist.ITEM_ID, condition=lambda x: x.get(obj_prop.trigger.item_persist.TIMER,0) == 1, default=0, remappable=True)
        ],
    obj_id.trigger.COLLISION_BLOCK: [
            IDRule(type='collision_id', prop=obj_prop.trigger.collision_block.BLOCK_ID, min=1, max=9999)
        ],
    obj_id.trigger.ARROW: [
            IDRule(type='trigger_channel', prop=obj_prop.trigger.arrow.TARGET_CHANNEL, default=0)
        ],
    obj_id.trigger.START_POSITION: [
            IDRule(type='trigger_channel', prop=obj_prop.start_pos.TARGET_CHANNEL, default=0)
        ],
    obj_id.trigger.area.STOP: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.TARGET_ID, default=0, remappable=True)
        ],
    obj_id.trigger.enter.MOVE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.trigger.enter.SCALE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.trigger.enter.ROTATE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.trigger.enter.FADE: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.trigger.enter.STOP: [
            IDRule(type='effect_id', prop=obj_prop.trigger.effect.EFFECT_ID, default=0),
            IDRule(type='enter_channel', prop=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    22: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    24: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    23: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    25: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    26: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    27: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    28: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    55: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    56: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    57: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    58: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    59: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    1915: [
            IDRule(type='enter_channel', prop=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, min=-32768, max=32767, remappable=True)
        ],
    obj_id.trigger.FORCE_BLOCK: [
            IDRule(type='force_id', prop=obj_prop.trigger.force_block.FORCE_ID, default=0)
        ],
    obj_id.trigger.FORCE_CIRCLE: [
            IDRule(type='force_id', prop=obj_prop.trigger.force_block.FORCE_ID, default=0, min=-32768, max=32767)
        ]
    }
