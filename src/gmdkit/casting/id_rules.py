# Package Imports
from gmdkit.mappings import obj_id, prop_id, color_prop
from gmdkit.defaults.color_default import COLOR_1_DEFAULT, COLOR_2_DEFAULT


ID_RULES = {
    obj_id.trigger.color: [
            {'type': 'color_id', 'property_id': prop_id.trigger.color.channel, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': prop_id.trigger.color.copy_id, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.shader.gray_scale: [
            {'type': 'color_id', 'property_id': prop_id.trigger.shader.gray_scale_tint_channel, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.lens_circle: [
            {'type': 'color_id', 'property_id': prop_id.trigger.shader.lens_circle_tint_channel, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.lens_circle_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.radial_blur: [
            {'type': 'color_id', 'property_id': prop_id.trigger.shader.radial_blur_ref_channel, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.radial_blur_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.motion_blur: [
            {'type': 'color_id', 'property_id': prop_id.trigger.shader.motion_blur_ref_channel, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.motion_blur_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    'any': [
            {'type': 'color_id', 'property_id': prop_id.color_1, 'default': lambda x: COLOR_1_DEFAULT.get(x,0), 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': prop_id.color_2, 'default': lambda x: COLOR_2_DEFAULT.get(x,0), 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.groups, 'replace': lambda x, kvm: x.remap(kvm), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True},
            {'type': 'group_id', 'property_id': prop_id.parent_groups, 'replace': lambda x, kvm: x.remap(kvm), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True},
            {'type': 'linked_id', 'property_id': prop_id.linked_group, 'min': 1, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'trigger_channel', 'property_id': prop_id.trigger.channel, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False},
            {'type': 'material_id', 'property_id': prop_id.material, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False},
            {'type': 'control_id', 'property_id': prop_id.trigger.control_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.pulse: [
            {'type': 'color_id', 'property_id': prop_id.trigger.pulse.copy_id, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'color_id', 'property_id': prop_id.trigger.pulse.target_id, 'condition': lambda x: x.get(prop_id.trigger.pulse.target_type,0) == 0, 'min': 1, 'max': 999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.pulse.target_id, 'condition': lambda x: x.get(prop_id.trigger.pulse.target_type,0) == 1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.tint: [
            {'type': 'color_id', 'property_id': prop_id.trigger.effect.tint_channel, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.tint: [
            {'type': 'color_id', 'property_id': prop_id.trigger.effect.tint_channel, 'min': 1, 'max': 999, 'remappable': False, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.level_start: [
            {'type': 'color_id', 'property_id': prop_id.level.colors, 'function': lambda x: x.unique_values(lambda i: i.channels), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(kvm)), 'min': 1, 'max': 999, 'remappable': False, 'iterable': True},
            {'type': 'group_id', 'property_id': prop_id.level.player_spawn, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.move: [
            {'type': 'group_id', 'property_id': prop_id.trigger.move.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.move.target_pos, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.move.target_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.alpha: [
            {'type': 'group_id', 'property_id': prop_id.trigger.alpha.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.toggle: [
            {'type': 'group_id', 'property_id': prop_id.trigger.toggle.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.toggle_block: [
            {'type': 'group_id', 'property_id': prop_id.trigger.toggle_block.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.orb.toggle: [
            {'type': 'group_id', 'property_id': prop_id.trigger.toggle_block.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.on_death: [
            {'type': 'group_id', 'property_id': prop_id.trigger.on_death.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.spawn: [
            {'type': 'group_id', 'property_id': prop_id.trigger.spawn.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'remap_base', 'property_id': prop_id.trigger.spawn.remaps, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': True},
            {'type': 'remap_target', 'property_id': prop_id.trigger.spawn.remaps, 'condition': lambda x: x.get(prop_id.trigger.spawn.reset_remap,0) == 1, 'function': lambda x: x.values(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': True},
            {'type': 'remap_target', 'property_id': prop_id.trigger.spawn.remaps, 'condition': lambda x: x.get(prop_id.trigger.spawn.reset_remap,0) == 0, 'function': lambda x: x.values(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(value_map=kvm)), 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': True}
        ],
    obj_id.trigger.teleport: [
            {'type': 'group_id', 'property_id': prop_id.trigger.teleport.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.song: [
            {'type': 'group_id', 'property_id': prop_id.trigger.song.group_id_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.song.group_id_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'song_id', 'property_id': prop_id.trigger.song.song_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'song_channel', 'property_id': prop_id.trigger.song.channel, 'default': 0, 'min': 0, 'max': 4, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.song_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.song.group_id_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.song.group_id_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'song_channel', 'property_id': prop_id.trigger.song.channel, 'default': 0, 'min': 0, 'max': 4, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.sfx: [
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group_id_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group_id_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'sfx_id', 'property_id': prop_id.trigger.sfx.sfx_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'unique_sfx_id', 'property_id': prop_id.trigger.sfx.unique_id, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'sfx_group', 'property_id': prop_id.trigger.sfx.group_id, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.sfx_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group_id_1, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group_id_2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.sfx.group, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'unique_sfx_id', 'property_id': prop_id.trigger.sfx.unique_id, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False},
            {'type': 'sfx_group', 'property_id': prop_id.trigger.sfx.group_id, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.rotate: [
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.rotate_target, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.aim_target, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.min_x_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.min_y_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.max_x_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.rotate.max_y_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.follow: [
            {'type': 'group_id', 'property_id': prop_id.trigger.follow.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.follow.follow_target, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.animate: [
            {'type': 'group_id', 'property_id': prop_id.trigger.animate.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.touch: [
            {'type': 'group_id', 'property_id': prop_id.trigger.touch.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.count: [
            {'type': 'group_id', 'property_id': prop_id.trigger.count.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.count.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.instant_count: [
            {'type': 'group_id', 'property_id': prop_id.trigger.instant_count.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.instant_count.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.follow_player_y: [
            {'type': 'group_id', 'property_id': prop_id.trigger.follow_player_y.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.collision: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collision.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': prop_id.trigger.collision.block_a, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': prop_id.trigger.collision.block_b, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.random: [
            {'type': 'group_id', 'property_id': prop_id.trigger.random.true_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.random.false_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.end_wall: [
            {'type': 'group_id', 'property_id': prop_id.trigger.end_wall.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.camera_edge: [
            {'type': 'group_id', 'property_id': prop_id.trigger.camera_edge.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.checkpoint: [
            {'type': 'group_id', 'property_id': prop_id.trigger.checkpoint.spawn_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.checkpoint.target_pos, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.checkpoint.respawn_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.scale: [
            {'type': 'group_id', 'property_id': prop_id.trigger.scale.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.scale.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.adv_follow: [
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_follow.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_follow.follow_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_follow.max_range_ref, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_follow.start_speed_ref, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_follow.start_dir_ref, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.keyframe: [
            {'type': 'group_id', 'property_id': prop_id.trigger.keyframe.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.keyframe.spawn_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'keyframe_id', 'property_id': prop_id.trigger.keyframe.key_id, 'default': 0, 'min': 0, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.animate_keyframe: [
            {'type': 'group_id', 'property_id': prop_id.trigger.animate_keyframe.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.animate_keyframe.parent_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.animate_keyframe.animation_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.end: [
            {'type': 'group_id', 'property_id': prop_id.trigger.end.spawn_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.end.target_pos, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.event: [
            {'type': 'group_id', 'property_id': prop_id.trigger.event.spawn_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'material_id', 'property_id': prop_id.trigger.event.extra_id_1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.spawn_particle: [
            {'type': 'group_id', 'property_id': prop_id.trigger.spawn_particle.particle_group, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.spawn_particle.position_group, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.instant_collision: [
            {'type': 'group_id', 'property_id': prop_id.trigger.instant_collision.true_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.instant_collision.false_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': prop_id.trigger.instant_collision.block_a, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'collision_id', 'property_id': prop_id.trigger.instant_collision.block_b, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.ui: [
            {'type': 'group_id', 'property_id': prop_id.trigger.ui.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.ui.ui_target, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.time: [
            {'type': 'group_id', 'property_id': prop_id.trigger.time.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.time.item_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.time_event: [
            {'type': 'group_id', 'property_id': prop_id.trigger.time_event.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.time_event.item_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.reset: [
            {'type': 'group_id', 'property_id': prop_id.trigger.reset.group_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.object_control: [
            {'type': 'group_id', 'property_id': prop_id.trigger.object_control.target_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.link_visible: [
            {'type': 'group_id', 'property_id': prop_id.trigger.link_visible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.item_compare: [
            {'type': 'group_id', 'property_id': prop_id.trigger.item_compare.true_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.item_compare.false_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.item_compare.item_id_1, 'condition': lambda x: x.get(prop_id.trigger.item_compare.item_type_1,0) in (0,1), 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_compare.item_id_1, 'condition': lambda x: x.get(prop_id.trigger.item_compare.item_type_1,0) == 2, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.item_compare.item_id_2, 'condition': lambda x: x.get(prop_id.trigger.item_compare.item_type_2,0) in (0,1), 'default': 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_compare.item_id_2, 'condition': lambda x: x.get(prop_id.trigger.item_compare.item_type_2,0) == 2, 'default': 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.state_block: [
            {'type': 'group_id', 'property_id': prop_id.trigger.state_block.state_on, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.state_block.state_off, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.static_camera: [
            {'type': 'group_id', 'property_id': prop_id.trigger.static_camera.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.gradient: [
            {'type': 'group_id', 'property_id': prop_id.trigger.gradient.u, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.gradient.d, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.gradient.l, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.gradient.r, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'gradient_id', 'property_id': prop_id.trigger.gradient.gradient_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.shader.shockwave: [
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.shockwave_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.shockline: [
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.shockline_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.bulge: [
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.bulge_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.shader.pinch: [
            {'type': 'group_id', 'property_id': prop_id.trigger.shader.pinch_center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.stop: [
            {'type': 'group_id', 'property_id': prop_id.trigger.stop.target_id, 'condition': lambda x: x.get(prop_id.trigger.stop.use_control_id,0)== 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': prop_id.trigger.stop.target_id, 'condition': lambda x: x.get(prop_id.trigger.stop.use_control_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.sequence: [
            {'type': 'group_id', 'property_id': prop_id.trigger.sequence.sequence, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True}
        ],
    obj_id.trigger.adv_random: [
            {'type': 'group_id', 'property_id': prop_id.trigger.adv_random.targets, 'function': lambda x: x.keys(), 'replace': lambda x, kvm: x.apply(lambda i: i.remap(key_map=kvm)), 'min': 1, 'max': 9999, 'remappable': False, 'iterable': True}
        ],
    obj_id.trigger.edit_adv_follow: [
            {'type': 'group_id', 'property_id': prop_id.trigger.edit_adv_follow.target_id, 'condition': lambda x: x.get(prop_id.trigger.edit_adv_follow.use_control_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.edit_adv_follow.speed_ref, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.edit_adv_follow.dir_ref, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': prop_id.trigger.edit_adv_follow.target_id, 'condition': lambda x: x.get(prop_id.trigger.edit_adv_follow.use_control_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.retarget_adv_follow: [
            {'type': 'group_id', 'property_id': prop_id.trigger.edit_adv_follow.target_id, 'condition': lambda x: x.get(prop_id.trigger.edit_adv_follow.use_control_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.edit_adv_follow.follow_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'control_id', 'property_id': prop_id.trigger.edit_adv_follow.target_id, 'condition': lambda x: x.get(prop_id.trigger.edit_adv_follow.use_control_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.collectible.user_coin: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.collectible.key: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1587: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1589: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    1598: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.collectible.small_coin: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    3601: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4401: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4402: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4403: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4404: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4405: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4406: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4407: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4408: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4409: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4410: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4411: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4412: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4413: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4414: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4415: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4416: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4417: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4418: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4419: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4420: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4421: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4422: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4423: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4424: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4425: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4426: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4427: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4428: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4429: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4430: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4431: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4432: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4433: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4434: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4435: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4436: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4437: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4438: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4439: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4440: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4441: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4442: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4443: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4444: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4445: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4446: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4447: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4448: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4449: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4450: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4451: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4452: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4453: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4454: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4455: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4456: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4457: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4458: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4459: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4460: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4461: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4462: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4463: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4464: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4465: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4466: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4467: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4468: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4469: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4470: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4471: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4472: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4473: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4474: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4475: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4476: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4477: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4478: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4479: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4480: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4481: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4482: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4483: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4484: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4485: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4486: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4487: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4488: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4538: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4489: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4490: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4491: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4492: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4493: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4494: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4495: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4496: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4497: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4537: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4498: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4499: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4500: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4501: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4502: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4503: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4504: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4505: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4506: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4507: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4508: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4509: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4510: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4511: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4512: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4513: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4514: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4515: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4516: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4517: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4518: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4519: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4520: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4521: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4522: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4523: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4524: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4525: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4526: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4527: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4528: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4529: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4530: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4531: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4532: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4533: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4534: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4535: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4536: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    4539: [
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.group_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.collectible.particle   , 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.collectible.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.move: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.scale: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.rotate: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.fade: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.center_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.move_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.scale_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.rotate_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.fade_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.area.tint_edit: [
            {'type': 'group_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 0, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'condition': lambda x: x.get(prop_id.trigger.effect.use_effect_id,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.item_edit: [
            {'type': 'item_id', 'property_id': prop_id.trigger.item_edit.target_item_id, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_3,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_edit.target_item_id, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_3,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.item_edit.item_id_1, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_1,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_edit.item_id_1, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_1,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'item_id', 'property_id': prop_id.trigger.item_edit.item_id_2, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_2,0) in (0,1), 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_edit.item_id_2, 'condition': lambda x: x.get(prop_id.trigger.item_edit.item_type_2,0) == 2, 'min': 1, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.item_label: [
            {'type': 'item_id', 'property_id': prop_id.item_label.item_id, 'condition': lambda x: x.get(prop_id.item_label.time_counter,0) == 0, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.item_label.item_id, 'condition': lambda x: x.get(prop_id.item_label.time_counter,0) == 1, 'default': 0, 'min': 0, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.pickup: [
            {'type': 'item_id', 'property_id': prop_id.trigger.pickup.item_id, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.time_control: [
            {'type': 'time_id', 'property_id': prop_id.trigger.time_control.item_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.item_persist: [
            {'type': 'item_id', 'property_id': prop_id.trigger.item_persist.item_id, 'condition': lambda x: x.get(prop_id.trigger.item_persist.timer,0) == 0, 'default': 0, 'min': 0, 'max': 9999, 'remappable': True, 'iterable': False},
            {'type': 'time_id', 'property_id': prop_id.trigger.item_persist.item_id, 'condition': lambda x: x.get(prop_id.trigger.item_persist.timer,0) == 1, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.collision_block: [
            {'type': 'collision_id', 'property_id': prop_id.trigger.collision_block.block_id, 'min': 1, 'max': 9999, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.arrow: [
            {'type': 'trigger_channel', 'property_id': prop_id.trigger.arrow.target_channel, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.start_pos: [
            {'type': 'trigger_channel', 'property_id': prop_id.start_pos.target_channel, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.area.stop: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.target_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.move: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.scale: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.rotate: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.fade: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.enter.stop: [
            {'type': 'effect_id', 'property_id': prop_id.trigger.effect.effect_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False},
            {'type': 'enter_channel', 'property_id': prop_id.trigger.effect.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    22: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    24: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    23: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    25: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    26: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    27: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    28: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    55: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    56: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    57: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    58: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    59: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    1915: [
            {'type': 'enter_channel', 'property_id': prop_id.trigger.enter_preset.enter_channel, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': True, 'iterable': False}
        ],
    obj_id.trigger.force_block: [
            {'type': 'force_id', 'property_id': prop_id.trigger.force_block.force_id, 'default': 0, 'min': -2147483648, 'max': 2147483647, 'remappable': False, 'iterable': False}
        ],
    obj_id.trigger.force_circle: [
            {'type': 'force_id', 'property_id': prop_id.trigger.force_block.force_id, 'default': 0, 'min': -32768, 'max': 32767, 'remappable': False, 'iterable': False}
        ]
    }


def filter_rules(condition:callable, rule_list=ID_RULES):
    
    new_dict = {}
    
    for key, value in rule_list.items():
        
        new_list = []
        
        for item in value:
            
            if condition(item):
                
                new_list.append(item)
            
        if new_list != []:
            
            new_dict[key] = new_list
            
    return new_dict
