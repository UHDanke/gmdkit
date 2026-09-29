# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class CheckpointTrigger(TriggerObject):
    spawn_id: int = Field(51)
    target_pos: int = Field(71)
    player_pos: bool = Field(138)
    respawn_id: int = Field(448)


class EndTrigger(TriggerObject):
    spawn_id: int = Field(51)
    target_pos: int = Field(71)
    no_effects: bool = Field(460)
    no_sfx: bool = Field(461)
    instant: bool = Field(487)


class EndWallTrigger(TriggerObject): # unused
    group_id: int = Field(51)
    lock_y: bool = Field(59)
    reverse: bool = Field(118)


class GameplayArrow(TriggerObject):
    dir_y_neg: enums.ArrowDir = Field(166)
    dir_x_pos: enums.ArrowDir = Field(167)
    edit_velocity: bool = Field(169)
    change_channel: bool = Field(171)
    channel_only: bool = Field(172)
    target_channel: int = Field(173)
    instant_offset: bool = Field(368)
    velocity_mod_x: float = Field(582)
    velocity_mod_y: float = Field(583)
    override_velocity: bool = Field(584)
    dont_slide: bool = Field(585)


class GravityTrigger(TriggerObject):
    player_1: bool = Field(138)
    gravity_mod: float = Field(148)
    player_2: bool = Field(200)
    player_touch: bool = Field(201)


class OptionsTrigger(TriggerObject):
    streak_additive: enums.Option = Field(159)
    unlink_dual_gravity: enums.Option = Field(160)
    hide_ground: enums.Option = Field(161)
    hide_p1: enums.Option = Field(162)
    hide_p2: enums.Option = Field(163)
    disable_p1_controls: enums.Option = Field(165)
    hide_mg: enums.Option = Field(195)
    disable_controls_p1: enums.Option = Field(199)
    hide_attempts: enums.Option = Field(532)
    edit_respawn_time: enums.Option = Field(573)
    respawn_time: float = Field(574)
    audio_on_death: enums.Option = Field(575)
    disable_death_sfx: enums.Option = Field(576)
    boost_slide: enums.Option = Field(593)


class PlayerControlTrigger(TriggerObject):
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    stop_jump: bool = Field(540)
    stop_move: bool = Field(541)
    stop_rotation: bool = Field(542)
    stop_slide: bool = Field(543)
    
    
# CheckpointTrigger
register_id(2063, CheckpointTrigger)  # Checkpoint

# EndTrigger
register_id(3600, EndTrigger)  # End Trigger

# EndWallTrigger
register_id(1931, EndWallTrigger)  # End Wall Trigger

# GameplayArrow
register_id(2900, GameplayArrow)  # Gameplay Rotation Trigger

# GravityTrigger
register_id(2066, GravityTrigger)  # Gravity Trigger

# OptionsTrigger
register_id(2899, OptionsTrigger)  # Options Trigger

# PlayerControlTrigger
register_id(1932, PlayerControlTrigger)  # Player Control Trigger