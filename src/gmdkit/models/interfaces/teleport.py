# Package Imports
from gmdkit.utils import enums
from gmdkit.serialization.classes import BaseInterface
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id
from gmdkit.models.interfaces.gameplay import OrbObject, PortalObject

class TeleportSettings(BaseInterface):
    smooth_ease: bool = Field(55) #
    use_force: bool = Field(345) #
    force: float = Field(346) #
    redirect_force: bool = Field(347) #
    force_min: float = Field(348) #
    force_max: float = Field(349) #
    exit_portal_force_mod: float = Field(350) #
    keep_offset: bool = Field(351) #
    ignore_x: bool = Field(352) #
    ignore_y: bool = Field(353) #
    gravity: enums.GravityMode = Field(354) #
    additive_force: bool = Field(443) #
    instant_camera: bool = Field(464) #
    snap_ground: bool = Field(510) #
    redirect_dash: bool = Field(591) #


class LinkedTeleportPortal(TeleportSettings,PortalObject):
    portal_distance: float = Field(54)

    
class TeleportTrigger(TeleportSettings,TriggerObject):
    target_id: int = Field(51)


class TeleportOrb(TeleportSettings,OrbObject):
    target_id: int = Field(51)

    
class UnlinkedTeleportPortal(TeleportSettings,PortalObject):
    target_id: int = Field(51)


# LinkedTeleportPortal
register_id(747, LinkedTeleportPortal)  # Linked Teleport Portals

# TriggerObject
register_id(2064, PortalObject)  # Unlinked Orange Teleport Portal

# UnlinkedTeleportPortal
register_id(2902, UnlinkedTeleportPortal)  # Unlinked Blue Teleport Portal

# TeleportTrigger
register_id(3022, TeleportTrigger)  # Teleport Trigger

# TeleportOrb
register_id(3027, TeleportOrb)  # Teleport Orb