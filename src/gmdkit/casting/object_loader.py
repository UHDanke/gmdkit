from gmdkit.utils import enums
from gmdkit.serialization.type_cast import (
    to_bool, from_bool,
    from_float,
    decode_text, encode_text,
    to_numkey
    )
from gmdkit.serialization.classes import FieldInterface, AliasField
from gmdkit.serialization.mixins import DictDecoderMixin
from gmdkit.models.prop.groups import IDList
from gmdkit.models.prop.events import EventList
from gmdkit.models.prop.sequence import SequenceList
from gmdkit.models.prop.random import RandomWeightsList
from gmdkit.models.prop.remaps import RemapList
from gmdkit.models.prop.guideline import GuidelineList
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.prop.particle import Particle
from gmdkit.models.prop.color import Color, ColorList


class FieldLoaderMixin(DictDecoderMixin, FieldInterface):
    KEY_DECODER = to_numkey
    KEY_ENCODER = str

FieldLoaderMixin.add_field(key=1, decoder=int, default=0)
FieldLoaderMixin.add_field(key=2, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=3, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=4, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=5, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=6, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=7, decoder=int, default=0)
FieldLoaderMixin.add_field(key=8, decoder=int, default=0)
FieldLoaderMixin.add_field(key=9, decoder=int, default=0)
FieldLoaderMixin.add_field(key=10, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=11, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=12, decoder=int, default=0)
FieldLoaderMixin.add_field(key=13, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=14, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=15, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=16, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=17, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=19, decoder=enums.OldColor, default=0)
FieldLoaderMixin.add_field(key=20, decoder=int, default=0)
FieldLoaderMixin.add_field(key=21, decoder=int, default=0)
FieldLoaderMixin.add_field(key=22, decoder=int, default=0)
FieldLoaderMixin.add_field(key=23, decoder=int, default=0)
FieldLoaderMixin.add_field(key=24, decoder=int, default=0)
FieldLoaderMixin.add_field(key=25, decoder=int, default=0)
FieldLoaderMixin.add_field(key=28, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=29, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=30, decoder=enums.Easing, default=enums.Easing.NONE)
FieldLoaderMixin.add_field(key=31, decoder=decode_text, encoder=encode_text, default="")
FieldLoaderMixin.add_field(key=32, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=34, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=35, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=36, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=41, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=42, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=43, decoder=HSV.from_string, encoder=HSV.to_string, default_factory=HSV)
FieldLoaderMixin.add_field(key=44, decoder=HSV.from_string, encoder=HSV.to_string, default_factory=HSV)
FieldLoaderMixin.add_field(key=45, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=46, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=47, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=48, decoder=enums.PulseColorType, default=enums.PulseColorType.COLOR)
FieldLoaderMixin.add_field(key=49, decoder=HSV.from_string, encoder=HSV.to_string, default_factory=HSV)
FieldLoaderMixin.add_field(key=50, decoder=int, default=0)
FieldLoaderMixin.add_field(key=51, decoder=int, default=0)
FieldLoaderMixin.add_field(key=52, decoder=enums.PulseTarget, default=enums.PulseTarget.CHANNEL)
FieldLoaderMixin.add_field(key=54, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=55, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=56, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=57, decoder=IDList.from_string, encoder=IDList.to_string, default_factory=IDList)
FieldLoaderMixin.add_field(key=58, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=59, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=60, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=61, decoder=int, default=0)
FieldLoaderMixin.add_field(key=62, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=63, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=64, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=65, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=66, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=67, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=68, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=69, decoder=int, default=0)
FieldLoaderMixin.add_field(key=70, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=71, decoder=int, default=0)
FieldLoaderMixin.add_field(key=72, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=73, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=75, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=76, decoder=int, default=0)
FieldLoaderMixin.add_field(key=77, decoder=int, default=0)
FieldLoaderMixin.add_field(key=78, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=80, decoder=int, default=0)
FieldLoaderMixin.add_field(key=81, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=82, decoder=enums.TouchMode, default=enums.TouchMode.TOGGLE)
FieldLoaderMixin.add_field(key=84, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=85, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=86, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=87, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=88, decoder=enums.InstantCountMode, default=enums.InstantCountMode.EQUAL)
FieldLoaderMixin.add_field(key=89, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=90, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=91, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=92, decoder=int, default=0)
FieldLoaderMixin.add_field(key=93, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=94, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=95, decoder=int, default=0)
FieldLoaderMixin.add_field(key=96, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=97, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=98, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=99, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=100, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=101, decoder=enums.TargetAxis, default=enums.TargetAxis.NONE)
FieldLoaderMixin.add_field(key=102, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=103, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=104, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=105, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=106, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=107, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=108, decoder=int, default=0)
FieldLoaderMixin.add_field(key=110, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=111, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=112, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=113, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=114, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=115, decoder=int, default=0)
FieldLoaderMixin.add_field(key=116, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=117, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=118, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=120, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=121, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=122, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=123, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=126, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=127, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=128, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=129, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=131, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=132, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=133, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=134, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=135, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=136, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=137, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=138, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=139, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=141, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=142, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=143, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=144, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=145, decoder=Particle.from_string, encoder=Particle.to_string, default_factory=Particle)
FieldLoaderMixin.add_field(key=146, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=147, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=148, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=149, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=150, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=151, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=152, decoder=RandomWeightsList.from_string, encoder=RandomWeightsList.to_string, default_factory=RandomWeightsList)
FieldLoaderMixin.add_field(key=153, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=154, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=155, decoder=int, default=0)
FieldLoaderMixin.add_field(key=156, decoder=int, default=0)
FieldLoaderMixin.add_field(key=157, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=159, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=160, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=161, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=162, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=163, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=164, decoder=enums.CameraEdge, default=enums.CameraEdge.NONE)
FieldLoaderMixin.add_field(key=165, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=166, decoder=enums.ArrowDir, default=enums.ArrowDir.NONE)
FieldLoaderMixin.add_field(key=167, decoder=enums.ArrowDir, default=enums.ArrowDir.NONE)
FieldLoaderMixin.add_field(key=169, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=170, decoder=int, default=0)
FieldLoaderMixin.add_field(key=171, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=172, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=173, decoder=int, default=0)
FieldLoaderMixin.add_field(key=174, decoder=enums.GradientBlending, default=enums.GradientBlending.NORMAL)
FieldLoaderMixin.add_field(key=175, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=176, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=177, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=179, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=180, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=181, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=182, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=183, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=184, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=185, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=186, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=187, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=188, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=189, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=190, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=191, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=192, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=193, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=194, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=195, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=196, decoder=enums.GradientLayer, default=enums.GradientLayer.BG)
FieldLoaderMixin.add_field(key=197, decoder=enums.GradientLayer, default=enums.GradientLayer.MAX)
FieldLoaderMixin.add_field(key=198, decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key=199, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=200, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=201, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=202, decoder=enums.GradientLayer, default=enums.GradientLayer.BG)
FieldLoaderMixin.add_field(key=203, decoder=int, default=0)
FieldLoaderMixin.add_field(key=204, decoder=int, default=0)
FieldLoaderMixin.add_field(key=205, decoder=int, default=0)
FieldLoaderMixin.add_field(key=206, decoder=int, default=0)
FieldLoaderMixin.add_field(key=207, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=208, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=209, decoder=int, default=0)
FieldLoaderMixin.add_field(key=210, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=211, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=212, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=213, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=214, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=217, decoder=enums.EnterMode, default=enums.EnterMode.NONE)
FieldLoaderMixin.add_field(key=218, decoder=int, default=0)
FieldLoaderMixin.add_field(key=219, decoder=int, default=0)
FieldLoaderMixin.add_field(key=220, decoder=int, default=0)
FieldLoaderMixin.add_field(key=221, decoder=int, default=0)
FieldLoaderMixin.add_field(key=222, decoder=int, default=0)
FieldLoaderMixin.add_field(key=223, decoder=int, default=0)
FieldLoaderMixin.add_field(key=224, decoder=int, default=0)
FieldLoaderMixin.add_field(key=225, decoder=int, default=0)
FieldLoaderMixin.add_field(key=231, decoder=int, default=0)
FieldLoaderMixin.add_field(key=232, decoder=int, default=0)
FieldLoaderMixin.add_field(key=233, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=234, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=235, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=236, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=237, decoder=int, default=0)
FieldLoaderMixin.add_field(key=238, decoder=int, default=0)
FieldLoaderMixin.add_field(key=239, decoder=int, default=0)
FieldLoaderMixin.add_field(key=240, decoder=int, default=0)
FieldLoaderMixin.add_field(key=241, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=242, decoder=enums.Easing, default=enums.Easing.NONE)
FieldLoaderMixin.add_field(key=243, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=248, decoder=enums.Easing, default=enums.Easing.NONE)
FieldLoaderMixin.add_field(key=249, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=252, decoder=int, default=0)
FieldLoaderMixin.add_field(key=253, decoder=int, default=0)
FieldLoaderMixin.add_field(key=260, decoder=int, default=0)
FieldLoaderMixin.add_field(key=261, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=262, decoder=int, default=0)
FieldLoaderMixin.add_field(key=263, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=264, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=265, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=270, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=271, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=274, decoder=IDList.from_string, encoder=IDList.to_string, default_factory=IDList)
FieldLoaderMixin.add_field(key=275, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=276, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=278, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=279, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=280, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=281, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=282, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=283, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=284, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=285, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=286, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=287, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=288, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=289, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=290, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=291, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=292, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=293, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=298, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=299, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=300, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=301, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=305, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=306, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=307, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=308, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=309, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=310, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=311, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=312, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=313, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=314, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=315, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=316, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=317, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=318, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=319, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=320, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=321, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=322, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=323, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=324, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=325, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=326, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=327, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=328, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=329, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=330, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=331, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=332, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=333, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=334, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=335, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=336, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=337, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=338, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=339, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=340, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=341, decoder=int, default=0)
FieldLoaderMixin.add_field(key=343, decoder=int, default=0)
FieldLoaderMixin.add_field(key=344, decoder=int, default=0)
FieldLoaderMixin.add_field(key=345, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=346, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=347, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=348, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=349, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=350, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=351, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=352, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=353, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=354, decoder=enums.GravityMode, default=enums.GravityMode.NONE)
FieldLoaderMixin.add_field(key=355, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=356, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=357, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=358, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=359, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=360, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=361, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=362, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=363, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=364, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=365, decoder=int, default=0)
FieldLoaderMixin.add_field(key=366, decoder=int, default=0)
FieldLoaderMixin.add_field(key=367, decoder=enums.AdvFollowMode, default=enums.AdvFollowMode.MODE_1)
FieldLoaderMixin.add_field(key=368, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=369, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=370, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=371, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=372, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=373, decoder=int, default=0)
FieldLoaderMixin.add_field(key=374, decoder=int, default=0)
FieldLoaderMixin.add_field(key=375, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=376, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=377, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=378, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=379, decoder=enums.KeyframeRefMode, default=enums.KeyframeRefMode.TIME)
FieldLoaderMixin.add_field(key=380, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=381, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=382, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=383, decoder=int, default=0)
FieldLoaderMixin.add_field(key=385, decoder=enums.UIRef, default=enums.UIRef.AUTO_X)
FieldLoaderMixin.add_field(key=386, decoder=enums.UIRef, default=enums.UIRef.AUTO_Y)
FieldLoaderMixin.add_field(key=387, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=388, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=389, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=390, decoder=enums.ItemLabelSpecialID, default=enums.ItemLabelSpecialID.NONE)
FieldLoaderMixin.add_field(key=391, decoder=enums.ItemLabelAlignment, default=enums.ItemLabelAlignment.CENTER)
FieldLoaderMixin.add_field(key=392, decoder=int, default=0)
FieldLoaderMixin.add_field(key=393, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=394, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=395, decoder=int, default=0)
FieldLoaderMixin.add_field(key=396, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=397, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=399, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=400, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=401, decoder=int, default=0)
FieldLoaderMixin.add_field(key=402, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=403, decoder=int, default=0)
FieldLoaderMixin.add_field(key=404, decoder=int, default=0)
FieldLoaderMixin.add_field(key=405, decoder=int, default=0)
FieldLoaderMixin.add_field(key=406, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=407, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=408, decoder=int, default=0)
FieldLoaderMixin.add_field(key=409, decoder=int, default=0)
FieldLoaderMixin.add_field(key=410, decoder=int, default=0)
FieldLoaderMixin.add_field(key=411, decoder=int, default=0)
FieldLoaderMixin.add_field(key=412, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=413, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=414, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=415, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=416, decoder=int, default=0)
FieldLoaderMixin.add_field(key=417, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=418, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=419, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=420, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=421, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=422, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=423, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=424, decoder=int, default=0)
FieldLoaderMixin.add_field(key=425, decoder=int, default=0)
FieldLoaderMixin.add_field(key=426, decoder=int, default=0)
FieldLoaderMixin.add_field(key=428, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=430, decoder=EventList.from_string, encoder=EventList.to_string, default_factory=EventList)
FieldLoaderMixin.add_field(key=431, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=432, decoder=int, default=0)
FieldLoaderMixin.add_field(key=433, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=434, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=435, decoder=SequenceList.from_string, encoder=SequenceList.to_string, default_factory=SequenceList)
FieldLoaderMixin.add_field(key=436, decoder=enums.SequenceMode, default=enums.SequenceMode.STOP)
FieldLoaderMixin.add_field(key=437, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=438, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=439, decoder=enums.SequenceResetType, default=enums.SequenceResetType.RESET_FULL)
FieldLoaderMixin.add_field(key=440, decoder=int, default=0)
FieldLoaderMixin.add_field(key=441, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=442, decoder=RemapList.from_string, encoder=RemapList.to_string, default_factory=RemapList)
FieldLoaderMixin.add_field(key=443, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=444, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=445, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=446, decoder=int, default=0)
FieldLoaderMixin.add_field(key=447, decoder=int, default=0)
FieldLoaderMixin.add_field(key=448, decoder=int, default=0)
FieldLoaderMixin.add_field(key=449, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=452, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=453, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=454, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=455, decoder=int, default=0)
FieldLoaderMixin.add_field(key=456, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=457, decoder=int, default=0)
FieldLoaderMixin.add_field(key=458, decoder=enums.VolumeDirection, default=enums.VolumeDirection.CIRCULAR)
FieldLoaderMixin.add_field(key=459, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=460, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=461, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=462, decoder=int, default=0)
FieldLoaderMixin.add_field(key=463, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=464, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=465, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=466, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=467, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=468, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=469, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=470, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=471, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=472, decoder=enums.TimeControlType, default=enums.TimeControlType.START)
FieldLoaderMixin.add_field(key=473, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=474, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=475, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=476, decoder=enums.ItemType, default=enums.ItemType.DEFAULT)
FieldLoaderMixin.add_field(key=477, decoder=enums.ItemType, default=enums.ItemType.DEFAULT)
FieldLoaderMixin.add_field(key=478, decoder=enums.ItemType, default=enums.ItemType.DEFAULT)
FieldLoaderMixin.add_field(key=479, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=480, decoder=enums.ItemOperation)
FieldLoaderMixin.add_field(key=481, decoder=enums.ItemOperation)
FieldLoaderMixin.add_field(key=482, decoder=enums.ItemOperation)
FieldLoaderMixin.add_field(key=483, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=484, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=485, decoder=enums.ItemRoundOp, default=enums.ItemRoundOp.NONE)
FieldLoaderMixin.add_field(key=486, decoder=enums.ItemRoundOp, default=enums.ItemRoundOp.NONE)
FieldLoaderMixin.add_field(key=487, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=488, decoder=int, default=0)
FieldLoaderMixin.add_field(key=489, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=490, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=491, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=492, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=493, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=494, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=495, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=496, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=497, decoder=enums.SingleColorMode, default=enums.SingleColorMode.DEFAULT)
FieldLoaderMixin.add_field(key=498, decoder=int, default=0)
FieldLoaderMixin.add_field(key=499, decoder=enums.Speed, default=enums.Speed.NORMAL)
FieldLoaderMixin.add_field(key=500, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=501, decoder=int, default=0)
FieldLoaderMixin.add_field(key=502, decoder=enums.ReverbPreset, default=enums.ReverbPreset.GENERIC)
FieldLoaderMixin.add_field(key=503, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=504, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=505, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=506, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=507, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=508, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=509, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=510, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=511, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=512, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=513, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=514, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=515, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=516, decoder=int, default=0)
FieldLoaderMixin.add_field(key=517, decoder=int, default=0)
FieldLoaderMixin.add_field(key=518, decoder=int, default=0)
FieldLoaderMixin.add_field(key=519, decoder=int, default=0)
FieldLoaderMixin.add_field(key=520, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=521, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=522, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=523, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=524, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=525, decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key=526, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=527, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=528, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=529, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=530, decoder=int, default=0)
FieldLoaderMixin.add_field(key=531, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=532, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=533, decoder=int, default=0)
FieldLoaderMixin.add_field(key=534, decoder=int, default=0)
FieldLoaderMixin.add_field(key=535, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=536, decoder=enums.KeyframeSpin, default=enums.KeyframeSpin.NONE)
FieldLoaderMixin.add_field(key=537, decoder=int, default=0)
FieldLoaderMixin.add_field(key=538, decoder=enums.EffectSpecialCenter, default=enums.EffectSpecialCenter.NONE)
FieldLoaderMixin.add_field(key=539, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=540, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=541, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=542, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=543, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=544, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=545, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=546, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=547, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=548, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=549, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=550, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=551, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=552, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=553, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=554, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=555, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=556, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=557, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=558, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=559, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=560, decoder=int, default=0)
FieldLoaderMixin.add_field(key=561, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=562, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=563, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=564, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=565, decoder=int, default=0)
FieldLoaderMixin.add_field(key=566, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=567, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=568, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=569, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=570, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=571, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=572, decoder=enums.AdvFollowInit, default=enums.AdvFollowInit.INIT)
FieldLoaderMixin.add_field(key=573, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=574, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=575, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=576, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=577, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=578, decoder=enums.ItemSignOp, default=enums.ItemSignOp.NONE)
FieldLoaderMixin.add_field(key=579, decoder=enums.ItemSignOp, default=enums.ItemSignOp.NONE)
FieldLoaderMixin.add_field(key=580, decoder=enums.StopMode, default=enums.StopMode.STOP)
FieldLoaderMixin.add_field(key=581, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=582, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=583, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=584, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=585, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=586, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=587, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=588, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=589, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=590, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=591, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=592, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=593, decoder=enums.Option, default=enums.Option.IGNORE)
FieldLoaderMixin.add_field(key=595, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=596, decoder=int, default=0)
FieldLoaderMixin.add_field(key=597, decoder=int, default=0)
FieldLoaderMixin.add_field(key=598, decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key=599, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key=600, decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA1", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA2", decoder=enums.Gamemode, default=enums.Gamemode.CUBE)
FieldLoaderMixin.add_field(key="kA3", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA4", decoder=enums.Speed, default=enums.Speed.NORMAL)
FieldLoaderMixin.add_field(key="kA5", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA6", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA7", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA8", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA9", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA10", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA11", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA12", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA13", decoder=float, encoder=from_float, default=0.0)
FieldLoaderMixin.add_field(key="kA14", decoder=GuidelineList.from_string, encoder=GuidelineList.to_string, default_factory=GuidelineList)
FieldLoaderMixin.add_field(key="kA15", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA16", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA17", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA18", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA19", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA20", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA21", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA22", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA23", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA24", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA25", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA26", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA27", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA28", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA29", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA31", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA32", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA33", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA34", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA35", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA36", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA37", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA38", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA39", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA40", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA41", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA42", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA43", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA44", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA45", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA46", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kA47", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kA48", decoder=to_bool, encoder=from_bool, default=False)
FieldLoaderMixin.add_field(key="kS1", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS2", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS3", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS4", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS5", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS6", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS7", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS8", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS9", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS10", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS11", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS12", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS13", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS14", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS15", decoder=int, default=0)
FieldLoaderMixin.add_field(key="kS16", decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key="kS17", decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key="kS18", decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key="kS19", decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key="kS20", decoder=enums.TargetPlayer, default=enums.TargetPlayer.NONE)
FieldLoaderMixin.add_field(key="kS29", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS30", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS31", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS32", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS33", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS34", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS35", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS36", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS37", decoder=Color.from_string, encoder=Color.to_string, default_factory=Color)
FieldLoaderMixin.add_field(key="kS38", decoder=ColorList.from_string, encoder=ColorList.to_string, default_factory=ColorList)
FieldLoaderMixin.add_field(key="kS39", decoder=int, default=0)


"""
--- Object interface logic ---
Don't use these as object class reference for Geometry Dash, they don't match.
GD's object classes are a disaster and should have been split into subclasses.
GD class references are kept purely for mapping objects to gmdkit classes.

"""

# Class GameObject, EnhancedObject
class BaseObject(FieldLoaderMixin):
    obj_id: int = AliasField(1)
    x: float = AliasField(2)
    y: float = AliasField(3)
    flip_x: bool = AliasField(4)
    flip_y: bool = AliasField(5)
    rotation: float = AliasField(6)
    old_color_id: enums.OldColor = AliasField(19)
    editor_l1: int = AliasField(20)
    color_1: int = AliasField(21)
    color_2: int = AliasField(22)
    z_layer: int = AliasField(24)
    z_order: int = AliasField(25)
    old_scale: float = AliasField(32)
    group_parent: bool = AliasField(34)
    hsv_enabled_1: bool = AliasField(41)
    hsv_enabled_2: bool = AliasField(42)
    hsv_1: HSV = AliasField(43)
    hsv_2: HSV = AliasField(44)
    groups: IDList = AliasField(57)
    editor_l2: int = AliasField(61)
    dont_fade: bool = AliasField(64)
    dont_enter: bool = AliasField(67)
    no_glow: bool = AliasField(96)
    high_detail: bool = AliasField(103)
    linked_group: int = AliasField(108)
    no_effects: bool = AliasField(116)
    no_touch: bool = AliasField(121)
    scale_x: float = AliasField(128)
    scale_y: float = AliasField(129)
    skew_x: float = AliasField(131)
    skew_y: float = AliasField(132)
    passable: bool = AliasField(134)
    hide: bool = AliasField(135)
    nonstick_x: bool = AliasField(136)
    ice_block: bool = AliasField(137)
    color_1_index: int = AliasField(155)
    color_2_index: int = AliasField(156)
    grip_slope: bool = AliasField(193)
    target_player_2: bool = AliasField(200)
    parent_groups: IDList = AliasField(274)
    area_parent: bool = AliasField(279)
    nonstick_y: bool = AliasField(289)
    enter_channel: int = AliasField(343)
    scale_stick: bool = AliasField(356)
    disable_grid_snap: bool = AliasField(370)
    no_audio_scale: bool = AliasField(372)
    material: int = AliasField(446)
    extra_sticky: bool = AliasField(495)
    dont_boost_y: bool = AliasField(496)
    single_color_type: enums.SingleColorMode = AliasField(497)
    no_particle: bool = AliasField(507)
    dont_boost_x: bool = AliasField(509)
    extended_collision: bool = AliasField(511)

# Class AnimatedGameObject
class AnimatedObject(BaseObject):
    randomize_start: bool = AliasField(106)
    animation_speed: float = AliasField(107)
    use_speed: bool = AliasField(122)
    animate_on_trigger: bool = AliasField(123)
    delayed_loop: bool = AliasField(126)
    explosion_disable_shine: bool = AliasField(127)
    animate_active_only: bool = AliasField(214)
    single_frame: int = AliasField(462)
    offset_anim: bool = AliasField(592)

# Class ParticleGameObject
class ParticleObject(BaseObject):
    data: Particle = AliasField(145)
    use_obj_color: bool = AliasField(146)
    uniform_obj_color: bool = AliasField(147)
    quick_start: bool = AliasField(211)


class Saw(BaseObject):
    """(new, no C++ equivalent)"""
    rotation_speed: float = AliasField(97)
    disable_rotation: bool = AliasField(98)


class SpecialAnimated(BaseObject):
    """SpecialAnimGameObject"""
    pass

# Class EffectGameObject
class TriggerObject(BaseObject):
    touch_trigger: bool = AliasField(11)
    editor_preview: bool = AliasField(13)
    interactible: bool = AliasField(36)
    spawn_trigger: bool = AliasField(62)
    multi_trigger: bool = AliasField(87)
    multi_activate: bool = AliasField(99)
    order: int = AliasField(115)
    reverse: bool = AliasField(117)
    channel: int = AliasField(170)
    ignore_gparent: bool = AliasField(280)
    ignore_linked: bool = AliasField(281)
    single_ptouch: bool = AliasField(284)
    center_effect: bool = AliasField(369)
    disable_multi_activate: bool = AliasField(444)
    control_id: int = AliasField(534)

# Object 1935
class Timewarp(TriggerObject):
    time_mod: float = AliasField(120)

# Object 3016
# Class AdvancedFollowTriggerObject
class AdvancedFollowTrigger(TriggerObject):
    target_id: int = AliasField(51)
    follow_id: int = AliasField(71)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    corner: bool = AliasField(201)
    delay: float = AliasField(292)
    delay_rand: float = AliasField(293)
    max_speed: float = AliasField(298)
    max_speed_rand: float = AliasField(299)
    start_speed: float = AliasField(300)
    start_speed_rand: float = AliasField(301)
    target_dir: bool = AliasField(305)
    x_only: bool = AliasField(306)
    y_only: bool = AliasField(307)
    max_range: float = AliasField(308)
    max_range_rand: float = AliasField(309)
    steer: float = AliasField(316)
    steer_rand: float = AliasField(317)
    steer_low: float = AliasField(318)
    steer_low_rand: float = AliasField(319)
    steer_high: float = AliasField(320)
    steer_high_rand: float = AliasField(321)
    speed_range_low: float = AliasField(322)
    speed_range_low_rand: float = AliasField(323)
    speed_range_high: float = AliasField(324)
    speed_range_high_rand: float = AliasField(325)
    break_force: float = AliasField(326)
    break_force_rand: float = AliasField(327)
    break_angle: float = AliasField(328)
    break_angle_rand: float = AliasField(329)
    break_steer: float = AliasField(330)
    break_steer_rand: float = AliasField(331)
    break_steer_speed_limit: float = AliasField(332)
    break_steer_speed_limit_rand: float = AliasField(333)
    acceleration: float = AliasField(334)
    acceleration_rand: float = AliasField(335)
    ignore_disabled: bool = AliasField(336)
    steer_low_check: bool = AliasField(337)
    steer_high_check: bool = AliasField(338)
    rotate_dir: bool = AliasField(339)
    rot_offset: float = AliasField(340)
    near_accel: float = AliasField(357)
    near_accel_rand: float = AliasField(358)
    near_dist: float = AliasField(359)
    near_dist_rand: float = AliasField(360)
    easing: float = AliasField(361)
    easing_rand: float = AliasField(362)
    rot_easing: float = AliasField(363)
    rot_deadzone: float = AliasField(364)
    priority: int = AliasField(365)
    max_range_ref: int = AliasField(366)
    mode: enums.AdvFollowMode = AliasField(367)
    friction: float = AliasField(558)
    friction_rand: float = AliasField(559)
    start_speed_ref: int = AliasField(560)
    near_friction: float = AliasField(561)
    near_friction_rand: float = AliasField(562)
    start_dir: float = AliasField(563)
    start_dir_rand: float = AliasField(564)
    start_dir_ref: int = AliasField(565)
    exclusive: bool = AliasField(571)
    init: enums.AdvFollowInit = AliasField(572)

# BREAK THIS UP IN TWO
# Class AdvancedFollowEditObject
class EditAdvFollowTrigger(TriggerObject):
    """AdvancedFollowEditObject"""
    target_id: int = AliasField(51)
    follow_id: int = AliasField(71)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    corner: bool = AliasField(201)
    speed: float = AliasField(300)
    speed_rand: float = AliasField(301)
    x_only: bool = AliasField(306)
    y_only: bool = AliasField(307)
    use_control_id: bool = AliasField(535)
    speed_ref: int = AliasField(560)
    dir_angle: float = AliasField(563)
    dir_rand: float = AliasField(564)
    dir_ref: int = AliasField(565)
    mod_x: float = AliasField(566)
    mod_x_rand: float = AliasField(567)
    mod_y: float = AliasField(568)
    mod_y_rand: float = AliasField(569)

# Object 1007
class AlphaTrigger(TriggerObject):
    duration: float = AliasField(10)
    opacity: float = AliasField(35)
    group_id: int = AliasField(51)

# Object 1585
class AnimateTrigger(TriggerObject):
    target_id: int = AliasField(51)
    animation_id: int = AliasField(76)


class ArtTrigger(TriggerObject):
    """ArtTriggerGameObject"""
    bg_id: int = AliasField(533)
    gr_id: int = AliasField(533)
    mg_id: int = AliasField(533)


class BPMTrigger(TriggerObject):
    """AudioLineGuideGameObject"""
    duration: float = AliasField(10)
    bpm: int = AliasField(498)
    speed: enums.Speed = AliasField(499)
    disable: bool = AliasField(500)
    bpb: int = AliasField(501)


class BgSpeedTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    x_mod: float = AliasField(143)
    y_mod: float = AliasField(144)


class CameraTrigger(TriggerObject):
    """CameraTriggerGameObject"""
    duration: float = AliasField(10)
    offset_x: float = AliasField(28)
    offset_y: float = AliasField(29)
    easing: enums.Easing = AliasField(30)
    edge_target_id: int = AliasField(51)
    degrees: float = AliasField(68)
    add: bool = AliasField(70)
    target_id: int = AliasField(71)
    ease_rate: float = AliasField(85)
    axis: enums.TargetAxis = AliasField(101)
    exit: bool = AliasField(110)
    free_mode: bool = AliasField(111)
    edit_settings: bool = AliasField(112)
    mode_easing: float = AliasField(113)
    padding: float = AliasField(114)
    direction: enums.CameraEdge = AliasField(164)
    follow_group: bool = AliasField(212)
    follow_easing: float = AliasField(213)
    zoom: float = AliasField(371)
    snap_360: bool = AliasField(394)
    smooth_velocity: bool = AliasField(453)
    velocity_mod: float = AliasField(454)
    exit_instant: bool = AliasField(465)
    preview_opacity: float = AliasField(506)

# Object 2068
# Class RandTriggerGameObject
class AdvancedRandomTrigger(TriggerObject):
    group_weights: RandomWeightsList = AliasField(152)

# Object 3607
# Class SequenceTriggerGameObject
class SequenceTrigger(TriggerObject):
    sequence: SequenceList = AliasField(435)
    mode: enums.SequenceMode = AliasField(436)
    min_interval: float = AliasField(437)
    reset_time: float = AliasField(438)
    reset_type: enums.SequenceResetType = AliasField(439)
    unique_remap: bool = AliasField(505)

# Object 2063 
# Class CheckpointGameObject
class CheckpointTrigger(TriggerObject):
    spawn_id: int = AliasField(51)
    target_pos: int = AliasField(71)
    player_pos: bool = AliasField(138)
    respawn_id: int = AliasField(448)


class CollectibleObject(TriggerObject):
    coin_id: int = AliasField(12) # TODO SUBCLASS
    group_id: int = AliasField(51)
    sub_count: bool = AliasField(78)
    item_id: int = AliasField(80)
    pickup_item: bool = AliasField(381)
    toggle_trigger: bool = AliasField(382)
    points: int = AliasField(383)
    particle: int = AliasField(440)
    no_anim: bool = AliasField(463)

# Object 1816
class CollisionBlock(TriggerObject):
    block_id: int = AliasField(80)
    dynamic: bool = AliasField(94)

# Object 1815
class CollisionTrigger(TriggerObject):
    _10: float = AliasField(10)
    target_id: int = AliasField(51)
    activate_group: bool = AliasField(56)
    block_a: int = AliasField(80)
    on_exit: bool = AliasField(93)
    block_b: int = AliasField(95)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    between_players: bool = AliasField(201)

# Object 899
class ColorTrigger(TriggerObject):
    red: int = AliasField(7)
    green: int = AliasField(8)
    blue: int = AliasField(9)
    duration: float = AliasField(10)
    tint_ground: bool = AliasField(14)
    player_1: bool = AliasField(15)
    player_2: bool = AliasField(16)
    blending: bool = AliasField(17)
    color_channel: int = AliasField(23)
    opacity: float = AliasField(35)
    hsv: HSV = AliasField(49)
    copy_id: int = AliasField(50)
    copy_opacity: bool = AliasField(60)
    disable_legacy_hsv: bool = AliasField(210)


class CountTrigger(TriggerObject):
    """CountTriggerGameObject"""
    target_id: int = AliasField(51)
    activate_group: bool = AliasField(56)
    count: int = AliasField(77)
    item_id: int = AliasField(80)
    mode: enums.InstantCountMode = AliasField(88)
    multi_activate: bool = AliasField(104)
    override: bool = AliasField(139)
    mod: float = AliasField(449)


class EndTrigger(TriggerObject):
    """EndTriggerGameObject"""
    spawn_id: int = AliasField(51)
    target_pos: int = AliasField(71)
    no_effects: bool = AliasField(460)
    no_sfx: bool = AliasField(461)
    instant: bool = AliasField(487)


class EndWallTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    group_id: int = AliasField(51)
    lock_y: bool = AliasField(59)
    reverse: bool = AliasField(118)


class EnhancedTrigger(TriggerObject):
    """EnhancedTriggerObject"""
    pass


class EnterEffect(TriggerObject):
    """EnterEffectObject"""
    duration: float = AliasField(10)
    hsv: HSV = AliasField(49)
    target_id: int = AliasField(51)
    main_only: bool = AliasField(65)
    detail_only: bool = AliasField(66)
    center_id: int = AliasField(71)
    m_138: bool = AliasField(138)
    m_200: bool = AliasField(200)
    m_201: bool = AliasField(201)
    enter_only: enums.EnterMode = AliasField(217)
    move_dist: int = AliasField(218)
    move_dist_rand: int = AliasField(219)
    offset: int = AliasField(220)
    offset_rand: int = AliasField(221)
    length: int = AliasField(222)
    length_rand: int = AliasField(223)
    m_224: int = AliasField(224)
    effect_id: int = AliasField(225)
    move_angle: int = AliasField(231)
    move_angle_rand: int = AliasField(232)
    scale_x: float = AliasField(233)
    scale_x_rand: float = AliasField(234)
    scale_y: float = AliasField(235)
    scale_y_rand: float = AliasField(236)
    move_x: int = AliasField(237)
    move_x_rand: int = AliasField(238)
    move_y: int = AliasField(239)
    move_y_rand: int = AliasField(240)
    xy_mode: bool = AliasField(241)
    easing: enums.Easing = AliasField(242)
    easing_rate: float = AliasField(243)
    easing_2: enums.Easing = AliasField(248)
    easing_rate_2: float = AliasField(249)
    offset_y: int = AliasField(252)
    offset_y_rand: int = AliasField(253)
    tint_channel: int = AliasField(260)
    ease_out: bool = AliasField(261)
    direction: int = AliasField(262)
    mod_front: float = AliasField(263)
    mod_back: float = AliasField(264)
    tint: float = AliasField(265)
    rotate: float = AliasField(270)
    rotate_rand: float = AliasField(271)
    to_opacity: float = AliasField(275)
    inwards: bool = AliasField(276)
    enable_hsv: bool = AliasField(278)
    deadzone: float = AliasField(282)
    mirrored: bool = AliasField(283)
    m_285: float = AliasField(285)
    from_opacity: float = AliasField(286)
    relative: bool = AliasField(287)
    rfade: float = AliasField(288)
    priority: int = AliasField(341)
    enter_channel: int = AliasField(344)
    use_effect_id: bool = AliasField(355)
    special_center: enums.EffectSpecialCenter = AliasField(538)
    deap: bool = AliasField(539)

# Object 3604
# Class EventLinkTrigger
class EventTrigger(TriggerObject):
    spawn_id: int = AliasField(51)
    events: EventList = AliasField(430)
    extra_id_1: int = AliasField(447)
    extra_id_2: enums.TargetPlayer = AliasField(525)


# Object
# Class
class FollowPlayerYTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    duration: float = AliasField(10)
    target_id: int = AliasField(51)
    speed: float = AliasField(90)
    delay: float = AliasField(91)
    offset: int = AliasField(92)
    max_speed: float = AliasField(105)

# Object
# Class
class FollowTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    duration: float = AliasField(10)
    target_id: int = AliasField(51)
    follow_target: int = AliasField(71)
    mod_x: float = AliasField(72)
    mod_y: float = AliasField(73)

# Object
# Class
class ForceBlock(TriggerObject):
    """ForceBlockGameObject"""
    value: float = AliasField(149)
    value_min: float = AliasField(526)
    value_max: float = AliasField(527)
    relative: bool = AliasField(528)
    value_range: bool = AliasField(529)
    force_id: int = AliasField(530)


class GamemodePortalTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    free_mode: bool = AliasField(111)
    edit_settings: bool = AliasField(112)
    easing: float = AliasField(113)
    padding: float = AliasField(114)

# Object
# Class
class GameplayArrow(TriggerObject):
    """RotateGameplayGameObject"""
    dir_y_neg: enums.ArrowDir = AliasField(166)
    dir_x_pos: enums.ArrowDir = AliasField(167)
    edit_velocity: bool = AliasField(169)
    change_channel: bool = AliasField(171)
    channel_only: bool = AliasField(172)
    target_channel: int = AliasField(173)
    instant_offset: bool = AliasField(368)
    velocity_mod_x: float = AliasField(582)
    velocity_mod_y: float = AliasField(583)
    override_velocity: bool = AliasField(584)
    dont_slide: bool = AliasField(585)

# Object
# Class
class GameplayOffsetTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    offset_x: float = AliasField(28)
    offset_y: float = AliasField(29)
    dont_zoom_x: bool = AliasField(58)
    dont_zoom_y: bool = AliasField(59)
    axis: enums.TargetAxis = AliasField(101)

# Object 2903
# Class GradientTriggerObject
class GradientTrigger(TriggerObject):
    blending: enums.GradientBlending = AliasField(174)
    layer: enums.GradientLayer = AliasField(202)
    u_id: int = AliasField(203)
    bl_id: int = AliasField(203)
    d_id: int = AliasField(204)
    br_id: int = AliasField(204)
    l_id: int = AliasField(205)
    tl_id: int = AliasField(205)
    r_id: int = AliasField(206)
    tr_id: int = AliasField(206)
    vertex_mode: bool = AliasField(207)
    disable: bool = AliasField(208)
    gradient_id: int = AliasField(209)
    preview_opacity: float = AliasField(456)
    disable_all: bool = AliasField(508)

# Object 2066
class GravityTrigger(TriggerObject):
    player_1: bool = AliasField(138)
    gravity_mod: float = AliasField(148)
    player_2: bool = AliasField(200)
    player_touch: bool = AliasField(201)

# Object 3609
class InstantCollisionTrigger(TriggerObject):
    true_id: int = AliasField(51)
    false_id: int = AliasField(71)
    block_a: int = AliasField(80)
    block_b: int = AliasField(95)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    between_players: bool = AliasField(201)
    dont_reset_remap: bool = AliasField(600)

# Object 1615
# Class LabelGameObject
class ItemLabel(TriggerObject):
    item_id: int = AliasField(80)
    seconds_only: bool = AliasField(389)
    special_id: enums.ItemLabelSpecialID = AliasField(390)
    alignment: enums.ItemLabelAlignment = AliasField(391)
    time_counter: bool = AliasField(466)
    kerning: int = AliasField(488)

# Object
# Class
class ItemTrigger(TriggerObject):
    """ItemTriggerGameObject"""
    target_item_id: int = AliasField(51)
    true_id: int = AliasField(51)
    false_id: int = AliasField(71)
    item_id_1: int = AliasField(80)
    item_id: int = AliasField(80)
    item_id_2: int = AliasField(95)
    item_type_1: enums.ItemType = AliasField(476)
    item_type_2: enums.ItemType = AliasField(477)
    item_type_3: enums.ItemType = AliasField(478)
    mod: float = AliasField(479)
    mod_1: float = AliasField(479)
    item_op_1: enums.ItemOperation = AliasField(480)
    item_op_2: enums.ItemOperation = AliasField(481)
    item_op_3: enums.ItemOperation = AliasField(482)
    mod_2: float = AliasField(483)
    tolerance: float = AliasField(484)
    round_op_1: enums.ItemRoundOp = AliasField(485)
    round_op_2: enums.ItemRoundOp = AliasField(486)
    set_persistent: bool = AliasField(491)
    target_all: bool = AliasField(492)
    reset: bool = AliasField(493)
    timer: bool = AliasField(494)
    sign_op_1: enums.ItemSignOp = AliasField(578)
    sign_op_2: enums.ItemSignOp = AliasField(579)

# Object 3032
# Class KeyframeGameObject
class KeyframeObject(TriggerObject):
    duration: float = AliasField(10)
    easing: enums.Easing = AliasField(30)
    group_id: int = AliasField(51)
    spawn_id: int = AliasField(71)
    ease_rate: float = AliasField(85)
    key_id: int = AliasField(373)
    index: int = AliasField(374)
    ref_only: bool = AliasField(375)
    close_loop: bool = AliasField(376)
    prox: bool = AliasField(377)
    curve: bool = AliasField(378)
    time_mode: enums.KeyframeRefMode = AliasField(379)
    preview_art: bool = AliasField(380)
    auto_layer: bool = AliasField(459)
    line_opacity: float = AliasField(524)
    spin_direction: enums.KeyframeSpin = AliasField(536)
    full_rotations: int = AliasField(537)
    spawn_delay: float = AliasField(557)

# Object 3033
# Class KeyframeAnimTriggerObject
class AnimateKeyframeTrigger(TriggerObject):
    target_id: int = AliasField(51)
    parent_id: int = AliasField(71)
    animation_id: int = AliasField(76)
    time_mod: float = AliasField(520)
    pos_x_mod: float = AliasField(521)
    rotation_mod: float = AliasField(522)
    scale_x_mod: float = AliasField(523)
    pos_y_mod: float = AliasField(545)
    scale_y_mod: float = AliasField(546)

# Object 3662
class LinkVisibleTrigger(TriggerObject):
    group_id: int = AliasField(51)

# Object 2999
class MgEditTrigger(TriggerObject):
    duration: float = AliasField(10)
    offset_y: float = AliasField(29)
    easing: enums.Easing = AliasField(30)
    ease_rate: float = AliasField(85)

# Object 3612
class MgSpeedTrigger(TriggerObject):
    x_mod: float = AliasField(143)
    y_mod: float = AliasField(144)

# Object 901
class MoveTrigger(TriggerObject):
    duration: float = AliasField(10)
    move_x: float = AliasField(28)
    move_y: float = AliasField(29)
    easing: enums.Easing = AliasField(30)
    target_id: int = AliasField(51)
    lock_player_x: bool = AliasField(58)
    lock_player_y: bool = AliasField(59)
    target_pos: int = AliasField(71)
    ease_rate: float = AliasField(85)
    target_mode: bool = AliasField(100)
    target_axis: enums.TargetAxis = AliasField(101)
    player_1: bool = AliasField(138)
    lock_camera_x: bool = AliasField(141)
    lock_camera_y: bool = AliasField(142)
    follow_x_mod: float = AliasField(143)
    follow_y_mod: float = AliasField(144)
    player_2: bool = AliasField(200)
    use_small_step: bool = AliasField(393)
    direction_mode: bool = AliasField(394)
    target_center_id: int = AliasField(395)
    target_distance: float = AliasField(396)
    dynamic_mode: bool = AliasField(397)
    silent: bool = AliasField(544)

# Object
# Class
class ObjectControlTrigger(TriggerObject):
    """ObjectControlGameObject"""
    target_id: int = AliasField(51)

# Object
# Class
class OnDeathTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    group_id: int = AliasField(51)
    activate_group: bool = AliasField(56)

# Object
# Class
class OptionsTrigger(TriggerObject):
    """GameOptionsTrigger"""
    streak_additive: enums.Option = AliasField(159)
    unlink_dual_gravity: enums.Option = AliasField(160)
    hide_ground: enums.Option = AliasField(161)
    hide_p1: enums.Option = AliasField(162)
    hide_p2: enums.Option = AliasField(163)
    disable_p1_controls: enums.Option = AliasField(165)
    hide_mg: enums.Option = AliasField(195)
    disable_controls_p1: enums.Option = AliasField(199)
    hide_attempts: enums.Option = AliasField(532)
    edit_respawn_time: enums.Option = AliasField(573)
    respawn_time: float = AliasField(574)
    audio_on_death: enums.Option = AliasField(575)
    disable_death_sfx: enums.Option = AliasField(576)
    boost_slide: enums.Option = AliasField(593)


class Orb(TriggerObject):
    """RingObject"""
    rotation_speed: float = AliasField(97)
    disable_rotation: bool = AliasField(98)


class DashOrb(Orb):
    """DashRingObject"""
    speed: float = AliasField(586)
    collide: bool = AliasField(587)
    end_boost: float = AliasField(588)
    stop_slide: bool = AliasField(589)
    max_duration: float = AliasField(590)


class Teleportal(Orb):
    """TeleportPortalObject"""
    target_id: int = AliasField(51)
    portal_distance: float = AliasField(54)
    smooth_ease: bool = AliasField(55)
    use_force: bool = AliasField(345)
    force: float = AliasField(346)
    redirect_force: bool = AliasField(347)
    force_min: float = AliasField(348)
    force_max: float = AliasField(349)
    exit_portal_force_mod: float = AliasField(350)
    keep_offset: bool = AliasField(351)
    ignore_x: bool = AliasField(352)
    ignore_y: bool = AliasField(353)
    gravity: enums.GravityMode = AliasField(354)
    additive_force: bool = AliasField(443)
    instant_camera: bool = AliasField(464)
    snap_ground: bool = AliasField(510)
    redirect_dash: bool = AliasField(591)

# Object
# Class
class PlayerControlTrigger(TriggerObject):
    """PlayerControlGameObject"""
    m_58: bool = AliasField(58)
    m_59: bool = AliasField(59)
    player_1: bool = AliasField(138)
    m_141: bool = AliasField(141)
    player_2: bool = AliasField(200)
    stop_jump: bool = AliasField(540)
    stop_move: bool = AliasField(541)
    stop_rotation: bool = AliasField(542)
    stop_slide: bool = AliasField(543)

# Object
# Class
class PulseTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    red: int = AliasField(7)
    green: int = AliasField(8)
    blue: int = AliasField(9)
    fade_in: float = AliasField(45)
    hold: float = AliasField(46)
    fade_out: float = AliasField(47)
    color_type: enums.PulseColorType = AliasField(48)
    hsv: HSV = AliasField(49)
    copy_id: int = AliasField(50)
    target_id: int = AliasField(51)
    target_type: enums.PulseTarget = AliasField(52)
    main_only: bool = AliasField(65)
    detail_only: bool = AliasField(66)
    exclusive: bool = AliasField(86)
    disable_static_hsv: bool = AliasField(210)

# Object
# Class
class RandomTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    chance: float = AliasField(10)
    true_id: int = AliasField(51)
    false_id: int = AliasField(71)

# Object
# Class
class ResetTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    group_id: int = AliasField(51)

# Object
# Class
class RotateTrigger(TriggerObject):
    """(new, no C++ equivalent)"""
    duration: float = AliasField(10)
    easing: enums.Easing = AliasField(30)
    target_id: int = AliasField(51)
    degrees: float = AliasField(68)
    full: int = AliasField(69)
    lock_rotation: bool = AliasField(70)
    center_id: int = AliasField(71)
    ease_rate: float = AliasField(85)
    aim_mode: bool = AliasField(100)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    follow_mode: bool = AliasField(394)
    dynamic_mode: bool = AliasField(397)
    aim_target: int = AliasField(401)
    aim_offset: float = AliasField(402)
    aim_easing: int = AliasField(403)
    min_x_id: int = AliasField(516)
    min_y_id: int = AliasField(517)
    max_x_id: int = AliasField(518)
    max_y_id: int = AliasField(519)


class SFXTrigger(TriggerObject):
    """SFXTriggerGameObject"""
    duration: float = AliasField(10)
    group_id_1: int = AliasField(51)
    group_id_2: int = AliasField(71)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    sfx_id: int = AliasField(392)
    speed: int = AliasField(404)
    pitch: int = AliasField(405)
    volume: float = AliasField(406)
    use_reverb: bool = AliasField(407)
    start: int = AliasField(408)
    fade_in: int = AliasField(409)
    end: int = AliasField(410)
    fade_out: int = AliasField(411)
    fft: bool = AliasField(412)
    loop: bool = AliasField(413)
    stop_loop: bool = AliasField(414)
    unique: bool = AliasField(415)
    unique_id: int = AliasField(416)
    stop: bool = AliasField(417)
    change_volume: bool = AliasField(418)
    change_speed: bool = AliasField(419)
    override: bool = AliasField(420)
    vol_near: float = AliasField(421)
    vol_med: float = AliasField(422)
    vol_far: float = AliasField(423)
    dist_1: int = AliasField(424)
    dist_2: int = AliasField(425)
    dist_3: int = AliasField(426)
    camera: bool = AliasField(428)
    pre_load: bool = AliasField(433)
    min_int: float = AliasField(434)
    group: int = AliasField(455)
    group_id: int = AliasField(457)
    direction: enums.VolumeDirection = AliasField(458)
    ignore_volume: bool = AliasField(489)
    sfx_duration: float = AliasField(490)
    reverb: enums.ReverbPreset = AliasField(502)
    override_reverb: bool = AliasField(503)
    m_595: bool = AliasField(595)
    speed_rand: int = AliasField(596)
    pitch_rand: int = AliasField(597)
    volume_rand: float = AliasField(598)
    pitch_steps: bool = AliasField(599)


class SongTrigger(SFXTrigger):
    """SongTriggerGameObject"""
    duration: float = AliasField(10)
    group_id_1: int = AliasField(51)
    group_id_2: int = AliasField(71)
    player_1: bool = AliasField(138)
    player_2: bool = AliasField(200)
    song_id: int = AliasField(392)
    prep: bool = AliasField(399)
    load_prep: bool = AliasField(400)
    speed: int = AliasField(404)
    m_405: int = AliasField(405)
    volume: float = AliasField(406)
    m_407: bool = AliasField(407)
    start: int = AliasField(408)
    fade_in: int = AliasField(409)
    end: int = AliasField(410)
    fade_out: int = AliasField(411)
    m_412: bool = AliasField(412)
    loop: bool = AliasField(413)
    stop_loop: bool = AliasField(414)
    m_415: bool = AliasField(415)
    m_416: int = AliasField(416)
    stop: bool = AliasField(417)
    change_volume: bool = AliasField(418)
    change_speed: bool = AliasField(419)
    m_420: bool = AliasField(420)
    vol_near: float = AliasField(421)
    vol_med: float = AliasField(422)
    fol_var: float = AliasField(423)
    dist_1: int = AliasField(424)
    dist_2: int = AliasField(425)
    dist_3: int = AliasField(426)
    camera: bool = AliasField(428)
    channel: int = AliasField(432)
    m_433: bool = AliasField(433)
    m_434: float = AliasField(434)
    m_455: int = AliasField(455)
    m_457: int = AliasField(457)
    direction: enums.VolumeDirection = AliasField(458)
    m_489: bool = AliasField(489)
    m_490: float = AliasField(490)
    m_502: enums.ReverbPreset = AliasField(502)
    m_503: bool = AliasField(503)
    dont_reset: bool = AliasField(595)
    m_596: int = AliasField(596)
    m_597: int = AliasField(597)
    m_598: float = AliasField(598)
    m_599: bool = AliasField(599)

# Object
# Class
class ScaleTrigger(TriggerObject):
    """TransformTriggerGameObject"""
    duration: float = AliasField(10)
    easing: enums.Easing = AliasField(30)
    target_id: int = AliasField(51)
    center_id: int = AliasField(71)
    ease_rate: float = AliasField(85)
    only_move: bool = AliasField(133)
    scale_by_x: float = AliasField(150)
    scale_by_y: float = AliasField(151)
    div_by_x: bool = AliasField(153)
    div_by_y: bool = AliasField(154)
    relative_rotation: bool = AliasField(452)
    relative_scale: bool = AliasField(577)


class ShaderTrigger(TriggerObject):
    """ShaderGameObject"""
    fade_time: float = AliasField(10)
    easing: enums.Easing = AliasField(30)
    ease_rate: float = AliasField(85)
    shader_opt_ignore_player_particles: bool = AliasField(188)
    shader_opt_disable_all: bool = AliasField(192)
    shader_opt_layer_min: enums.GradientLayer = AliasField(196)
    shader_opt_layer_max: enums.GradientLayer = AliasField(197)
    relative: bool = AliasField(514)
    disable_preview: bool = AliasField(531)


class Bulge(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    player_1: bool = AliasField(138)
    bulge: float = AliasField(176)
    radius: float = AliasField(180)
    target: bool = AliasField(188)
    player_2: bool = AliasField(200)
    screen_offset_x: float = AliasField(290)
    screen_offset_y: float = AliasField(291)
    relative: bool = AliasField(514)


class Chromatic(ShaderTrigger):
    """(new, no C++ equivalent)"""
    target_x: float = AliasField(180)
    use_x: bool = AliasField(188)
    target_y: float = AliasField(189)
    use_y: bool = AliasField(190)
    relative: bool = AliasField(514)


class ChromaticGlitch(ShaderTrigger):
    """(new, no C++ equivalent)"""
    speed: float = AliasField(175)
    strength: float = AliasField(176)
    line_thickness: float = AliasField(179)
    rgb_offset: float = AliasField(180)
    segment_h: float = AliasField(189)
    line_strength: float = AliasField(191)
    disable: bool = AliasField(192)
    relative_pos: bool = AliasField(194)
    relative: bool = AliasField(514)


class EditColor(ShaderTrigger):
    """(new, no C++ equivalent)"""
    cb: float = AliasField(175)
    cr: float = AliasField(176)
    br: float = AliasField(179)
    bg: float = AliasField(180)
    bb: float = AliasField(189)
    cg: float = AliasField(191)


class Glitch(ShaderTrigger):
    """(new, no C++ equivalent)"""
    speed: float = AliasField(175)
    strength: float = AliasField(176)
    slice_height: float = AliasField(179)
    max_col_x_offset: float = AliasField(181)
    max_col_y_offset: float = AliasField(182)
    max_slice_x_offset: float = AliasField(191)
    relative: bool = AliasField(514)


class GrayScale(ShaderTrigger):
    """(new, no C++ equivalent)"""
    tint_channel: int = AliasField(51)
    target: float = AliasField(176)
    use_lum: bool = AliasField(188)
    use_tint: bool = AliasField(190)


class Hue(ShaderTrigger):
    """(new, no C++ equivalent)"""
    degrees: float = AliasField(176)


class InvertColor(ShaderTrigger):
    """(new, no C++ equivalent)"""
    target: float = AliasField(176)
    r: float = AliasField(179)
    g: float = AliasField(180)
    edit_rgb: bool = AliasField(188)
    b: float = AliasField(189)
    tween_rgb: bool = AliasField(190)
    clamp_rgb: bool = AliasField(194)


class LensCircle(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    tint_channel: int = AliasField(71)
    player_1: bool = AliasField(138)
    strength: float = AliasField(176)
    size: float = AliasField(179)
    fade: float = AliasField(181)
    player_2: bool = AliasField(200)
    screen_offset_x: float = AliasField(290)
    screen_offset_y: float = AliasField(291)
    relative: bool = AliasField(514)


class MotionBlur(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    ref_channel: int = AliasField(71)
    player_1: bool = AliasField(138)
    intensity: float = AliasField(176)
    target_x: float = AliasField(180)
    fade: float = AliasField(181)
    use_x: bool = AliasField(188)
    target_y: float = AliasField(189)
    use_y: bool = AliasField(190)
    follow_ease: float = AliasField(191)
    dual_dir: bool = AliasField(194)
    player_2: bool = AliasField(200)
    center: bool = AliasField(201)
    relative: bool = AliasField(514)
    empty_only: bool = AliasField(515)


class Pinch(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    player_1: bool = AliasField(138)
    modifier: float = AliasField(179)
    target_x: float = AliasField(180)
    target: bool = AliasField(188)
    use_x: bool = AliasField(190)
    use_y: bool = AliasField(194)
    player_2: bool = AliasField(200)
    screen_offset_x: float = AliasField(290)
    screen_offset_y: float = AliasField(291)
    radius: float = AliasField(512)


class Pixelate(ShaderTrigger):
    """(new, no C++ equivalent)"""
    target_x: float = AliasField(180)
    use_x: bool = AliasField(188)
    target_y: float = AliasField(189)
    use_y: bool = AliasField(190)
    snap_grid: bool = AliasField(194)
    relative: bool = AliasField(514)
    hard_edges: bool = AliasField(515)


class RadialBlur(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    ref_channel: int = AliasField(71)
    player_1: bool = AliasField(138)
    intensity: float = AliasField(176)
    size: float = AliasField(179)
    fade: float = AliasField(181)
    target: bool = AliasField(188)
    player_2: bool = AliasField(200)
    screen_offset_x: float = AliasField(290)
    screen_offset_y: float = AliasField(291)
    empty_only: bool = AliasField(515)


class Sepia(ShaderTrigger):
    """(new, no C++ equivalent)"""
    target: float = AliasField(176)


class ShockLine(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    player_1: bool = AliasField(138)
    speed: float = AliasField(175)
    strength: float = AliasField(176)
    time_offset: float = AliasField(177)
    wave_width: float = AliasField(179)
    thickness: float = AliasField(180)
    fade_in: float = AliasField(181)
    fade_out: float = AliasField(182)
    invert: bool = AliasField(184)
    flip: bool = AliasField(185)
    rotate: bool = AliasField(186)
    dual: bool = AliasField(187)
    target: bool = AliasField(188)
    follow: bool = AliasField(190)
    player_2: bool = AliasField(200)
    screen_offset: float = AliasField(290)
    max_size: float = AliasField(512)
    animate: bool = AliasField(513)
    relative: bool = AliasField(514)


class Shockwave(ShaderTrigger):
    """(new, no C++ equivalent)"""
    center_id: int = AliasField(51)
    player_1: bool = AliasField(138)
    speed: float = AliasField(175)
    strength: float = AliasField(176)
    time_offset: float = AliasField(177)
    wave_width: float = AliasField(179)
    thickness: float = AliasField(180)
    fade_in: float = AliasField(181)
    fade_out: float = AliasField(182)
    inner: float = AliasField(183)
    invert: bool = AliasField(184)
    target: bool = AliasField(188)
    follow: bool = AliasField(190)
    outer: float = AliasField(191)
    player_2: bool = AliasField(200)
    screen_offset_x: float = AliasField(290)
    screen_offset_y: float = AliasField(291)
    max_size: float = AliasField(512)
    animate: bool = AliasField(513)
    relative: bool = AliasField(514)


class SplitScreen(ShaderTrigger):
    """(new, no C++ equivalent)"""
    target_x: float = AliasField(180)
    use_x: bool = AliasField(188)
    target_y: float = AliasField(189)
    use_y: bool = AliasField(190)

# Object 1520
class ShakeTrigger(TriggerObject):
    duration: float = AliasField(10)
    strength: float = AliasField(75)
    interval: float = AliasField(84)

# Object 3608
# Class SpawnParticleTrigger
class SpawnParticleTrigger(TriggerObject):
    particle_group: int = AliasField(51)
    position_group: int = AliasField(71)
    offset_x: float = AliasField(547)
    offset_y: float = AliasField(548)
    offvar_x: float = AliasField(549)
    offvar_y: float = AliasField(550)
    match_rot: bool = AliasField(551)
    rotation: float = AliasField(552)
    rotation_rand: float = AliasField(553)
    scale: float = AliasField(554)
    scale_rand: float = AliasField(555)

# Object 1268
# Class SpawnTrigger
class SpawnTrigger(TriggerObject):
    group_id: int = AliasField(51)
    delay: float = AliasField(63)
    disable_preview: bool = AliasField(102)
    ordered: bool = AliasField(441)
    remaps: RemapList = AliasField(442)
    delay_rand: float = AliasField(556)
    reset_remap: bool = AliasField(581)

# Object 31
# Class StartPosObject
class StartPosition(TriggerObject):
    target_order: int = AliasField('kA19')
    reverse_mode: bool = AliasField('kA20')
    disable: bool = AliasField('kA21')
    target_channel: int = AliasField('kA26')
    mirror_mode: bool = AliasField('kA28')
    rotate_mode: bool = AliasField('kA29')
    reset_camera: bool = AliasField('kA35')
    mini_mode = None
    dual_mode = None
    flip_gravity = None
    speed = None
    gamemode = None


# Object 3640
class StateBlock(TriggerObject):
    state_on: int = AliasField(51)
    state_off: int = AliasField(71)

# Object 1612
# Class TriggerControlGameObject
class StopTrigger(TriggerObject):
    target_id: int = AliasField(51)
    use_control_id: bool = AliasField(535)
    mode: enums.StopMode = AliasField(580)

# Object 3614
# Class TimerTriggerGameObject
class TimerTrigger(TriggerObject):
    target_id: int = AliasField(51)
    item_id: int = AliasField(80)
    start_time: float = AliasField(467)
    dont_override: bool = AliasField(468)
    ignore_timewarp: bool = AliasField(469)
    mod: float = AliasField(470)
    start_paused: bool = AliasField(471)
    control_stop: enums.TimeControlType = AliasField(472)
    stop_time: float = AliasField(473)
    target_time: float = AliasField(473)
    stop: bool = AliasField(474)
    multi_activate: bool = AliasField(475)

# Object 3643
class ToggleBlock(TriggerObject):
    group_id: int = AliasField(51)
    activate_group: bool = AliasField(56)
    claim_touch: bool = AliasField(445)
    spawn_only: bool = AliasField(504)

# Object 1049
class ToggleTrigger(TriggerObject):
    group_id: int = AliasField(51)
    activate_group: bool = AliasField(56)

# Object 1595
class TouchTrigger(TriggerObject):
    group_id: int = AliasField(51)
    hold_mode: bool = AliasField(81)
    toggle_mode: enums.TouchMode = AliasField(82)
    dual_mode: bool = AliasField(89)
    only_player: enums.TargetPlayer = AliasField(198)

# Object 3613
# Class UISettingsGameObject
class UITrigger(TriggerObject):
    group_id: int = AliasField(51)
    ui_target: int = AliasField(71)
    ref_x: enums.UIRef = AliasField(385)
    ref_y: enums.UIRef = AliasField(386)
    relative_x: bool = AliasField(387)
    relative_y: bool = AliasField(388)

# Class SmartGameObject
class Template(BaseObject):
    reference_only: bool = AliasField(157)

# Object 914
# Class TextGameObject
class Text(BaseObject):
    data: str = AliasField(31)
    kerning: int = AliasField(488)