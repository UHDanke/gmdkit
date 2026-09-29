# Package Imports
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class CollisionTrigger(TriggerObject):
    target_id: int = Field(51)
    activate_group: bool = Field(56)
    block_a: int = Field(80)
    on_exit: bool = Field(93)
    block_b: int = Field(95)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    between_players: bool = Field(201)


class CollisionBlock(TriggerObject):
    block_id: int = Field(80)
    dynamic: bool = Field(94)


class InstantCollisionTrigger(TriggerObject):
    true_id: int = Field(51)
    false_id: int = Field(71)
    block_a: int = Field(80)
    block_b: int = Field(95)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    between_players: bool = Field(201)
    dont_reset_remap: bool = Field(600)


class StateBlock(TriggerObject):
    state_on: int = Field(51)
    state_off: int = Field(71)

    
# CollisionTrigger
register_id(1815, CollisionTrigger)  # Collision Trigger

# CollisionBlock
register_id(1816, CollisionBlock)  # Collision Block

# InstantCollisionTrigger
register_id(3609, InstantCollisionTrigger)  # Instant Collision Trigger

# StateBlock
register_id(3640, StateBlock)  # Collision State Block