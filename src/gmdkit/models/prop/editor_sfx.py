# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils.enums import EnumClass
from gmdkit.serialization.mixins import (
    ArrayDecoderMixin, DataclassDecoderMixin, DelimiterMixin, DictDecoderMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.classes import FieldMetaclass, DictField
from gmdkit.serialization.type_cast import to_bool, from_bool, from_float, serialize
from gmdkit.models.custom_sfx import CustomSFXMappingList


class EditorSFXAction(EnumClass):
    PLACE_ANY = 100
    DELETE_ONE = 101
    DELETE_MANY = 102
    DUPLICATE = 103
    PICKUP_OBJECT = 104
    DROP_OBJECT = 105
    DROP_OBJECT_SNAPPED = 106
    EDIT_OBJECT = 107
    EDIT_GROUP = 108
    EDIT_SPECIAL = 109
    COPY = 110
    PASTE = 111
    COPY_VALUES = 112
    PASTE_STATE = 113
    PASTE_COLOR = 114
    DESELECT_ALL = 120
    SELECT_OBJECT = 121
    SELECT_RECT = 122
    ROTATE = 130
    ROTATE_SNAP = 131
    FLIP = 132
    MOVE_ANY = 150
    MOVE_TINY = 151
    MOVE_NORMAL = 152
    MOVE_BIG = 153
    MOVE_SMALL = 155
    ZOOM_IN = 160
    ZOOM_OUT = 161
    SAVE_POSITION = 162
    LOAD_POSITION = 163
    BUILD_TAB_SWITCH = 164
    MODE_ANY = 169
    MODE_CREATE = 170
    MODE_EDIT = 171
    MODE_DELETE = 172
    MODE_VIEW = 173
    UNDO = 180
    REDO = 181
    TOGGLE_SETTING_ANY = 189
    TOGGLE_SNAP = 190
    TOGGLE_FREE_MOVE = 191
    TOGGLE_SWIPE = 192
    TOGGLE_ROTATE = 193
    TOGGLE_UI = 194
    TOGGLE_PREVIEW_MODE = 195
    TOGGLE_HITBOXES = 196
    TOGGLE_HIDE_INVISIBLE = 197
    TOGGLE_PARTICLE_ICONS = 198
    INCREASE_GRID_SIZE = 200
    DECREASE_GRID_SIZE = 201
    TOGGLE_GRID_ON = 202
    TOGGLE_GRID_OFF = 203
    GRID_SIZE_PLUS_1 = 204
    GRID_SIZE_MINUS_1 = 205
    PLAYTEST_START = 210
    PLAYTEST_STOP = 211
    OPEN_SETTINGS = 220
    OPEN_PAUSE_MENU = 221
    SAVE_LEVEL = 222
    RESUME = 223
    EXIT_EDITOR = 224
    AUTO_SAVE = 225
    AUTO_BACKUP = 226
    PLACE_TRIGGER = 250
    PLACE_PARTICLE = 251
    PLACE_TEXT = 252
    PLACE_ANIMATED = 253
    PLACE_SPINNING = 254
    PLACE_SPIN_HAZARD = 255
    PLACE_HAZARD = 256
    PLACE_PORTAL = 257
    PLACE_ORB = 258
    PLACE_PAD = 259
    PLACE_INTERACTIVE = 260
    PLACE_SLOPE = 261
    PLACE_SOLID = 262
    PLACE_DECORATION = 263
    PLACE_MONSTER = 264
    PLACE_SPEED_PORTAL = 265
    DEATH_MARKER_ANY = 266
    DEATH_MARKER_LOCAL = 267
    DEATH_MARKER_GLOBAL = 268
    TOGGLE_LDM = 269
    DEATH_MARKER_LABEL_GLOBAL = 270
    DEATH_MARKER_LABEL_STAR = 271
    DEATH_MARKER_LABEL_LOCAL = 272
    DEATH_MARKER_LABEL_FIRE = 273
    HOLD_SWIPE = 274
    ANCHOR_SNAP = 275
    MOVE_CUSTOM = 276
    SELECT_BUILD_OBJECT = 277
    BUILD_PAGE_SWITCH = 278


class EditorSFXPlayMode(EnumClass):
    RANDOM = 0
    IN_ORDER = 1


class EditorSFXSound(DictDecoderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    SEPARATOR = ","
    KEY_DECODER = int
    KEY_ENCODER = str
    DEFAULT_DECODER = None
    DEFAULT_ENCODER = staticmethod(serialize)

    sfx_id: int = DictField(key=1, decoder=int, default=0)                                          # 392
    volume: float = DictField(key=2, decoder=float, encoder=from_float, default=1.0)                # 406
    speed: int = DictField(key=3, decoder=int, default=0)                                           # 404
    pitch: int = DictField(key=4, decoder=int, default=0)                                           # 405
    start: int = DictField(key=5, decoder=int, default=0)                                           # 408
    end: int = DictField(key=6, decoder=int, default=0)                                             # 410
    fade_in: int = DictField(key=7, decoder=int, default=0)                                         # 409
    fade_out: int = DictField(key=8, decoder=int, default=0)                                        # 411
    min_interval: float = DictField(key=9, decoder=float, encoder=from_float, default=0.0)          # 434
    speed_rand: int = DictField(key=10, decoder=int, default=0)                                     # 596
    pitch_rand: int = DictField(key=11, decoder=int, default=0)                                     # 597
    volume_rand: float = DictField(key=12, decoder=float, encoder=from_float, default=0.0)          # 598
    pitch_steps: bool = DictField(key=13, decoder=to_bool, encoder=from_bool, default=False)        # 599
    fft: bool = DictField(key=14, decoder=to_bool, encoder=from_bool, default=False)                # 412
    custom_library_id: int = DictField(key=15, decoder=int, default=0)                              # 601
    use_reverb: bool = DictField(key=16, decoder=to_bool, encoder=from_bool, default=False)         # 407


class EditorSFXSoundList(ArrayDecoderMixin, ListClass[EditorSFXSound]):

    __slots__ = ()

    SEPARATOR = ":"
    DECODER = EditorSFXSound.from_string
    ENCODER = EditorSFXSound.to_string


class EditorSFXBinding(DictDecoderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    SEPARATOR = ","
    KEY_DECODER = int
    KEY_ENCODER = str
    DEFAULT_DECODER = None
    DEFAULT_ENCODER = staticmethod(serialize)

    action: EditorSFXAction = DictField(
        key=1, decoder=EditorSFXAction.from_string, default=EditorSFXAction.PLACE_ANY
        )
    play_mode: EditorSFXPlayMode = DictField(
        key=2, decoder=EditorSFXPlayMode.from_string, default=EditorSFXPlayMode.RANDOM
        )
    min_interval: float = DictField(key=3, decoder=float, encoder=from_float, default=0.0)
    

@dataclass_decoder(slots=True, from_array=True, separator=";")
class EditorSFXSoundBinding(DataclassDecoderMixin):
    binding: EditorSFXBinding = field_decoder(decoder=EditorSFXBinding.from_string,encoder=EditorSFXBinding.to_string,default_factory=EditorSFXBinding)
    sounds: EditorSFXSoundList = field_decoder(
        decoder=EditorSFXSoundList.from_string,
        encoder=EditorSFXSoundList.to_string,
        default_factory=EditorSFXSoundList,
        )

class EditorSFXSoundBindingList(DelimiterMixin, ArrayDecoderMixin, ListClass[EditorSFXBinding]):
    __slots__ = ()

    SEPARATOR = ";"
    END_DELIMITER = ";"
    GROUP_SIZE = 2
    DECODER = EditorSFXSoundBinding.from_tokens
    ENCODER = EditorSFXSoundBinding.to_tokens

    def get_action(self, action: int):
        for b in self:
            if b.binding.action == action:
                return b
        return None


@dataclass_decoder(slots=True, from_array=True, separator="M|")
class EditorSFXBindingMapping(DataclassDecoderMixin):

    bindings: EditorSFXSoundBindingList = field_decoder(
        default_factory=EditorSFXSoundBindingList,
        decoder=EditorSFXSoundBindingList.from_string, encoder=EditorSFXSoundBindingList.to_string
        )
    mappings: CustomSFXMappingList = field_decoder(
        default_factory=CustomSFXMappingList,
        decoder=CustomSFXMappingList.from_string, encoder=CustomSFXMappingList.to_string,
        optional=True
        )


@dataclass_decoder(slots=True, from_array=True, separator=";",max_split=1)
class EditorSFXString(DataclassDecoderMixin):

    version: int = 1
    sfx_data: EditorSFXBindingMapping = field_decoder(
        default_factory=EditorSFXBindingMapping, 
        decoder=EditorSFXBindingMapping.from_string, 
        encoder=EditorSFXBindingMapping.to_string
        )