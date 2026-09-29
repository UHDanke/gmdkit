# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import (
    TriggerObject, BaseObject, Field, register_id
    )
from gmdkit.models.prop.events import EventList
from gmdkit.models.prop.sequence import SequenceList
from gmdkit.models.prop.random import RandomWeightsList
from gmdkit.models.prop.remaps import RemapList


class ToggleTrigger(TriggerObject):
    group_id: int = Field(51)
    activate_group: bool = Field(56)


class SpawnTrigger(TriggerObject):
    group_id: int = Field(51)
    delay: float = Field(63)
    disable_preview: bool = Field(102)
    ordered: bool = Field(441)
    remaps: RemapList = Field(442)
    delay_rand: float = Field(556)
    reset_remap: bool = Field(581)


class TouchTrigger(TriggerObject):
    group_id: int = Field(51)
    hold_mode: bool = Field(81)
    toggle_mode: enums.TouchMode = Field(82)
    dual_mode: bool = Field(89)
    only_player: enums.TargetPlayer = Field(198)


class RandomTrigger(TriggerObject):
    chance: float = Field(10)
    true_id: int = Field(51)
    false_id: int = Field(71)


class AdvancedRandomTrigger(TriggerObject):
    group_weights: RandomWeightsList = Field(152)


class SequenceTrigger(TriggerObject):
    sequence: SequenceList = Field(435)
    mode: enums.SequenceMode = Field(436)
    min_interval: float = Field(437)
    reset_time: float = Field(438)
    reset_type: enums.SequenceResetType = Field(439)
    unique_remap: bool = Field(505)


class EventTrigger(TriggerObject):
    spawn_id: int = Field(51)
    events: EventList = Field(430)
    extra_id_1: int = Field(447)
    extra_id_2: enums.TargetPlayer = Field(525)


class OnDeathTrigger(TriggerObject):
    group_id: int = Field(51)
    activate_group: bool = Field(56)


class ResetTrigger(TriggerObject):
    group_id: int = Field(51)


class StopTrigger(TriggerObject):
    target_id: int = Field(51)
    use_control_id: bool = Field(535)
    mode: enums.StopMode = Field(580)


class ObjectControlTrigger(TriggerObject): # unused
    target_id: int = Field(51)


class LinkVisibleTrigger(TriggerObject):
    group_id: int = Field(51)


class UITrigger(TriggerObject):
    group_id: int = Field(51)
    ui_target: int = Field(71)
    ref_x: enums.UIRef = Field(385)
    ref_y: enums.UIRef = Field(386)
    relative_x: bool = Field(387)
    relative_y: bool = Field(388)

    
class TimewarpTrigger(TriggerObject):
    time_mod: float = Field(120)


class Template(BaseObject):
    reference_only: bool = Field(157)


class Text(BaseObject):
    data: str = Field(31)
    kerning: int = Field(488)


# AdvancedRandomTrigger
register_id(2068, AdvancedRandomTrigger)  # Advanced Random Trigger

# EventTrigger
register_id(3604, EventTrigger)  # Event Trigger

# LinkVisibleTrigger
register_id(3662, LinkVisibleTrigger)  # Link Visible Trigger

# ObjectControlTrigger
register_id(3655, ObjectControlTrigger)  # Object Control Trigger

# OnDeathTrigger
register_id(1812, OnDeathTrigger)  # On Death Trigger

# RandomTrigger
register_id(1912, RandomTrigger)  # Random Trigger

# ResetTrigger
register_id(3618, ResetTrigger)  # Reset Trigger

# SequenceTrigger
register_id(3607, SequenceTrigger)  # Sequence Trigger

# SpawnTrigger
register_id(1268, SpawnTrigger)  # Spawn Trigger

# StopTrigger
register_id(1616, StopTrigger)  # Stop Trigger

# ToggleTrigger
register_id(1049, ToggleTrigger)  # Toggle Trigger

# TouchTrigger
register_id(1595, TouchTrigger)  # Touch Trigger

# Timewarp
register_id(1935, TimewarpTrigger)  # TimeWarp Trigger

# UITrigger
register_id(3613, UITrigger)  # UI Trigger

# TriggerObject
register_id(29, TriggerObject)  # Old Background Color Trigger
register_id(30, TriggerObject)  # Old Ground Color Trigger
register_id(32, TriggerObject)  # Enable Ghost Trail
register_id(33, TriggerObject)  # Disable Ghost Trail
register_id(105, TriggerObject)  # Old Object Color Trigger
register_id(744, TriggerObject)  # Old 3D Line Color Trigger
register_id(900, TriggerObject)  # Old Ground 2 Color Trigger
register_id(915, TriggerObject)  # Old Line Color Trigger
register_id(1612, TriggerObject)  # Hide Player Trigger
register_id(1613, TriggerObject)  # Show Player Trigger
register_id(1818, TriggerObject)  # Background Effect On Trigger
register_id(1819, TriggerObject)  # Background Effect Off Trigger
register_id(1917, TriggerObject)  # Reverse Trigger

# Template
register_id(2895, Template)  # Smart Template Square
register_id(2896, Template)  # Smart Template Slope
register_id(2897, Template)  # Smart Template Wide Slope

# Text
register_id(914, Text)  # Text