# Imports
from typing import Self

# Package Imports
from gmdkit.utils import enums
from gmdkit.models.prop.color import Color
from gmdkit.models.object import Object
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class AnimateTrigger(TriggerObject):
    target_id: int = Field(51)
    animation_id: int = Field(76)


class ColorTrigger(TriggerObject):
    red: int = Field(7)
    green: int = Field(8)
    blue: int = Field(9)
    duration: float = Field(10)
    tint_ground: bool = Field(14)
    player_1: bool = Field(15)
    player_2: bool = Field(16)
    blending: bool = Field(17)
    color_channel: int = Field(23)
    opacity: float = Field(35)
    hsv: HSV = Field(49)
    copy_id: int = Field(50)
    copy_opacity: bool = Field(60)
    disable_legacy_hsv: bool = Field(210)
    

    @classmethod
    def from_color(cls, color:Color) -> Self:
        new = cls(Object.default(899))
        new.red = color.red
        new.green = color.green
        new.blue = color.blue

        match color.player:
            case 1: new.player_1 = True
            case 2: new.player_2 = True
            case _: pass

        new.blending = color.blending
        new.color_channel = color.channel
        new.opacity = color.opacity
        new.copy_id = color.copy_id
        if color.has_hsv(): new.hsv = color.hsv
        if color.copy_opacity: color.copy_opacity = True

        return new

    def to_color(self) -> Color:
        color = Color()
        color.red = self.red
        color.green = self.green
        color.blue = self.blue            
        color.blending = self.blending
        color.channel = self.color_channel
        color.opacity = self.opacity
        color.copy_id = self.copy_id
        color.hsv = self.hsv
        color.copy_opacity = self.copy_opacity
        
        if self.player_1:
            color.player = enums.TargetPlayer.P1
        elif self.player_2:
            color.player = enums.TargetPlayer.P1
        else:
            color.player = enums.TargetPlayer.NONE

        return color
    

class PulseTrigger(TriggerObject):
    red: int = Field(7)
    green: int = Field(8)
    blue: int = Field(9)
    fade_in: float = Field(45)
    hold: float = Field(46)
    fade_out: float = Field(47)
    color_type: enums.PulseColorType = Field(48)
    hsv: HSV = Field(49)
    copy_id: int = Field(50)
    target_id: int = Field(51)
    target_type: enums.PulseTarget = Field(52)
    main_only: bool = Field(65)
    detail_only: bool = Field(66)
    exclusive: bool = Field(86)
    disable_static_hsv: bool = Field(210)


class AlphaTrigger(TriggerObject):
    duration: float = Field(10)
    opacity: float = Field(35)
    group_id: int = Field(51)


class GradientTrigger(TriggerObject):
    blending: enums.GradientBlending = Field(174)
    layer: enums.GradientLayer = Field(202)
    u_id: int = Field(203)
    bl_id: int = Field(203)
    d_id: int = Field(204)
    br_id: int = Field(204)
    l_id: int = Field(205)
    tl_id: int = Field(205)
    r_id: int = Field(206)
    tr_id: int = Field(206)
    vertex_mode: bool = Field(207)
    disable: bool = Field(208)
    gradient_id: int = Field(209)
    preview_opacity: float = Field(456)
    disable_all: bool = Field(508)


class BackgroundTrigger(TriggerObject):
    bg_id: int = Field(533)


class GroundTrigger(TriggerObject):
    # this trigger displays line options but they don't get saved
    gr_id: int = Field(533)


class MiddlegroundTrigger(TriggerObject):
    mg_id: int = Field(533)


class MgEditTrigger(TriggerObject):
    duration: float = Field(10)
    offset_y: float = Field(29)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)


class BgSpeedTrigger(TriggerObject):
    x_mod: float = Field(143)
    y_mod: float = Field(144)


class MgSpeedTrigger(TriggerObject):
    x_mod: float = Field(143)
    y_mod: float = Field(144)


class SpawnParticleTrigger(TriggerObject):
    particle_group: int = Field(51)
    position_group: int = Field(71)
    offset_x: float = Field(547)
    offset_y: float = Field(548)
    offvar_x: float = Field(549)
    offvar_y: float = Field(550)
    match_rot: bool = Field(551)
    rotation: float = Field(552)
    rotation_rand: float = Field(553)
    scale: float = Field(554)
    scale_rand: float = Field(555)


# AnimateTrigger
register_id(1585, AnimateTrigger)  # Animate Trigger

# AlphaTrigger
register_id(1007, AlphaTrigger)  # Alpha Trigger

# BackgroundTrigger
register_id(3029, BackgroundTrigger)  # Change Background Trigger

# BgSpeedTrigger
register_id(3606, BgSpeedTrigger)  # Background Speed Trigger

# ColorTrigger
register_id(899, ColorTrigger)  # Color Trigger

# GradientTrigger
register_id(2903, GradientTrigger)  # Gradient Trigger

# GroundTrigger
register_id(3030, GroundTrigger)  # Change Ground Trigger

# MgEditTrigger
register_id(2999, MgEditTrigger)  # Edit Middleground Trigger

# MgSpeedTrigger
register_id(3612, MgSpeedTrigger)  # Middleground Speed Trigger

# MiddlegroundTrigger
register_id(3031, MiddlegroundTrigger)  # Change Middleground Trigger

# PulseTrigger
register_id(1006, PulseTrigger)  # Pulse Trigger

# SpawnParticleTrigger
register_id(3608, SpawnParticleTrigger)  # Spawn Particle Trigger