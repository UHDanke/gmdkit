# Package Imports
from gmdkit import enums
from gmdkit.models.interfaces.base import EffectObject, Field, register_id
from gmdkit.models.interfaces.animated import SpinningObject


class GameplayObject(EffectObject):
    disable_multi_activate: bool = Field(444)


class PadObject(GameplayObject):
    reverse: bool = Field(117)


class OrbObject(GameplayObject):
    reverse: bool = Field(117)
    
    
class DashOrbObject(OrbObject):
    speed: float = Field(586)
    collide: bool = Field(587)
    end_boost: float = Field(588)
    stop_slide: bool = Field(589)
    max_duration: float = Field(590)


class SpinningOrbObject(SpinningObject,OrbObject):
    pass


class PortalObject(GameplayObject):
    pass


class GamemodePortalObject(PortalObject):
    pass


class ToggleBlock(GameplayObject):
    group_id: int = Field(51)
    activate_group: bool = Field(56)
    claim_touch: bool = Field(445)
    spawn_only: bool = Field(504)


class ForceBlock(GameplayObject):
    value: float = Field(149)
    value_min: float = Field(526)
    value_max: float = Field(527)
    relative: bool = Field(528)
    value_range: bool = Field(529)
    force_id: int = Field(530)


class StartPosition(EffectObject):
    gamemode: enums.Gamemode = Field('kA2')
    mini_mode: bool = Field('kA3')
    speed: enums.Speed = Field('kA4')
    dual_mode: bool = Field('kA8')
    flip_gravity: bool = Field('kA11')
    target_order: int = Field('kA19')
    reverse_mode: bool = Field('kA20')
    disable: bool = Field('kA21')
    target_channel: int = Field('kA26')
    mirror_mode: bool = Field('kA28')
    rotate_mode: bool = Field('kA29')
    reset_camera: bool = Field('kA35')
    
    
# DashOrbObject
register_id(1704, DashOrbObject)  # Green Dash Orb
register_id(1751, DashOrbObject)  # Pink Gravity Dash Orb

# OrbObject
register_id(36, OrbObject)  # Yellow Jump Orb
register_id(84, OrbObject)  # Blue Gravity Orb
register_id(141, OrbObject)  # Pink Jump Orb
register_id(1333, OrbObject)  # Red Jump Orb
register_id(3004, OrbObject)  # Spider Orb

# SpinningOrbObject
register_id(1022, SpinningOrbObject)  # Green Gravity Orb
register_id(1330, SpinningOrbObject)  # Black Drop Orb

# PortalObject
register_id(10, PortalObject)  # Blue Gravity Portal
register_id(11, PortalObject)  # Yellow Gravity Portal
register_id(45, PortalObject)  # Orange Mirror Portal
register_id(46, PortalObject)  # Blue Mirror Portal
register_id(99, PortalObject)  # Green Size Portal
register_id(101, PortalObject)  # Pink Size Portal
register_id(200, PortalObject)  # Yellow Slow Speed Portal
register_id(201, PortalObject)  # Blue Normal Speed Portal
register_id(202, PortalObject)  # Green Fast Speed Portal
register_id(203, PortalObject)  # Pink Fast Speed Portal
register_id(1334, PortalObject)  # Red Fast Speed Portal
register_id(2926, PortalObject)  # Green Gravity Portal

# PadObject
register_id(35, PadObject)  # Yellow Jump Pad
register_id(67, PadObject)  # Blue Gravity Pad
register_id(140, PadObject)  # Pink Jump Pad
register_id(1332, PadObject)  # Red Jump Pad
register_id(3005, PadObject)  # Spider Pad

# GamemodePortalObject
register_id(12, GamemodePortalObject)  # Cube Portal
register_id(13, GamemodePortalObject)  # Ship Portal
register_id(47, GamemodePortalObject)  # Ball Portal
register_id(111, GamemodePortalObject)  # UFO Portal
register_id(286, GamemodePortalObject)  # Dual Portal
register_id(287, GamemodePortalObject)  # Exit Dual Portal
register_id(660, GamemodePortalObject)  # Wave Portal
register_id(745, GamemodePortalObject)  # Robot Portal
register_id(1331, GamemodePortalObject)  # Spider Portal
register_id(1933, GamemodePortalObject)  # Swing Portal

# EffectObject
register_id(1755, EffectObject)  # Allow Wave Drag Modifier
register_id(1813, EffectObject)  # Stop Jump Buffer Modifier
register_id(1829, EffectObject)  # Stop Dash Modifier
register_id(1859, EffectObject)  # Allow Head Collision Modifier
register_id(2866, EffectObject)  # Gravity Flip Modifier

# ForceBlock
register_id(2069, ForceBlock)  # Force Block
register_id(3645, ForceBlock)  # Force Circle

# StartPosition
register_id(31, StartPosition)  # Start Position

# ToggleBlock
register_id(1594, ToggleBlock)  # Toggle Orb
register_id(3643, ToggleBlock)  # Player Touch Toggle Block