# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id
from gmdkit.utils.functions import normalize_orientation


class CheckpointTrigger(TriggerObject):
    spawn_id: int = Field(51)
    target_pos: int = Field(71)
    player_pos: bool = Field(138)
    respawn_id: int = Field(448)
    prespawn_id: int = Field(604)


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
    
    def update_dir(self) -> tuple[enums.ArrowDir, enums.ArrowDir]:
        rotation = self.rotation
        if rotation == 0 and (self.skew_x or self.skew_y):
            rotation = self.skew_x
        r = int(rotation) % 360
        if r % 90:
            x_pos, y_neg = enums.ArrowDir.RIGHT, enums.ArrowDir.DOWN
        else:
            x_pos, y_neg = normalize_orientation(r, bool(self.flip_x), bool(self.flip_y))
        self.dir_x_pos = x_pos
        self.dir_y_neg = y_neg
        return x_pos, y_neg

    def set_dir(self, rotated: bool, reverse: bool, gravity: bool):
        if rotated:
            x_pos, y_neg = enums.ArrowDir.DOWN, enums.ArrowDir.LEFT
        else:
            x_pos, y_neg = enums.ArrowDir.RIGHT, enums.ArrowDir.DOWN
        x_pos = x_pos.flip() if reverse else x_pos
        y_neg = y_neg.flip() if gravity else y_neg

        if self.update_dir() != (x_pos, y_neg):
            transforms = sorted(
                ((r, fx, fy) for r in (0, 90, 180, 270) for fx in (False, True) for fy in (False, True)),
                key=lambda t: (t[1] + t[2], t[0]))
            r, fx, fy = next(t for t in transforms if normalize_orientation(*t) == (x_pos, y_neg))
            old = self.hitbox_rect if self.touch_trigger else None
            self.rotation = r
            self.skew_x = 0
            self.skew_y = 0
            self.flip_x = fx
            self.flip_y = fy
            if old is not None:
                self.scale_x = 1
                self.scale_y = 1
                new = self.hitbox_rect
                if r in (90, 270):
                    self.scale_x = round(old[3] / new[3], 3)
                    self.scale_y = round(old[2] / new[2], 3)
                else:
                    self.scale_x = round(old[2] / new[2], 3)
                    self.scale_y = round(old[3] / new[3], 3)

        self.dir_x_pos = x_pos
        self.dir_y_neg = y_neg

    @property
    def rotate_mode(self) -> bool:
        return self.dir_y_neg in (enums.ArrowDir.LEFT, enums.ArrowDir.RIGHT)

    @rotate_mode.setter
    def rotate_mode(self, value: bool):
        self.set_dir(value, self.reverse, self.gravity)

    @property
    def reverse_mode(self) -> bool:
        return self.dir_x_pos in (enums.ArrowDir.UP, enums.ArrowDir.LEFT)

    @reverse_mode.setter
    def reverse_mode(self, value: bool):
        self.set_dir(self.rotated, value, self.gravity)

    @property
    def flip_gravity(self) -> bool:
        flipped = enums.ArrowDir.RIGHT if self.rotated else enums.ArrowDir.UP
        return self.dir_y_neg == flipped

    @flip_gravity.setter
    def flip_gravity(self, value: bool):
        self.set_dir(self.rotated, self.reverse, value)


class ReverseTrigger(TriggerObject):
    
    @property
    def reverse_mode(self) -> bool:
        return True


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

    
class ProgressTrigger(TriggerObject):
    target_item_id: int = Field(80)
    item_id: int = Field(95)
    progress: int = Field(602)
    add_progress: bool = Field(603)
    item_input: bool = Field(605)
    
# CheckpointTrigger
register_id(2063, CheckpointTrigger)  # Checkpoint

# EndTrigger
register_id(3600, EndTrigger)  # End Trigger

# EndWallTrigger
register_id(1931, EndWallTrigger)  # End Wall Trigger

# GameplayArrow
register_id(2900, GameplayArrow)  # Gameplay Rotation Trigger

# ReverseTrigger
register_id(1917, ReverseTrigger)  # Reverse Trigger

# GravityTrigger
register_id(2066, GravityTrigger)  # Gravity Trigger

# OptionsTrigger
register_id(2899, OptionsTrigger)  # Options Trigger

# PlayerControlTrigger
register_id(1932, PlayerControlTrigger)  # Player Control Trigger

# ProgressTrigger
register_id(3663, ProgressTrigger)