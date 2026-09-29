# Package Imports
from gmdkit.utils import enums
from gmdkit.models.prop.hsv import HSV
from gmdkit.serialization.classes import BaseInterface
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id

# Common
class AreaSettings(BaseInterface):
    offset: int = Field(220)
    offset_rand: int = Field(221)
    length: int = Field(222)
    length_rand: int = Field(223)
    offset_y: int = Field(252)
    offset_y_rand: int = Field(253)
    mod_front: float = Field(263)
    mod_back: float = Field(264)
    deadzone: float = Field(282)

class AreaTrigger(AreaSettings,TriggerObject):
    target_id: int = Field(51)
    center_id: int = Field(71)
    effect_id: int = Field(225)
    direction: int = Field(262)
    inwards: bool = Field(276)
    mirrored: bool = Field(283)
    priority: int = Field(341)
    special_center: enums.EffectSpecialCenter = Field(538)

class AreaTransformTrigger(AreaTrigger):
   easing: enums.Easing = Field(242)
   easing_rate: float = Field(243)
   easing_2: enums.Easing = Field(248)
   easing_rate_2: float = Field(249)
   ease_out: bool = Field(261)
   deap: bool = Field(539)

class EditAreaTrigger(AreaSettings,TriggerObject):
    duration: float = Field(10)
    target_id: int = Field(51)
    use_effect_id: bool = Field(355)


# Area Move
class MoveSettings(BaseInterface):
    move_dist: int = Field(218)
    move_dist_rand: int = Field(219)
    move_angle: int = Field(231)
    move_angle_rand: int = Field(232)
    move_x: int = Field(237)
    move_x_rand: int = Field(238)
    move_y: int = Field(239)
    move_y_rand: int = Field(240)
    xy_mode: bool = Field(241)
    relative: bool = Field(287)
    rfade: float = Field(288)

class AreaMoveTrigger(MoveSettings,AreaTransformTrigger):
    pass

class EditAreaMoveTrigger(MoveSettings,EditAreaTrigger):
    pass


# Area Rotate
class RotateSettings(BaseInterface):
    rotate: float = Field(270)
    rotate_rand: float = Field(271)

class AreaRotateTrigger(RotateSettings,AreaTransformTrigger):
    pass

class EditAreaRotateTrigger(RotateSettings,EditAreaTrigger):
    pass


# Area Scale
class ScaleSettings(BaseInterface):
    scale_x: float = Field(233)
    scale_x_rand: float = Field(234)
    scale_y: float = Field(235)
    scale_y_rand: float = Field(236)

class AreaScaleTrigger(ScaleSettings,AreaTransformTrigger):
    pass

class EditAreaScaleTrigger(ScaleSettings,EditAreaTrigger):
    pass


# Area Fade
class FadeSettings(BaseInterface):
    to_opacity: float = Field(275)
    from_opacity: float = Field(286)

class AreaFadeTrigger(FadeSettings,AreaTrigger):
    pass

class EditAreaFadeTrigger(FadeSettings,EditAreaTrigger):
    pass


# Area Tint
class TintSettings(BaseInterface):
    hsv: HSV = Field(49)
    tint: float = Field(265)
    enable_hsv: bool = Field(278)

class AreaTintTrigger(TintSettings,AreaTrigger):
    main_only: bool = Field(65)
    detail_only: bool = Field(66)
    tint_channel: int = Field(260)

class EditAreaTintTrigger(TintSettings,EditAreaTrigger):
    pass


# Area Stop
class StopAreaTrigger(TriggerObject):
    effect_id: int = Field(51)


# AreaMoveTrigger
register_id(3006, AreaMoveTrigger)  # Area Move Trigger
register_id(3011, EditAreaMoveTrigger)  # Edit Area Move Trigger

# AreaRotateTrigger
register_id(3007, AreaRotateTrigger)  # Area Rotate Trigger
register_id(3012, EditAreaRotateTrigger)  # Edit Area Rotate Trigger

# AreaScaleTrigger
register_id(3008, AreaScaleTrigger)  # Area Scale Trigger
register_id(3013, EditAreaScaleTrigger)  # Edit Area Scale Trigger

# AreaFadeTrigger
register_id(3009, AreaFadeTrigger)  # Area Fade Trigger
register_id(3014, EditAreaFadeTrigger)  # Edit Area Fade Trigger

# AreaTintTrigger
register_id(3010, AreaTintTrigger)  # Area Tint Trigger
register_id(3015, EditAreaTintTrigger)  # Edit Area Tint Trigger

# StopAreaTrigger
register_id(3024, StopAreaTrigger)  # Area Stop Trigger

