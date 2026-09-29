# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class KeyframeObject(TriggerObject):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    group_id: int = Field(51)
    spawn_id: int = Field(71)
    ease_rate: float = Field(85)
    key_id: int = Field(373)
    index: int = Field(374)
    ref_only: bool = Field(375)
    close_loop: bool = Field(376)
    prox: bool = Field(377)
    curve: bool = Field(378)
    time_mode: enums.KeyframeRefMode = Field(379)
    preview_art: bool = Field(380)
    auto_layer: bool = Field(459)
    line_opacity: float = Field(524)
    spin_direction: enums.KeyframeSpin = Field(536)
    full_rotations: int = Field(537)
    spawn_delay: float = Field(557)


class AnimateKeyframeTrigger(TriggerObject):
    target_id: int = Field(51)
    parent_id: int = Field(71)
    animation_id: int = Field(76)
    time_mod: float = Field(520)
    pos_x_mod: float = Field(521)
    rotation_mod: float = Field(522)
    scale_x_mod: float = Field(523)
    pos_y_mod: float = Field(545)
    scale_y_mod: float = Field(546)


class MoveTrigger(TriggerObject):
    duration: float = Field(10)
    move_x: float = Field(28)
    move_y: float = Field(29)
    easing: enums.Easing = Field(30)
    target_id: int = Field(51)
    lock_player_x: bool = Field(58)
    lock_player_y: bool = Field(59)
    target_pos: int = Field(71)
    ease_rate: float = Field(85)
    target_mode: bool = Field(100)
    target_axis: enums.TargetAxis = Field(101)
    player_1: bool = Field(138)
    lock_camera_x: bool = Field(141)
    lock_camera_y: bool = Field(142)
    follow_x_mod: float = Field(143)
    follow_y_mod: float = Field(144)
    player_2: bool = Field(200)
    use_small_step: bool = Field(393)
    direction_mode: bool = Field(394)
    target_center_id: int = Field(395)
    target_distance: float = Field(396)
    dynamic_mode: bool = Field(397)
    silent: bool = Field(544)


class RotateTrigger(TriggerObject):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    target_id: int = Field(51)
    degrees: float = Field(68)
    full_rotations: int = Field(69)
    lock_rotation: bool = Field(70)
    center_id: int = Field(71)
    ease_rate: float = Field(85)
    aim_mode: bool = Field(100)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    follow_mode: bool = Field(394)
    dynamic_mode: bool = Field(397)
    aim_target: int = Field(401)
    aim_offset: float = Field(402)
    aim_easing: int = Field(403)
    min_x_id: int = Field(516)
    min_y_id: int = Field(517)
    max_x_id: int = Field(518)
    max_y_id: int = Field(519)


class ScaleTrigger(TriggerObject):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    target_id: int = Field(51)
    center_id: int = Field(71)
    ease_rate: float = Field(85)
    only_move: bool = Field(133)
    scale_by_x: float = Field(150)
    scale_by_y: float = Field(151)
    div_by_x: bool = Field(153)
    div_by_y: bool = Field(154)
    relative_rotation: bool = Field(452)
    relative_scale: bool = Field(577)


# AnimateKeyframeTrigger
register_id(3033, AnimateKeyframeTrigger)  # Keyframe Animation Trigger

# KeyframeObject
register_id(3032, KeyframeObject)  # Keyframe Point

# MoveTrigger
register_id(901, MoveTrigger)  # Move Trigger

# RotateTrigger
register_id(1346, RotateTrigger)  # Rotate Trigger

# ScaleTrigger
register_id(2067, ScaleTrigger)  # Scale Trigger