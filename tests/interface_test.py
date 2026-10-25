from gmdkit import Object
from gmdkit.models import interfaces

obj = Object.from_editor(1913)
intf = obj.require_interface(interfaces.ZoomCameraTrigger)
intf.zoom