# Package Imports
from gmdkit.mappings import obj_id, obj_prop
from gmdkit.utils.id_classes import IDRule, RuleHandler
from gmdkit.utils.id_functions import (
    remap_custom_color_channels,
    item_edit_first_is_timer,
    edit_adv_follow_use_group,
    get_rotate_default_aim_target,
    get_secondary_color,
    get_default_keyframe_group,
    area_use_effect_id,
    special_color,
    get_default_radial_blur_target,
    get_keys,
    pulse_target_group,
    item_persist_timer,
    item_compare_second_is_item,
    stop_use_control_id,
    item_edit_target_is_item,
    item_compare_second_is_timer,
    remap_special_color_channels,
    get_default_shockwave_target,
    item_compare_first_is_timer,
    get_default_collision_block_b,
    spawn_keep_remap,
    get_song_default_volume_group,
    stop_use_group,
    item_persist_item,
    get_default_instant_coll_block_b,
    remap,
    get_values,
    get_rotate_default_aim,
    item_edit_target_is_timer,
    get_default_motion_blur_target,
    get_area_default_center,
    get_gray_scale_default_color,
    item_edit_second_is_timer,
    item_edit_first_is_item,
    edit_adv_follow_use_control_id,
    item_label_display_item,
    item_compare_first_is_item,
    get_default_collision_block_a,
    get_move_default_target,
    item_edit_second_is_item,
    get_default_instant_coll_block_a,
    remap_pairs_keys,
    get_special_color_channels,
    get_default_bulge_target,
    get_collectible_default_item_id,
    remap_custom_color_copies,
    item_label_display_timer,
    get_default_shockline_target,
    get_base_color,
    get_default_pinch_target,
    get_default_lens_circle_target,
    get_collectible_default_group_id,
    remap_special_base_color_copies,
    pulse_target_channel,
    get_sfx_default_volume_group,
    get_custom_color_channels,
    area_use_group_id,
    get_special_color_copies,
    get_custom_color_copies,
    get_effect_tint_channel,
    remap_pairs_vals
)


ID_TYPES = {'trigger_channel', 'control_id', 'sfx_group', 'song_id', 'gradient_id', 'collision_id', 'color_id', 'group_id', 'song_channel', 'remap_target', 'material_id', 'link_id', 'time_id', 'unique_sfx_id', 'effect_id', 'item_id', 'enter_channel', 'remap_base', 'keyframe_id', 'sfx_id', 'force_id'}
    

ID_RULES = RuleHandler(
    base = (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.COLOR_1, fallback=get_base_color, default=0, actions={'get_alpha', 'get_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.COLOR_2, fallback=get_secondary_color, default=0, actions={'get_alpha', 'get_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.GROUPS, replace=remap, id_min=1, id_max=9999, iterable=True, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.PARENT_GROUPS, replace=remap, id_min=1, id_max=9999, iterable=True, reference=True),
            IDRule(id_type='link_id', obj_prop_id=obj_prop.LINKED_GROUP, id_min=1, reference=True),
            IDRule(id_type='trigger_channel', obj_prop_id=obj_prop.trigger.CHANNEL, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.ENTER_CHANNEL, default=0, id_min=-32768, id_max=32767, reference=True),
            IDRule(id_type='material_id', obj_prop_id=obj_prop.MATERIAL, default=0, id_min=-32768, id_max=32767, reference=True),
            IDRule(id_type='control_id', obj_prop_id=obj_prop.trigger.CONTROL_ID, default=0, remappable=True, reference=True)
        ),
    by_id = {
        obj_id.trigger.COLOR: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.color.CHANNEL, actions={'set_color', 'set_alpha'}, fixed=special_color, id_min=1, id_max=1101),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.color.COPY_ID, actions={'get_alpha', 'get_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True)
        ),
    obj_id.trigger.shader.GRAY_SCALE: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.shader.GRAY_SCALE_TINT_CHANNEL, default=get_gray_scale_default_color, actions={'get_color'}, fixed=special_color, remappable=True, id_min=1, id_max=1101, reference=True)
        ,),
    obj_id.trigger.shader.LENS_CIRCLE: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.shader.LENS_CIRCLE_TINT_CHANNEL, default=0, actions={'get_color'}, fixed=special_color, remappable=True, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.LENS_CIRCLE_CENTER_ID, default=get_default_lens_circle_target, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.shader.RADIAL_BLUR: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.shader.RADIAL_BLUR_REF_CHANNEL, default=0, actions={'get_color'}, fixed=special_color, remappable=True, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.RADIAL_BLUR_CENTER_ID, default=get_default_radial_blur_target, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.shader.MOTION_BLUR: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.shader.MOTION_BLUR_REF_CHANNEL, default=0, actions={'get_color'}, fixed=special_color, remappable=True, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.MOTION_BLUR_CENTER_ID, default=get_default_motion_blur_target, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.PULSE: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.pulse.COPY_ID, actions={'get_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.pulse.TARGET_ID, condition=pulse_target_channel, default=0, actions={'use_color'}, fixed=special_color, remappable=True, id_min=1, id_max=1101),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.pulse.TARGET_ID, condition=pulse_target_group, default=0, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.area.TINT: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.effect.TINT_CHANNEL, default=get_effect_tint_channel, actions={'use_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.CENTER_ID, default=get_area_default_center, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'color_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ),
    obj_id.trigger.enter.TINT: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.trigger.effect.TINT_CHANNEL, default=get_effect_tint_channel, actions={'use_color'}, fixed=special_color, id_min=1, id_max=1101, reference=True),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    obj_id.LEVEL_START: (
            IDRule(id_type='color_id', obj_prop_id=obj_prop.level.COLORS, function=get_custom_color_channels, replace=remap_custom_color_channels, actions={'set_color', 'set_alpha'}, id_min=1, id_max=1101, iterable=True),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.level.COLORS, function=get_custom_color_copies, replace=remap_custom_color_copies, actions={'track_alpha', 'track_color'}, id_min=1, id_max=1101, iterable=True, reference=True),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.level.COLORS, function=get_special_color_channels, replace=remap_special_color_channels, actions={'set_color', 'set_alpha'}, fixed=True, id_min=1, id_max=1101, iterable=True),
            IDRule(id_type='color_id', obj_prop_id=obj_prop.level.COLORS, function=get_special_color_copies, replace=remap_special_base_color_copies, actions={'track_alpha', 'track_color'}, fixed=True, id_min=1, id_max=1101, iterable=True, reference=True),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.level.PLAYER_SPAWN, default=0, actions={'get_position'}, id_min=1, id_max=9999)
        ),
    obj_id.trigger.MOVE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.move.TARGET_ID, default=0, actions={'get_position', 'move', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.move.TARGET_POS, default=get_move_default_target, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.move.TARGET_CENTER_ID, default=get_move_default_target, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.ALPHA: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.alpha.GROUP_ID, default=0, actions={'alpha'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.TOGGLE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.toggle.GROUP_ID, default=0, actions={'toggle'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.TOGGLE_BLOCK: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.toggle_block.GROUP_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.orb.TOGGLE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.toggle_block.GROUP_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.ON_DEATH: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.on_death.GROUP_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.SPAWN: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.spawn.GROUP_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='remap_base', obj_prop_id=obj_prop.trigger.spawn.REMAPS, function=get_keys, replace=remap_pairs_keys, iterable=True),
            IDRule(id_type='remap_target', obj_prop_id=obj_prop.trigger.spawn.REMAPS, function=get_values, replace=remap_pairs_vals, remappable=spawn_keep_remap, iterable=True)
        ),
    obj_id.trigger.TELEPORT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.teleport.TARGET_ID, default=0, actions={'get_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ,),
    747: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.teleport.TARGET_ID, default=0, actions={'get_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ,),
    2902: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.teleport.TARGET_ID, default=0, actions={'get_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ,),
    3027: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.teleport.TARGET_ID, default=0, actions={'get_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.EDIT_SONG: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.song.GROUP_ID_1, default=0, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.song.GROUP_ID_2, default=get_song_default_volume_group, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='song_channel', obj_prop_id=obj_prop.trigger.song.CHANNEL, default=0, remappable=True, id_min=0, id_max=4)
        ),
    obj_id.trigger.SFX: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID_1, default=0, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID_2, default=get_sfx_default_volume_group, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='sfx_id', obj_prop_id=obj_prop.trigger.sfx.SFX_ID, default=0, remappable=True, reference=True),
            IDRule(id_type='unique_sfx_id', obj_prop_id=obj_prop.trigger.sfx.UNIQUE_ID, default=0, remappable=True, reference=True),
            IDRule(id_type='sfx_group', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID, default=0, remappable=True)
        ),
    obj_id.trigger.EDIT_SFX: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID_1, default=0, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID_2, default=get_sfx_default_volume_group, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sfx.GROUP, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='unique_sfx_id', obj_prop_id=obj_prop.trigger.sfx.UNIQUE_ID, default=0, remappable=True),
            IDRule(id_type='sfx_group', obj_prop_id=obj_prop.trigger.sfx.GROUP_ID, default=0, remappable=True)
        ),
    obj_id.trigger.ROTATE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.TARGET_ID, default=0, actions={'get_position', 'move', 'get_rand', 'rotate'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.CENTER_ID, default=0, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.AIM_TARGET, default=get_rotate_default_aim_target, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.MIN_X_ID, default=get_rotate_default_aim, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.MIN_Y_ID, default=get_rotate_default_aim, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.MAX_X_ID, default=get_rotate_default_aim, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.rotate.MAX_Y_ID, default=get_rotate_default_aim, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.FOLLOW: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.follow.TARGET_ID, default=0, actions={'move'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.follow.FOLLOW_TARGET, default=0, actions={'get_move'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.ANIMATE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.animate.TARGET_ID, default=0, actions={'animate'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.TOUCH: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.touch.GROUP_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.COUNT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.count.TARGET_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.count.ITEM_ID, default=0, actions={'track_value'}, remappable=True, id_min=0, id_max=9999)
        ),
    obj_id.trigger.INSTANT_COUNT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.instant_count.TARGET_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.instant_count.ITEM_ID, default=0, actions={'get_value'}, remappable=True, id_min=0, id_max=9999, reference=True)
        ),
    obj_id.trigger.FOLLOW_PLAYER_Y: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.follow_player_y.TARGET_ID, default=0, actions={'move'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.COLLISION: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collision.TARGET_ID, default=0, actions={'spawn', 'toggle'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='collision_id', obj_prop_id=obj_prop.trigger.collision.BLOCK_A, default=get_default_collision_block_a, actions={'track_collision'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='collision_id', obj_prop_id=obj_prop.trigger.collision.BLOCK_B, default=get_default_collision_block_b, actions={'track_collision'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.RANDOM: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.random.TRUE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.random.FALSE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.END_WALL: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.end_wall.GROUP_ID, default=0, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.CAMERA_EDGE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.camera_edge.TARGET_ID, default=0, actions={'track_position'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.CHECKPOINT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.checkpoint.SPAWN_ID, default=0, actions={'spawn'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.checkpoint.TARGET_POS, default=0, actions={'get_position'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.checkpoint.RESPAWN_ID, default=0, actions={'spawn'}, id_min=1, id_max=9999)
        ),
    obj_id.trigger.SCALE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.scale.TARGET_ID, default=0, actions={'scale', 'move'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.scale.CENTER_ID, default=0, actions={'track_position'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.ADV_FOLLOW: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_follow.TARGET_ID, default=0, actions={'move_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_follow.FOLLOW_ID, default=0, actions={'track_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_follow.MAX_RANGE_REF, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_follow.START_SPEED_REF, default=0, actions={'get_move'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_follow.START_DIR_REF, default=0, actions={'get_position', 'get_rand'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.KEYFRAME: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.keyframe.GROUP_ID, default=get_default_keyframe_group, actions={'move', 'rotate', 'scale'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.keyframe.SPAWN_ID, default=0, actions={'spawn'}, id_min=1, id_max=9999),
            IDRule(id_type='keyframe_id', obj_prop_id=obj_prop.trigger.keyframe.KEY_ID, default=0, id_min=0, reference=True)
        ),
    obj_id.trigger.ANIMATE_KEYFRAME: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.animate_keyframe.TARGET_ID, default=0, actions={'move', 'rotate', 'scale'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.animate_keyframe.PARENT_ID, default=0, actions={'get_scale', 'get_rotate'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.animate_keyframe.ANIMATION_ID, default=0, actions={'get_keyframes'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.END: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.end.SPAWN_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.end.TARGET_POS, default=0, actions={'get_position'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.EVENT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.event.SPAWN_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='material_id', obj_prop_id=obj_prop.trigger.event.EXTRA_ID_1, default=0, remappable=True)
        ),
    obj_id.trigger.SPAWN_PARTICLE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.spawn_particle.PARTICLE_GROUP, default=0, actions={'get_particles'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.spawn_particle.POSITION_GROUP, default=0, actions={'get_position'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.INSTANT_COLLISION: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.instant_collision.TRUE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.instant_collision.FALSE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='collision_id', obj_prop_id=obj_prop.trigger.instant_collision.BLOCK_A, default=get_default_instant_coll_block_a, actions={'check_collision'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='collision_id', obj_prop_id=obj_prop.trigger.instant_collision.BLOCK_B, default=get_default_instant_coll_block_b, actions={'check_collision'}, remappable=True, id_min=1, id_max=9999)
        ),
    obj_id.trigger.UI: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.ui.GROUP_ID, default=0, actions={'get_position'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.ui.UI_TARGET, default=0, actions={'move', 'set_ui'}, id_min=1, id_max=9999)
        ),
    obj_id.trigger.TIME: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.time.TARGET_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.time.ITEM_ID, default=0, actions={'set_value'}, remappable=True, reference=True)
        ),
    obj_id.trigger.TIME_EVENT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.time_event.TARGET_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.time_event.ITEM_ID, default=0, actions={'track_value'}, remappable=True, reference=True)
        ),
    obj_id.trigger.RESET: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.reset.GROUP_ID, default=0, actions={'reset'}, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.OBJECT_CONTROL: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.object_control.TARGET_ID, default=0, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.LINK_VISIBLE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.link_visible.GROUP_ID, default=0, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.ITEM_COMPARE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.item_compare.TRUE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.item_compare.FALSE_ID, default=0, actions={'spawn'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_compare.ITEM_ID_1, condition=item_compare_first_is_item, default=0, actions={'get_value'}, remappable=True, id_min=0, id_max=9999, reference=True),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_compare.ITEM_ID_1, condition=item_compare_first_is_timer, default=0, actions={'get_value'}, remappable=True, id_min=0, id_max=9999, reference=True),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_compare.ITEM_ID_2, condition=item_compare_second_is_item, default=0, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_compare.ITEM_ID_2, condition=item_compare_second_is_timer, default=0, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True)
        ),
    obj_id.trigger.STATE_BLOCK: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.state_block.STATE_ON, default=0, actions={'spawn'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.state_block.STATE_OFF, default=0, actions={'spawn'}, id_min=1, id_max=9999)
        ),
    obj_id.trigger.STATIC_CAMERA: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.static_camera.TARGET_ID, default=0, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.GRADIENT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.gradient.U, default=0, actions={'track_position'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.gradient.D, default=0, actions={'track_position'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.gradient.L, default=0, actions={'track_position'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.gradient.R, default=0, actions={'track_position'}, id_min=1, id_max=9999),
            IDRule(id_type='gradient_id', obj_prop_id=obj_prop.trigger.gradient.GRADIENT_ID, default=0, id_min=0, id_max=1000, reference=True)
        ),
    obj_id.trigger.shader.SHOCKWAVE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.SHOCKWAVE_CENTER_ID, default=get_default_shockwave_target, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.shader.SHOCKLINE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.SHOCKLINE_CENTER_ID, default=get_default_shockline_target, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.shader.BULGE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.BULGE_CENTER_ID, default=get_default_bulge_target, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.shader.PINCH: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.shader.PINCH_CENTER_ID, default=get_default_pinch_target, remappable=True, id_min=1, id_max=9999)
        ,),
    obj_id.trigger.STOP: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.stop.TARGET_ID, condition=stop_use_group, default=0, actions={'stop'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='control_id', obj_prop_id=obj_prop.trigger.stop.TARGET_ID, condition=stop_use_control_id, default=0, actions={'stop_target'}, remappable=True)
        ),
    obj_id.trigger.SEQUENCE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.sequence.SEQUENCE, function=get_keys, replace=remap_pairs_keys, actions={'spawn'}, id_min=1, id_max=9999, iterable=True)
        ,),
    obj_id.trigger.ADV_RANDOM: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.adv_random.TARGETS, function=get_keys, replace=remap_pairs_keys, actions={'spawn'}, id_min=1, id_max=9999, iterable=True)
        ,),
    obj_id.trigger.EDIT_ADV_FOLLOW: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=edit_adv_follow_use_group, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.SPEED_REF, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.DIR_REF, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='control_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=edit_adv_follow_use_control_id, default=0, remappable=True)
        ),
    obj_id.trigger.RETARGET_ADV_FOLLOW: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=edit_adv_follow_use_group, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.FOLLOW_ID, default=0, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='control_id', obj_prop_id=obj_prop.trigger.edit_adv_follow.TARGET_ID, condition=edit_adv_follow_use_control_id, default=0, remappable=True)
        ),
    obj_id.collectible.USER_COIN: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    obj_id.collectible.KEY: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    1587: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    1589: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    1598: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    obj_id.collectible.SMALL_COIN: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    3601: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4401: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4402: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4403: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4404: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4405: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4406: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4407: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4408: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4409: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4410: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4411: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4412: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4413: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4414: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4415: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4416: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4417: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4418: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4419: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4420: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4421: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4422: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4423: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4424: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4425: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4426: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4427: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4428: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4429: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4430: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4431: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4432: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4433: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4434: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4435: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4436: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4437: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4438: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4439: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4440: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4441: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4442: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4443: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4444: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4445: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4446: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4447: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4448: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4449: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4450: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4451: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4452: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4453: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4454: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4455: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4456: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4457: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4458: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4459: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4460: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4461: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4462: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4463: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4464: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4465: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4466: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4467: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4468: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4469: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4470: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4471: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4472: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4473: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4474: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4475: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4476: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4477: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4478: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4479: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4480: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4481: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4482: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4483: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4484: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4485: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4486: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4487: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4488: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4538: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4489: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4490: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4491: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4492: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4493: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4494: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4495: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4496: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4497: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4537: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4498: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4499: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4500: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4501: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4502: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4503: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4504: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4505: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4506: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4507: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4508: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4509: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4510: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4511: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4512: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4513: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4514: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4515: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4516: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4517: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4518: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4519: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4520: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4521: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4522: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4523: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4524: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4525: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4526: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4527: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4528: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4529: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4530: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4531: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4532: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4533: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4534: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4535: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4536: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    4539: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.GROUP_ID, default=get_collectible_default_group_id, actions={'spawn', 'toggle'}, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.collectible.PARTICLE, default=0, actions={'get_particles'}, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.collectible.ITEM_ID, default=get_collectible_default_item_id, actions={'set_value'}, id_min=0, id_max=9999)
        ),
    obj_id.trigger.area.MOVE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.CENTER_ID, default=get_area_default_center, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'move_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ),
    obj_id.trigger.area.SCALE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.CENTER_ID, default=get_area_default_center, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'scale_group', 'move_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ),
    obj_id.trigger.area.ROTATE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.CENTER_ID, default=get_area_default_center, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'rotate_group', 'move_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ),
    obj_id.trigger.area.FADE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.CENTER_ID, default=get_area_default_center, actions={'track_position'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'fade_group'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True)
        ),
    obj_id.trigger.area.EDIT_MOVE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_group_id, default=0, actions={'area_edit'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_effect_id, default=0, actions={'area_edit'}, remappable=True)
        ),
    obj_id.trigger.area.EDIT_SCALE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_group_id, default=0, actions={'area_edit'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_effect_id, default=0, actions={'area_edit'}, remappable=True)
        ),
    obj_id.trigger.area.EDIT_ROTATE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_group_id, default=0, actions={'area_edit'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_effect_id, default=0, actions={'area_edit'}, remappable=True)
        ),
    obj_id.trigger.area.EDIT_FADE: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_group_id, default=0, actions={'area_edit'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_effect_id, default=0, actions={'area_edit'}, remappable=True)
        ),
    obj_id.trigger.area.EDIT_TINT: (
            IDRule(id_type='group_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_group_id, default=0, actions={'area_edit'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, condition=area_use_effect_id, default=0, actions={'area_edit'}, remappable=True)
        ),
    obj_id.trigger.ITEM_EDIT: (
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=item_edit_target_is_item, actions={'set_value'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_edit.TARGET_ITEM_ID, condition=item_edit_target_is_timer, actions={'set_value'}, remappable=True, id_min=1, id_max=9999),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_edit.ITEM_ID_1, condition=item_edit_first_is_item, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_edit.ITEM_ID_1, condition=item_edit_first_is_timer, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True),
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_edit.ITEM_ID_2, condition=item_edit_second_is_item, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_edit.ITEM_ID_2, condition=item_edit_second_is_timer, actions={'get_value'}, remappable=True, id_min=1, id_max=9999, reference=True)
        ),
    obj_id.ITEM_LABEL: (
            IDRule(id_type='item_id', obj_prop_id=obj_prop.item_label.ITEM_ID, condition=item_label_display_item, default=0, actions={'set_value'}, id_min=0, id_max=9999, reference=True),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.item_label.ITEM_ID, condition=item_label_display_timer, default=0, actions={'set_value'}, id_min=0, id_max=9999, reference=True)
        ),
    obj_id.trigger.PICKUP: (
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.pickup.ITEM_ID, default=0, actions={'set_value'}, remappable=True, id_min=0, id_max=9999)
        ,),
    obj_id.trigger.TIME_CONTROL: (
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.time_control.ITEM_ID, default=0, remappable=True)
        ,),
    obj_id.trigger.ITEM_PERSIST: (
            IDRule(id_type='item_id', obj_prop_id=obj_prop.trigger.item_persist.ITEM_ID, condition=item_persist_item, default=0, actions={'set_persist'}, remappable=True, id_min=0, id_max=9999),
            IDRule(id_type='time_id', obj_prop_id=obj_prop.trigger.item_persist.ITEM_ID, condition=item_persist_timer, default=0, actions={'set_persist'}, remappable=True)
        ),
    obj_id.trigger.COLLISION_BLOCK: (
            IDRule(id_type='collision_id', obj_prop_id=obj_prop.trigger.collision_block.BLOCK_ID, default=0, id_min=1, id_max=9999, reference=True)
        ,),
    obj_id.trigger.ARROW: (
            IDRule(id_type='trigger_channel', obj_prop_id=obj_prop.trigger.arrow.TARGET_CHANNEL, default=0, actions={'set_value'}, reference=True)
        ,),
    obj_id.trigger.START_POSITION: (
            IDRule(id_type='trigger_channel', obj_prop_id=obj_prop.start_pos.TARGET_CHANNEL, default=0, actions={'set_value'})
        ,),
    obj_id.trigger.area.STOP: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.TARGET_ID, default=0, actions={'stop_area'}, remappable=True, reference=True)
        ,),
    obj_id.trigger.enter.MOVE: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    obj_id.trigger.enter.SCALE: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    obj_id.trigger.enter.ROTATE: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    obj_id.trigger.enter.FADE: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, reference=True),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    obj_id.trigger.enter.STOP: (
            IDRule(id_type='effect_id', obj_prop_id=obj_prop.trigger.effect.EFFECT_ID, default=0, actions={'area_stop'}),
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.effect.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ),
    22: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    24: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    23: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    25: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    26: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    27: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    28: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    55: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    56: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    57: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    58: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    59: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    1915: (
            IDRule(id_type='enter_channel', obj_prop_id=obj_prop.trigger.enter_preset.ENTER_CHANNEL, default=0, remappable=True, id_min=-32768, id_max=32767)
        ,),
    obj_id.trigger.SONG: (
            IDRule(id_type='song_id', obj_prop_id=obj_prop.trigger.song.SONG_ID, default=0, remappable=True, reference=True),
            IDRule(id_type='song_channel', obj_prop_id=obj_prop.trigger.song.CHANNEL, default=0, remappable=True, id_min=0, id_max=4, reference=True)
        ),
    obj_id.trigger.FORCE_BLOCK: (
            IDRule(id_type='force_id', obj_prop_id=obj_prop.trigger.force_block.FORCE_ID, default=0, reference=True)
        ,),
    obj_id.trigger.FORCE_CIRCLE: (
            IDRule(id_type='force_id', obj_prop_id=obj_prop.trigger.force_block.FORCE_ID, default=0, id_min=-32768, id_max=32767, reference=True)
        ,)
    }
)