# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class CountTrigger(TriggerObject):
    target_id: int = Field(51)
    activate_group: bool = Field(56)
    target_count: int = Field(77)
    item_id: int = Field(80)
    multi_activate: bool = Field(104)


class PickupTrigger(TriggerObject):
    count: int = Field(77)
    item_id: int = Field(80)
    mode: enums.InstantCountMode = Field(88)
    override: bool = Field(139)
    mod: float = Field(449)


class InstantCountTrigger(TriggerObject):
    target_id: int = Field(51)
    activate_group: bool = Field(56)
    target_count: int = Field(77)
    item_id: int = Field(80)
    mode: enums.InstantCountMode = Field(88)


class ItemLabel(TriggerObject):
    item_id: int = Field(80)
    seconds_only: bool = Field(389)
    special_id: enums.ItemLabelSpecialID = Field(390)
    alignment: enums.ItemLabelAlignment = Field(391)
    time_counter: bool = Field(466)
    kerning: int = Field(488)


class ItemEditTrigger(TriggerObject):
    target_item_id: int = Field(51)
    item_id_1: int = Field(80)
    item_id_2: int = Field(95)
    item_type_1: enums.ItemType = Field(476)
    item_type_2: enums.ItemType = Field(477)
    target_item_type: enums.ItemType = Field(478)
    mod: float = Field(479)
    assign_op: enums.ItemOperation = Field(480)
    item_op: enums.ItemOperation = Field(481)
    mod_op: enums.ItemOperation = Field(482)
    round_op_1: enums.ItemRoundOp = Field(485)
    round_op_2: enums.ItemRoundOp = Field(486)
    sign_op_1: enums.ItemSignOp = Field(578)
    sign_op_2: enums.ItemSignOp = Field(579)


class ItemCompareTrigger(TriggerObject):
    true_id: int = Field(51)
    false_id: int = Field(71)
    item_id_1: int = Field(80)
    item_id_2: int = Field(95)
    item_type_1: enums.ItemType = Field(476)
    item_type_2: enums.ItemType = Field(477)
    mod_1: float = Field(479)
    item_op_1: enums.ItemOperation = Field(480)
    item_op_2: enums.ItemOperation = Field(481)
    comp_op: enums.ItemOperation = Field(482)
    mod_2: float = Field(483)
    tolerance: float = Field(484)
    round_op_1: enums.ItemRoundOp = Field(485)
    round_op_2: enums.ItemRoundOp = Field(486)
    sign_op_1: enums.ItemSignOp = Field(578)
    sign_op_2: enums.ItemSignOp = Field(579)


class ItemPersistTrigger(TriggerObject):
    item_id: int = Field(80)
    set_persistent: bool = Field(491)
    target_all: bool = Field(492)
    reset: bool = Field(493)
    timer: bool = Field(494)


class TimerTrigger(TriggerObject):
    target_id: int = Field(51)
    item_id: int = Field(80)
    start_time: float = Field(467)
    dont_override: bool = Field(468)
    ignore_timewarp: bool = Field(469)
    time_mod: float = Field(470)
    start_paused: bool = Field(471)
    stop_time: float = Field(473)
    stop: bool = Field(474)


class TimerEventTrigger(TriggerObject):
    target_id: int = Field(51)
    item_id: int = Field(80)
    target_time: float = Field(473)
    multi_activate: bool = Field(475)


class TimerControlTrigger(TriggerObject):
    item_id: int = Field(80)
    control_mode: enums.TimeControlType = Field(472)


# CountTrigger
register_id(1611, CountTrigger)  # Count Trigger

# InstantCountTrigger
register_id(1811, InstantCountTrigger)  # Instant Count Trigger

# ItemCompareTrigger
register_id(3620, ItemCompareTrigger)  # Item Compare Trigger

# ItemEditTrigger
register_id(3619, ItemEditTrigger)  # Item Edit Trigger

# ItemLabel
register_id(1615, ItemLabel)  # Counter Label

# ItemPersistTrigger
register_id(3641, ItemPersistTrigger)  # Persistent Item Setup Trigger

# PickupTrigger
register_id(1817, PickupTrigger)  # Pickup Trigger

# TimerControlTrigger
register_id(3617, TimerControlTrigger)  # Time Control Trigger

# TimerEventTrigger
register_id(3615, TimerEventTrigger)  # Time Event Trigger

# TimerTrigger
register_id(3614, TimerTrigger)  # Time Trigger