# Package Imports
from gmdkit.utils import enums
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class EnterPreset(TriggerObject):
    enter_exit_only: enums.EnterMode = Field(217)
    enter_channel: int = Field(344)


class EnterTrigger(EnterPreset):
    offset: int = Field(220)
    offset_rand: int = Field(221)
    length: int = Field(222)
    length_rand: int = Field(223)
    effect_id: int = Field(225)
    easing: enums.Easing = Field(242)
    easing_rate: float = Field(243)


class EnterMoveTrigger(EnterTrigger):
    move_dist: int = Field(218)
    move_dist_rand: int = Field(219)
    move_angle: int = Field(231)
    move_angle_rand: int = Field(232)
    move_x: int = Field(237)
    move_x_rand: int = Field(238)
    move_y: int = Field(239)
    move_y_rand: int = Field(240)
    xy_mode: bool = Field(241)


class EnterRotateTrigger(EnterTrigger):
    rotate: float = Field(270)
    rotate_rand: float = Field(271)


class EnterScaleTrigger(EnterTrigger):
    scale_x: float = Field(233)
    scale_x_rand: float = Field(234)
    scale_y: float = Field(235)
    scale_y_rand: float = Field(236)


class EnterFadeTrigger(EnterTrigger):
    opacity: float = Field(275) # can be set but the option does not work


class EnterTintTrigger(EnterTrigger):
    hsv: HSV = Field(49)
    main_only: bool = Field(65)
    detail_only: bool = Field(66)
    tint_channel: int = Field(260)
    tint: float = Field(265)
    enable_hsv: bool = Field(278)


class StopEnterTrigger(TriggerObject):
    enter_channel: int = Field(344)
    effect_id: int = Field(225)

# EnterPreset
register_id(22, EnterPreset)  # No Fade Effect
register_id(23, EnterPreset)  # Fade Bottom Enter Effect
register_id(24, EnterPreset)  # Fade Top Enter Effect
register_id(25, EnterPreset)  # Fade Left Enter Effect
register_id(26, EnterPreset)  # Fade Right Enter Effect
register_id(27, EnterPreset)  # Small to Big Enter Effect
register_id(28, EnterPreset)  # Big to Small Enter Effect
register_id(55, EnterPreset)  # Chaotic Enter Effect
register_id(56, EnterPreset)  # Halve Left Enter Effect
register_id(57, EnterPreset)  # Halve Right Enter Effect
register_id(58, EnterPreset)  # Halve Enter Effect
register_id(59, EnterPreset)  # Inverse Halve Enter Effect
register_id(1915, EnterPreset)  # No Enter Effect

# EnterMoveTrigger
register_id(3017, EnterMoveTrigger)  # Enter Move Trigger

# EnterRotateTrigger
register_id(3018, EnterRotateTrigger)  # Enter Rotate Trigger

# EnterScaleTrigger
register_id(3019, EnterScaleTrigger)  # Enter Scale Trigger

# EnterFadeTrigger
register_id(3020, EnterFadeTrigger)  # Enter Fade Trigger

# EnterTintTrigger
register_id(3021, EnterTintTrigger)  # Enter Tint Trigger

# StopEnterTrigger
register_id(3023, StopEnterTrigger)  # Enter Stop Trigger