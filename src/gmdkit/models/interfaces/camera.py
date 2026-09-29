# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class ZoomCameraTrigger(TriggerObject):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    zoom: float = Field(371)


class StaticCameraTrigger(TriggerObject):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target_id: int = Field(71)
    target_axis: enums.TargetAxis = Field(101)
    exit_static: bool = Field(110)
    follow_group: bool = Field(212)
    follow_easing: float = Field(213)
    smooth_velocity: bool = Field(453)
    velocity_mod: float = Field(454)
    exit_instant: bool = Field(465)


class OffsetCameraTrigger(TriggerObject):
    duration: float = Field(10)
    offset_x: float = Field(28)
    offset_y: float = Field(29)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target_axis: enums.TargetAxis = Field(101)


class RotateCameraTrigger(TriggerObject):
    duration: float = Field(10)
    degrees: float = Field(68)
    add: bool = Field(70)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    snap_360: bool = Field(394)


class CameraEdgeTrigger(TriggerObject):
    target_id: int = Field(51)
    edge: enums.CameraEdge = Field(164)


class CameraModeTrigger(TriggerObject):
    free_mode: bool = Field(111)
    edit_settings: bool = Field(112)
    camera_easing: float = Field(113)
    camera_padding: float = Field(114)
    disable_grid_snap: float = Field(370)


class CameraGuide(TriggerObject):
    offset_x: float = Field(28)
    offset_y: float = Field(29)
    zoom: float = Field(371)
    preview_opacity: float = Field(506)


class ShakeTrigger(TriggerObject):
    duration: float = Field(10)
    strength: float = Field(75)
    interval: float = Field(84)


class GameplayOffsetTrigger(TriggerObject):
    offset_x: float = Field(28)
    offset_y: float = Field(29)
    dont_zoom_x: bool = Field(58)
    dont_zoom_y: bool = Field(59)
    target_axis: enums.TargetAxis = Field(101)


# CameraEdgeTrigger
register_id(2062, CameraEdgeTrigger)  # Edge Camera Trigger

# CameraGuide
register_id(2016, CameraGuide)  # Camera Guide

# CameraModeTrigger
register_id(2925, CameraModeTrigger)  # Mode Camera Trigger

# OffsetCameraTrigger
register_id(1916, OffsetCameraTrigger)  # Offset Camera Trigger

# RotateCameraTrigger
register_id(2015, RotateCameraTrigger)  # Rotate Camera Trigger

# ShakeTrigger
register_id(1520, ShakeTrigger)  # Shake Trigger

# StaticCameraTrigger
register_id(1914, StaticCameraTrigger)  # Static Camera Trigger

# ZoomCameraTrigger
register_id(1913, ZoomCameraTrigger)  # Zoom Camera Trigger

# GameplayOffsetTrigger
register_id(2901, GameplayOffsetTrigger)  # Gameplay Offset Camera Trigger