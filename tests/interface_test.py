from gmdkit import Object
from gmdkit.models import interfaces

obj = Object.default(1913)
intf = obj.require_interface(interfaces.ZoomCameraTrigger)
intf.zoom