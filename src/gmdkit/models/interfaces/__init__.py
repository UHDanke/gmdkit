# --- Object interface logic ---
# Don't use these as object class reference for Geometry Dash, they don't match.
# GD's object classes are a disaster and should have been split into subclasses.
# Game class references are kept purely for mapping objects to gmdkit classes.


from .objects import *
from .triggers import *
from .gameplay import *
from .visual import *
from .misc import *

from .base import LevelSettings, BaseObject, TriggerObject
from .triggers.audio import (
    BPMTrigger, SFXTrigger, SongTrigger, EditSFXTrigger, EditSongTrigger
    )
from .triggers.camera import (
    ZoomCameraTrigger, StaticCameraTrigger, OffsetCameraTrigger,
    RotateCameraTrigger, CameraEdgeTrigger, CameraModeTrigger,
    CameraGuide, ShakeTrigger
    )
from .triggers.shaders import (
    ShaderOptions, BulgeShader, ChromaticShader, ChromaticGlitchShader,
    EditColorShader, GlitchShader, GrayScaleShader, HueShader,
    InvertColorShader, LensCircleShader, MotionBlurShader, PinchShader,
    PixelateShader, RadialBlurShader, SepiaShader, ShockLineShader,
    ShockwaveShader, SplitScreenShader
    )