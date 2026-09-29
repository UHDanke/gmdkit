# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class AdvancedFollowTrigger(TriggerObject):
    target_id: int = Field(51)
    follow_id: int = Field(71)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    corner: bool = Field(201)
    delay: float = Field(292)
    delay_rand: float = Field(293)
    max_speed: float = Field(298)
    max_speed_rand: float = Field(299)
    start_speed: float = Field(300)
    start_speed_rand: float = Field(301)
    target_dir: bool = Field(305)
    x_only: bool = Field(306)
    y_only: bool = Field(307)
    max_range: float = Field(308)
    max_range_rand: float = Field(309)
    steer: float = Field(316)
    steer_rand: float = Field(317)
    steer_low: float = Field(318)
    steer_low_rand: float = Field(319)
    steer_high: float = Field(320)
    steer_high_rand: float = Field(321)
    speed_range_low: float = Field(322)
    speed_range_low_rand: float = Field(323)
    speed_range_high: float = Field(324)
    speed_range_high_rand: float = Field(325)
    break_force: float = Field(326)
    break_force_rand: float = Field(327)
    break_angle: float = Field(328)
    break_angle_rand: float = Field(329)
    break_steer: float = Field(330)
    break_steer_rand: float = Field(331)
    break_steer_speed_limit: float = Field(332)
    break_steer_speed_limit_rand: float = Field(333)
    acceleration: float = Field(334)
    acceleration_rand: float = Field(335)
    ignore_disabled: bool = Field(336)
    steer_low_check: bool = Field(337)
    steer_high_check: bool = Field(338)
    rotate_dir: bool = Field(339)
    rot_offset: float = Field(340)
    near_accel: float = Field(357)
    near_accel_rand: float = Field(358)
    near_dist: float = Field(359)
    near_dist_rand: float = Field(360)
    easing: float = Field(361)
    easing_rand: float = Field(362)
    rot_easing: float = Field(363)
    rot_deadzone: float = Field(364)
    priority: int = Field(365)
    max_range_ref: int = Field(366)
    mode: enums.AdvFollowMode = Field(367)
    friction: float = Field(558)
    friction_rand: float = Field(559)
    start_speed_ref: int = Field(560)
    near_friction: float = Field(561)
    near_friction_rand: float = Field(562)
    start_dir: float = Field(563)
    start_dir_rand: float = Field(564)
    start_dir_ref: int = Field(565)
    exclusive: bool = Field(571)
    init: enums.AdvFollowInit = Field(572)


class EditAdvancedFollowTrigger(TriggerObject):
    target_id: int = Field(51)
    speed: float = Field(300)
    speed_rand: float = Field(301)
    x_only: bool = Field(306)
    y_only: bool = Field(307)
    use_control_id: bool = Field(535)
    speed_ref: int = Field(560)
    dir_angle: float = Field(563)
    dir_rand: float = Field(564)
    dir_ref: int = Field(565)
    mod_x: float = Field(566)
    mod_x_rand: float = Field(567)
    mod_y: float = Field(568)
    mod_y_rand: float = Field(569)


class RetargetAdvancedFollowTrigger(TriggerObject):
    target_id: int = Field(51)
    follow_id: int = Field(71)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    corner: bool = Field(201)
    use_control_id: bool = Field(535)
    
    
class FollowTrigger(TriggerObject):
    duration: float = Field(10)
    target_id: int = Field(51)
    follow_id: int = Field(71)
    mod_x: float = Field(72)
    mod_y: float = Field(73)


class FollowPlayerYTrigger(TriggerObject):
    duration: float = Field(10)
    target_id: int = Field(51)
    speed: float = Field(90)
    delay: float = Field(91)
    offset: int = Field(92)
    max_speed: float = Field(105)
    

# AdvancedFollowTrigger
register_id(3016, AdvancedFollowTrigger)  # Advanced Follow Trigger

# EditAdvancedFollowTrigger
register_id(3660, EditAdvancedFollowTrigger)  # Edit Advanced Follow Trigger

# RetargetAdvancedFollowTrigger
register_id(3661, RetargetAdvancedFollowTrigger)  # Re-Target Advanced Follow Trigger

# FollowPlayerYTrigger
register_id(1814, FollowPlayerYTrigger)  # Follow Player Y Trigger

# FollowTrigger
register_id(1347, FollowTrigger)  # Follow Trigger