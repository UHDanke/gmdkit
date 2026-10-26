# Package Imports
from enum import IntEnum, IntFlag


class EnumClass(IntEnum):
    
    @classmethod
    def _missing_name(cls, value:int) -> str:
        return f"UNKNOWN_{'N' if value<0 else ''}{abs(value)}"

    @classmethod
    def from_string(cls, string: str):
        return cls(int(string))

    @classmethod
    def _missing_(cls, value):
        try:
            v = int(value)
        except (TypeError, ValueError):
            return None
        member = cls._value2member_map_.get(v)
        if member is None:
            name = cls._missing_name(v)
            if name is None: return None
            member = int.__new__(cls, v)
            member._name_ = name
            member._value_ = v
            cls._value2member_map_[v] = member
        return member

class FlagClass(IntFlag):

    @classmethod
    def from_string(cls, string: str):
        return cls(int(string))

class ObjectID(IntEnum):
    LEVEL_SETTINGS = 0
    PORTAL_GRAVITY_NORMAL = 10
    PORTAL_GRAVITY_INVERTED = 11
    PORTAL_CUBE = 12
    PORTAL_SHIP = 13
    ENTER_PRESET_FADE_ONLY = 22
    ENTER_PRESET_FADE_BOTTOM = 23
    ENTER_PRESET_FADE_TOP = 24
    ENTER_PRESET_FADE_LEFT = 25
    ENTER_PRESET_FADE_RIGHT = 26
    ENTER_PRESET_SCALE_UP = 27
    ENTER_PRESET_SCALE_DOWN = 28
    START_POSITION = 31
    TRIGGER_ENABLE_PLAYER_TRAIL = 32
    TRIGGER_DISABLE_PLAYER_TRIAL = 33
    PAD_YELLOW = 35
    ORB_YELLOW = 36
    PORTAL_MIRROR_ENTER = 45
    PORTAL_MIRROR_EXIT = 46
    PORTAL_BALL = 47
    ENTER_PRESET_CHAOTIC = 55
    ENTER_PRESET_HALF_LEFT = 56
    ENTER_PRESET_HALF_RIGHT = 57
    ENTER_PRESET_HALF = 58
    ENTER_PRESET_HALF_INVERT = 59
    PAD_BLUE = 67
    ORB_BLUE = 84
    PORTAL_SIZE_NORMAL = 99
    PORTAL_SIZE_SMALL = 101
    PORTAL_UFO = 111
    PAD_PINK = 140
    ORB_PINK = 141
    COLLECTIBLE_SECRET_COIN = 142
    PORTAL_SPEED_SLOW = 200
    PORTAL_SPEED_NORMAL = 201
    PORTAL_SPEED_FAST = 202
    PORTAL_SPEED_VERY_FAST = 203
    PORTAL_DUAL_ENTER = 286
    PORTAL_DUAL_EXIT = 287
    PORTAL_WAVE = 660
    PORTAL_ROBOT = 745
    PORTAL_LINKED_TELEPORT = 747
    TRIGGER_COLOR = 899
    TRIGGER_MOVE = 901
    OBJECT_TEXT = 914
    TRIGGER_PULSE = 1006
    TRIGGER_ALPHA = 1007
    ORB_GREEN = 1022
    TRIGGER_TOGGLE = 1049
    TRIGGER_SPAWN = 1268
    COLLECTIBLE_KEY = 1275
    COLLECTIBLE_USER_COIN = 1329
    ORB_BLACK = 1330
    PORTAL_SPIDER = 1331
    PAD_RED = 1332
    ORB_RED = 1333
    PORTAL_SPEED_SUPER_FAST = 1334
    TRIGGER_ROTATE = 1346
    TRIGGER_FOLLOW = 1347
    TRIGGER_SHAKE = 1520
    TRIGGER_ANIMATE = 1585
    ORB_TOGGLE = 1594
    TRIGGER_TOUCH = 1595
    TRIGGER_COUNT = 1611
    TRIGGER_PLAYER_HIDE = 1612
    TRIGGER_PLAYER_SHOW = 1613
    COLLECTIBLE_SMALL_COIN = 1614
    OBJECT_ITEM_LABEL = 1615
    TRIGGER_STOP = 1616
    ORB_DASH_GREEN = 1704
    ORB_DASH_PINK = 1751
    MODIFIER_WAVE_COLLISION = 1755
    TRIGGER_INSTANT_COUNT = 1811
    TRIGGER_ON_DEATH = 1812
    MODIFIER_STOP_JUMP = 1813
    TRIGGER_FOLLOW_PLAYER_Y = 1814
    TRIGGER_COLLISION = 1815
    OBJECT_COLLISION_BLOCK = 1816
    TRIGGER_PICKUP = 1817
    TRIGGER_BG_EFFECT_ENABLE = 1818
    TRIGGER_BG_EFFECT_DISABLE = 1819
    MODIFIER_STOP_DASH = 1829
    MODIFIER_HEAD_COLLISION = 1859
    TRIGGER_RANDOM = 1912
    TRIGGER_ZOOM_CAMERA = 1913
    TRIGGER_STATIC_CAMERA = 1914
    ENTER_PRESET_NO_FADE = 1915
    TRIGGER_OFFSET_CAMERA = 1916
    TRIGGER_REVERSE = 1917
    TRIGGER_END_WALL = 1931
    TRIGGER_PLAYER_CONTROL = 1932
    PORTAL_SWING = 1933
    TRIGGER_SONG = 1934
    TRIGGER_TIMEWARP = 1935
    TRIGGER_ROTATE_CAMERA = 2015
    TRIGGER_CAMERA_GUIDE = 2016
    TRIGGER_CAMERA_EDGE = 2062
    TRIGGER_CHECKPOINT = 2063
    PORTAL_EXIT_TELEPORT = 2064
    OBJECT_PARTICLE = 2065
    TRIGGER_GRAVITY = 2066
    TRIGGER_SCALE = 2067
    TRIGGER_ADV_RANDOM = 2068
    OBJECT_FORCE_BLOCK = 2069
    MODIFIER_FLIP_GRAVITY = 2866
    TRIGGER_OPTIONS = 2899
    TRIGGER_GP_ARROW = 2900
    TRIGGER_GAMEPLAY_OFFSET = 2901
    PORTAL_ENTER_TELEPORT = 2902
    TRIGGER_GRADIENT = 2903
    SHADER_OPTIONS = 2904
    SHADER_SHOCKWAVE = 2905
    SHADER_SHOCKLINE = 2907
    SHADER_GLITCH = 2909
    SHADER_CHROMATIC = 2910
    SHADER_CHROMATIC_GLITCH = 2911
    SHADER_PIXELATE = 2912
    SHADER_LENS_CIRCLE = 2913
    SHADER_RADIAL_BLUR = 2914
    SHADER_MOTION_BLUR = 2915
    SHADER_BULGE = 2916
    SHADER_PINCH = 2917
    SHADER_GRAY_SCALE = 2919
    SHADER_SEPIA = 2920
    SHADER_INVERT_COLOR = 2921
    SHADER_HUE = 2922
    SHADER_EDIT_COLOR = 2923
    TRIGGER_SPLIT_SCREEN = 2924
    TRIGGER_CAMERA_MODE = 2925
    PORTAL_GRAVITY_TOGGLE = 2926
    TRIGGER_EDIT_MG = 2999
    ORB_SPIDER = 3004
    PAD_SPIDER = 3005
    TRIGGER_AREA_MOVE = 3006
    TRIGGER_AREA_ROTATE = 3007
    TRIGGER_AREA_SCALE = 3008
    TRIGGER_AREA_FADE = 3009
    TRIGGER_AREA_TINT = 3010
    TRIGGER_EDIT_AREA_MOVE = 3011
    TRIGGER_EDIT_AREA_ROTATE = 3012
    TRIGGER_EDIT_AREA_SCALE = 3013
    TRIGGER_EDIT_AREA_FADE = 3014
    TRIGGER_EDIT_AREA_TINT = 3015
    TRIGGER_ADV_FOLLOW = 3016
    TRIGGER_ENTER_MOVE = 3017
    TRIGGER_ENTER_ROTATE = 3018
    TRIGGER_ENTER_SCALE = 3019
    TRIGGER_ENTER_FADE = 3020
    TRIGGER_ENTER_TINT = 3021
    TRIGGER_TELEPORT = 3022
    TRIGGER_STOP_ENTER = 3023
    TRIGGER_AREA_STOP = 3024
    ORB_TELEPORT = 3027
    TRIGGER_CHANGE_BG = 3029
    TRIGGER_CHANGE_GR = 3030
    TRIGGER_CHANGE_MG = 3031
    TRIGGER_KEYFRAME = 3032
    TRIGGER_ANIMATE_KEYFRAME = 3033
    TRIGGER_END = 3600
    TRIGGER_SFX = 3602
    TRIGGER_EDIT_SFX = 3603
    TRIGGER_EVENT = 3604
    TRIGGER_EDIT_SONG = 3605
    TRIGGER_BG_SPEED = 3606
    TRIGGER_SEQUENCE = 3607
    TRIGGER_SPAWN_PARTICLE = 3608
    TRIGGER_INSTANT_COLLISION = 3609
    TRIGGER_MG_SPEED = 3612
    TRIGGER_UI = 3613
    TRIGGER_TIMER = 3614
    TRIGGER_TIMER_EVENT = 3615
    TRIGGER_TIMER_CONTROL = 3617
    TRIGGER_RESET = 3618
    TRIGGER_ITEM_EDIT = 3619
    TRIGGER_ITEM_COMPARE = 3620
    OBJECT_STATE_BLOCK = 3640
    TRIGGER_ITEM_PERSIST = 3641
    BPM_GUIDE = 3642
    OBJECT_TOGGLE_BLOCK = 3643
    OBJECT_FORCE_CIRCLE_BLOCK = 3645
    TRIGGER_OBJECT_CONTROL = 3655
    TRIGGER_EDIT_ADV_FOLLOW = 3660
    TRIGGER_RETARGET_ADV_FOLLOW = 3661
    TRIGGER_LINK_VISIBLE = 3662
    
class OldColor(EnumClass):
    DEFAULT = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    COLOR_1 = 3
    COLOR_2 = 4
    LIGHT_BG = 5
    COLOR_3 = 6
    COLOR_4 = 7
    LINE_3D = 8
    
class ColorID(EnumClass):
    DEFAULT = 0
    BACKGROUND = 1000
    GROUND = 1001
    LINE = 1002
    LINE_3D = 1003
    OBJECT = 1004
    PLAYER_1 = 1005
    PLAYER_2 = 1006
    LIGHT_BG = 1007
    GROUND_2 = 1009
    BLACK = 1010
    WHITE = 1011
    LIGHTER = 1012
    MIDDLEGROUND = 1013
    MIDDLEGROUND_2 = 1014
    
    @classmethod
    def _missing_name(cls, value:int) -> str:
        if 0<=value<=999:
            p = "CUSTOM"
        elif 1000<=value<1101:
            p = "NA"
        else:
            p = "UNKNOWN"
        return f"{p}_{'N' if value<0 else ''}{abs(value)}"
    
    @property
    def is_editable(self):
        cls = type(self)
        ids = {
            cls.BLACK, 
            cls.WHITE, 
            cls.LIGHTER, 
            cls.LIGHT_BG, 
            cls.PLAYER_1, 
            cls.PLAYER_2
            }
        return self not in ids
    
    @property
    def is_custom(self):
        return 1<=self<=999
    
    @property
    def is_special(self):
        cls = type(self)
        ids = {
             cls.GROUND, 
             cls.LINE, 
             cls.LINE_3D, 
             cls.OBJECT, 
             cls.GROUND_2, 
             cls.MIDDLEGROUND, 
             cls.MIDDLEGROUND_2
            }
        return self not in ids
    
    @property
    def is_na(self):
        return self.name.startswith("NA")

class SingleColorMode(EnumClass):
    DEFAULT = 0
    BASE = 1
    DETAIL = 2

class ZLayer(EnumClass):
    B5 = -5
    B4 = -3
    B3 = -1
    DEFAULT = 0
    B2 = 1
    B1 = 3
    PORTAL_BACK = 4
    T1 = 5
    T2 = 7
    T3 = 9
    T4 = 11

class Easing(EnumClass):
    NONE = 0
    EASE_IN_OUT = 1
    EASE_IN = 2
    EASE_OUT = 3
    ELASTIC_IN_OUT = 4
    ELASTIC_IN = 5
    ELASTIC_OUT = 6
    BOUNCE_IN_OUT = 7
    BOUNCE_IN = 8
    BOUNCE_OUT = 9
    EXPONENTIAL_IN_OUT = 10
    EXPONENTIAL_IN = 11
    EXPONENTIAL_OUT = 12
    SINE_IN_OUT = 13
    SINE_IN = 14
    SINE_OUT = 15
    BACK_IN_OUT = 16
    BACK_IN = 17
    BACK_OUT = 18

class ItemLabelAlignment(EnumClass):
    CENTER = 0
    LEFT = 1
    RIGHT = 2

class ItemLabelSpecialID(EnumClass):
    NONE = 0
    MAINTIME = -1
    POINTS = -2
    ATTEMPTS = -3

class UIRef(EnumClass):
    DEFAULT = 0
    AUTO_X = 1
    CENTER_X = 2
    LEFT = 3
    RIGHT = 4
    AUTO_Y = 5
    CENTER_Y = 6
    BOTTOM = 7
    TOP = 8

class TouchMode(EnumClass):
    TOGGLE = 0
    ON = 1
    OFF = 2

class TargetPlayer(EnumClass):
    NONE = -1
    ALL = 0
    P1 = 1
    P2 = 2

class GravityMode(EnumClass):
    NONE = 0
    NORMAL = 1
    FLIPPED = 2
    TOGGLE = 3

class StopMode(EnumClass):
    STOP = 0
    PAUSE = 1
    RESUME = 2

class TargetAxis(EnumClass):
    NONE = 0
    X = 1
    Y = 2

class VolumeDirection(EnumClass):
    CIRCULAR = 0
    HORIZONTAL = 1
    LEFT = 2
    RIGHT = 3
    VERTICAL = 4
    DOWN = 5
    UP = 6

class ReverbPreset(EnumClass):
    GENERIC = 0
    PADDED_CELL = 1
    ROOM = 2
    BATH_ROOM = 3
    LIVING_ROOM = 4
    STONE_ROOM = 5
    AUDITORIUM = 6
    CONCERT_HALL = 7
    CAVE = 8
    ARENA = 9
    HANGAR = 10
    STONE_CORRIDOR = 11
    ALLEY = 12
    FOREST = 13
    CITY = 14
    MOUNTAINS = 15
    QUARRY = 16
    PLAIN = 17
    PARKING_LOT = 18
    SEWER_PIPE = 19
    UNDER_WATER = 20

class SequenceMode(EnumClass):
    STOP = 0
    LOOP = 1
    LAST = 2

class PulseTarget(EnumClass):
    CHANNEL = 0
    GROUP = 1

class PickupMode(EnumClass):
    ADD = 0
    MULTIPLY = 1
    DIVIDE = 2

class Option(EnumClass):
    DISABLE = -1
    IGNORE = 0
    ENABLE = 1

class KeyframeSpin(EnumClass):
    NONE = 0
    CW = 1
    CCW = 2

class KeyframeRefMode(EnumClass):
    TIME = 0
    EVEN = 1
    DIST = 2

class ItemOperation(EnumClass):
    EQUAL = 0
    ADD_GT = 1
    SUBTRACT_GE = 2
    MULTIPLY_LT = 3
    DIVIDE_LE = 4
    NOT_EQUAL = 5

class ItemType(EnumClass):
    DEFAULT = 0
    ITEM = 1
    TIMER = 2
    POINTS = 3
    MAINTIME = 4
    ATTEMPTS = 5

class ItemRoundOp(EnumClass):
    NONE = 0
    ROUND = 1
    FLOOR = 2
    CEILING = 3

class ItemSignOp(EnumClass):
    NONE = 0
    ABSOLUTE = 1
    NEGATIVE = 2

class InstantCountMode(EnumClass):
    EQUAL = 0
    LARGER = 1
    SMALLER = 2

class GradientBlending(EnumClass):
    NORMAL = 0
    ADDITIVE = 1
    MULTIPLY = 2
    INVERT = 3

class GradientLayer(EnumClass):
    BG = 1
    MG = 2
    B5 = 3
    B4 = 4
    B3 = 5
    B2 = 6
    B1 = 7
    P = 8
    T1 = 9
    T2 = 10
    T3 = 11
    T4 = 12
    G = 13
    UI = 14
    MAX = 15

class EnterMode(EnumClass):
    NONE = 0
    ENTER = 1
    EXIT = 2

class EffectSpecialCenter(EnumClass):
    NONE = 0
    P1 = -1
    P2 = -2
    C = -3
    BL = -4
    CL = -5
    TL = -6
    BC = -7
    TC = -8
    BR = -9
    CR = -10
    TR = -11

class CameraEdge(EnumClass):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class ArrowDir(EnumClass):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def flip(self):
        cls = type(self)
        opposites = {
            cls.UP: cls.DOWN,
            cls.DOWN: cls.UP,
            cls.LEFT: cls.RIGHT,
            cls.RIGHT: cls.LEFT,
        }
        return opposites.get(self, cls.NONE)

class AdvFollowInit(EnumClass):
    INIT = 0
    SET = 1
    ADD = 2

class AdvFollowMode(EnumClass):
    MODE_1 = 0
    MODE_2 = 1
    MODE_3 = 2

class GameEvents(EnumClass):
    TINY_LANDING = 1
    FEATHER_LANDING = 2
    SOFT_LANDING = 3
    NORMAL_LANDING = 4
    HARD_LANDING = 5
    HIT_HEAD = 6
    ORB_TOUCHED = 7
    ORB_ACTIVATED = 8
    PAD_ACTIVATED = 9
    GRAVITY_INVERTED = 10
    GRAVITY_RESTORED = 11
    NORMAL_JUMP = 12
    ROBOT_BOOST_START = 13
    ROBOT_BOOST_STOP = 14
    UFO_JUMP = 15
    SHIP_BOOST_START = 16
    SHIP_BOOST_END = 17
    SPIDER_TELEPORT = 18
    BALL_SWITCH = 19
    SWING_SWITCH = 20
    WAVE_PUSH = 21
    WAVE_RELEASE = 22
    DASH_START = 23
    DASH_STOP = 24
    TELEPORTED = 25
    PORTAL_NORMAL = 26
    PORTAL_SHIP = 27
    PORTAL_BALL = 28
    PORTAL_UFO = 29
    PORTAL_WAVE = 30
    PORTAL_ROBOT = 31
    PORTAL_SPIDER = 32
    PORTAL_SWING = 33
    YELLOW_ORB = 34
    PINK_ORB = 35
    RED_ORB = 36
    GRAVITY_ORB = 37
    GREEN_ORB = 38
    DROP_ORB = 39
    CUSTOM_ORB = 40
    DASH_ORB = 41
    GRAVITY_DASH_ORB = 42
    SPIDER_ORB = 43
    TELEPORT_ORB = 44
    YELLOW_PAD = 45
    PINK_PAD = 46
    RED_PAD = 47
    GRAVITY_PAD = 48
    SPIDER_PAD = 49
    PORTAL_GRAVITY_FLIP = 50
    PORTAL_GRAVITY_NORMAL = 51
    PORTAL_GRAVITY_INVERT = 52
    PORTAL_FLIP = 53
    PORTAL_UNFLIP = 54
    PORTAL_NORMAL_SCALE = 55
    PORTAL_MINI_SCALE = 56
    PORTAL_DUAL_ON = 57
    PORTAL_DUAL_OFF = 58
    PORTAL_TELEPORT = 59
    CHECKPOINT = 60
    DESTROY_BLOCK = 61
    USER_COIN = 62
    PICKUP_ITEM = 63
    CHECKPOINT_RESPAWN = 64
    FALL_LOW = 65
    FALL_MED = 66
    FALL_HIGH = 67
    FALL_VHIGH = 68
    JUMP_PUSH = 69
    JUMP_RELEASE = 70
    LEFT_PUSH = 71
    LEFT_RELEASE = 72
    RIGHT_PUSH = 73
    RIGHT_RELEASE = 74
    PLAYER_REVERSED =  75
    FALL_SPEED_LOW = 76
    FALL_SPEED_MED = 77
    FALL_SPEED_HIGH = 78

class BigBeastAnim(EnumClass):
    BITE = 0
    ATTACK01 = 1
    ATTACK01_END = 2
    IDLE01 = 3

class BatAnim(EnumClass):
    IDLE01 = 0
    IDLE02 = 1
    IDLE03 = 2
    ATTACK01 = 3
    ATTACK02 = 4
    ATTACK02_END = 5
    SLEEP = 6
    SLEEP_LOOP = 7
    SLEEP_END = 8
    ATTACK02_LOOP = 9

class SpikeBallAnim(EnumClass):
    IDLE01 = 0
    IDLE02 = 1
    TOATTACK01 = 2
    ATTACK01 = 3
    ATTACK02 = 4
    TOATTACK03 = 5
    ATTACK03 = 6
    IDLE03 = 7
    FROMATTACK03 = 8

class Gamemode(EnumClass):
    CUBE = 0
    SHIP = 1
    BALL = 2
    UFO = 3
    WAVE = 4
    ROBOT = 5
    SPIDER = 6
    SWING = 7

class Speed(EnumClass):
    NORMAL = 0
    SLOW = 1
    FAST = 2
    VERY_FAST = 3
    SUPER_FAST = 4

class LevelDifficulty(EnumClass):
    NA = -1
    AUTO = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5
    HARD_DEMON = 6
    EASY_DEMON = 7
    MEDIUM_DEMON = 8
    INSANE_DEMON = 9
    EXTREME_DEMON = 10

class ListDifficulty(EnumClass):
    NA = -1
    AUTO = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDER = 4
    INSANE = 5
    EASY_DEMON = 6
    MEDIUM_DEMON = 7
    HARD_DEMON = 8
    INSANE_DEMON = 9
    EXTREME_DEMON = 10

class LevelLength(EnumClass):
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4
    PLAT = 5

class OfficialSongs(EnumClass):
    STAY_INSIDE_ME = -1
    STEREO_MADNESS = 0
    BACK_ON_TRACK = 1
    POLARGEIST = 2
    DRY_OUT = 3
    BASE_AFTER_BASE = 4
    CANT_LET_GO = 5
    JUMPER = 6
    TIME_MACHINE = 7
    CYCLES = 8
    XSTEP = 9
    CLUTTERFUNK = 10
    THEORY_OF_EVERYTHING = 11
    ELECTROMAN_ADVENTURES = 12
    CLUBSTEP = 13
    ELECTRODYNAMIX = 14
    HEXAGON_FORCE = 15
    BLAST_PROCESSING = 16
    THEORY_OF_EVERYTHING_2 = 17
    GEOMETRICAL_DOMINATOR = 18
    DEADLOCKED = 19
    FINGERDASH = 20
    DASH = 21
    EXPLORERS = 22
    THE_SEVEN_SEAS = 23
    VIKING_ARENA = 24
    AIRBORNE_ROBOTS = 25
    SECRET = 26
    PAYLOAD = 27
    BEAST_MODE = 28
    MACHINA = 29
    YEARS = 30
    FRONTLINES = 31
    SPACE_PIRATES = 32
    STRIKER = 33
    EMBERS = 34
    ROUND_1 = 35
    MONSTER_DANCE_OFF = 36
    PRESS_START = 37
    NOCK_EM = 38
    POWER_TRIP = 39

class EpicRating(EnumClass):
    NONE = 0
    EPIC = 1
    LEGENDARY = 2
    MYTHIC = 3

class FeatureRating(EnumClass):
    UNRATED = 0
    RATED = 1
    FEATURED = 2
    EPIC = 3
    LEGENDARY = 4
    MYTHIC = 5

class DemonRating(EnumClass):
    HARD = 0
    UNKNOWN = 1
    EASY = 3
    MEDIUM = 4
    INSANE = 5
    EXTREME = 6

class LevelType(EnumClass):
    OFFICIAL = 1
    LOCAL = 2
    SAVED = 3
    ONLINE = 4

class TimelyType(EnumClass):
    NONE = 0
    DAILY = 1
    WEEKLY = 2
    EVENT = 3

class LevelRating(EnumClass):
    NONE = 0
    EASY = 10
    NORMAL = 20
    HARD = 30
    HARDER = 40
    INSANE = 50

class ReplayEventID(EnumClass):
    JUMP_P1 = 0 
    LEFT_P1 = 2
    RIGHT_P1 = 3
    BUTTON_4_P1 = 4
    BUTTON_5_P1 = 5
    JUMP_P2 = 6
    LEFT_P2 = 7
    RIGHT_P2 = 8
    BUTTON_4_P2 = 9
    BUTTON_5_P2 = 10
    CHECKPOINT_ADD = 98
    CHECKPOINT = 99  

class ToggleCBS(EnumClass):
    DEFAULT = 0
    ON = 1
    OFF = 2

class SequenceResetType(EnumClass):
    RESET_FULL = 0
    RESET_STEP = 1

class TimeControlType(EnumClass):
    START = 0
    STOP = 1

class PulseColorType(EnumClass):
    COLOR = 0
    HSV = 1

class TextureQuality(EnumClass):
    AUTO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Resolution(EnumClass):
    AUTO = 0
    R640X480 = 1
    R720X480 = 2
    R720X576 = 3
    R800X600 = 4
    R1024X768 = 5
    R1152X864 = 6
    R1176X664 = 7
    R1280X720 = 8
    R1280X768 = 9
    R1280X800 = 10
    R1280X960 = 11
    R1280X1024 = 12
    R1360X768 = 13
    R1366X768 = 14
    R1440X900 = 15
    R1600X900 = 16
    R1600X1024 = 17
    R1600X1200 = 18
    R1680X1050 = 19
    R1768X992 = 20
    R1920X1080 = 21
    R1920X1200 = 22
    R1920X1440 = 23
    R2048X1536 = 24
    R2560X1440 = 25
    R2560X1600 = 26
    R3840X2160 = 27

class ModStatus(EnumClass):
    NONE = 0
    RATE_ADVISOR = 1
    MODERATOR = 2

class DisplayIcon(EnumClass):
    CUBE = 0
    SHIP = 1
    BALL = 2
    UFO = 3
    WAVE = 4
    ROBOT = 5
    SPIDER = 6
    SWING = 7
    JETPACK = 8


class EditorWindow(EnumClass):
    EMOTE_PICKER_KEYBOARD = 0
    EDITOR_COMMANDS = 1
    EMOTE_PICKER = 2
    FIND_OBJECT = 3
    GRID_SETTINGS = 4
    MOVE_STEP = 5

    
class NamedGroupsType(EnumClass):
    GROUP_ID = 1
    ITEM_ID = 2
    COLLISION_ID = 3
    TIMER_ID = 4
    EFFECT_ID = 5
    CONTROL_ID = 6
    GRADIENT_ID = 7
    ENTER_CHANNEL = 8

class ControlSource(EnumClass):
    CREATOR = 0
    CUSTOM = 1

class ControlType(FlagClass):
    NONE = 0
    KEYBOARD = 1
    TOUCH = 2
    CONTROLLER = 4

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
    
class SpecialRewardItem(EnumClass):
    FIRE_SHARD = 1
    ICE_SHARD = 2
    POISON_SHARD = 3
    SHADOW_SHARD = 4
    LAVA_SHARD = 5
    DEMON_KEY = 6
    ORBS = 7
    DIAMONDS = 8
    CUSTOM_ITEM = 9
    EARTH_SHARD = 10
    BLOOD_SHARD = 11
    METAL_SHARD = 12
    LIGHT_SHARD = 13
    SOUL_SHARD = 14
    GOLD_KEY = 15

class RewardType(EnumClass):
    UNKNOWN = 0
    SMALL = 1
    LARGE = 2
    SMALL_TREASURE = 3
    LARGE_TREASURE = 4
    KEY_10_TREASURE = 5
    KEY_25_TREASURE = 6
    KEY_50_TREASURE = 7
    KEY_100_TREASURE = 8

class UnlockType(EnumClass):
    NONE = 0
    CUBE = 1
    COLOR_1 = 2
    COLOR_2 = 3
    SHIP = 4
    BALL = 5
    UFO = 6
    WAVE = 7
    ROBOT = 8
    SPIDER = 9
    STREAK = 10
    DEATH = 11
    ITEM = 12
    SWING = 13
    JETPACK = 14
    SHIP_FIRE = 15

class ChallengeType(EnumClass):
    UNKNOWN = 0
    ORBS = 1
    USER_COINS = 2
    STARS = 3
    MOONS = 4

class LikeItemType(EnumClass):
    LEVEL = 1
    LEVEL_COMMENT = 2   
    ACCOUNT_COMMENT = 3 
    LIST = 4      
    SOUND_PACK = 5   
    SOUND_PACK_COMMENT = 6 
    MOD_ROOM_LEVEL_COMMENT = 7 
    MOD_ROOM_USER_COMMENT = 8 
    
class LinkType(EnumClass):
    YOUTUBE = 1
    NEWGROUNDS = 2
    SOUNDCLOUD = 3
    SPOTIFY = 4
    BANDCAMP = 5
    NCS = 6
    WEBSITE = 7
    INSTAGRAM = 8
    TWITTER = 9
    FACEBOOK = 10
    TWITCH = 11
    DISCORD = 12
    TIKTOK = 13
    ITCH_IO = 14

class GameObjectType(EnumClass):
    SOLID = 0
    HAZARD = 2
    INVERSE_GRAVITY_PORTAL = 3
    NORMAL_GRAVITY_PORTAL = 4
    SHIP_PORTAL = 5
    CUBE_PORTAL = 6
    DECORATION = 7
    YELLOW_JUMP_PAD = 8
    PINK_JUMP_PAD = 9
    GRAVITY_PAD = 10
    YELLOW_JUMP_RING = 11
    PINK_JUMP_RING = 12
    GRAVITY_RING = 13
    INVERSE_MIRROR_PORTAL = 14
    NORMAL_MIRROR_PORTAL = 15
    BALL_PORTAL = 16
    REGULAR_SIZE_PORTAL = 17
    MINI_SIZE_PORTAL = 18
    UFO_PORTAL = 19
    MODIFIER = 20
    BREAKABLE = 21
    SECRET_COIN = 22
    DUAL_PORTAL = 23
    SOLO_PORTAL = 24
    SLOPE = 25
    WAVE_PORTAL = 26
    ROBOT_PORTAL = 27
    TELEPORT_PORTAL = 28
    GREEN_RING = 29
    COLLECTIBLE = 30
    USER_COIN = 31
    DROP_RING = 32
    SPIDER_PORTAL = 33
    RED_JUMP_PAD = 34
    RED_JUMP_RING = 35
    CUSTOM_RING = 36
    DASH_RING = 37
    GRAVITY_DASH_RING = 38
    COLLISION_OBJECT = 39
    SPECIAL = 40
    SWING_PORTAL = 41
    GRAVITY_TOGGLE_PORTAL = 42
    SPIDER_ORB = 43
    SPIDER_PAD = 44
    ENTER_EFFECT_OBJECT = 45
    TELEPORT_ORB = 46
    ANIMATED_HAZARD = 47
    
    def collision_type(self) -> "CollisionType":
        T = GameObjectType
        match self:
            case T.SOLID:
                return CollisionType.SOLID
            case T.BREAKABLE:
                return CollisionType.BREAKABLE
            case T.SLOPE:
                return CollisionType.SLOPE
            case T.HAZARD | T.ANIMATED_HAZARD:
                return CollisionType.HAZARD
            case T.MODIFIER | T.ENTER_EFFECT_OBJECT:
                return CollisionType.TRIGGER
            case T.SPECIAL:
                return CollisionType.SPECIAL
            case (T.YELLOW_JUMP_PAD | T.PINK_JUMP_PAD | T.GRAVITY_PAD | T.RED_JUMP_PAD
                  | T.SPIDER_PAD):
                return CollisionType.PAD
            case (T.YELLOW_JUMP_RING | T.PINK_JUMP_RING | T.GRAVITY_RING | T.GREEN_RING
                  | T.DROP_RING | T.RED_JUMP_RING | T.CUSTOM_RING | T.DASH_RING
                  | T.GRAVITY_DASH_RING | T.SPIDER_ORB | T.TELEPORT_ORB):
                return CollisionType.ORB
            case (T.INVERSE_GRAVITY_PORTAL | T.NORMAL_GRAVITY_PORTAL | T.SHIP_PORTAL
                  | T.CUBE_PORTAL | T.INVERSE_MIRROR_PORTAL | T.NORMAL_MIRROR_PORTAL
                  | T.BALL_PORTAL | T.REGULAR_SIZE_PORTAL | T.MINI_SIZE_PORTAL | T.UFO_PORTAL
                  | T.DUAL_PORTAL | T.SOLO_PORTAL | T.WAVE_PORTAL | T.ROBOT_PORTAL
                  | T.TELEPORT_PORTAL | T.SPIDER_PORTAL | T.SWING_PORTAL
                  | T.GRAVITY_TOGGLE_PORTAL):
                return CollisionType.PORTAL
            case T.SECRET_COIN | T.USER_COIN | T.COLLECTIBLE:
                return CollisionType.COLLECTIBLE
            case _:
                return CollisionType.NONE


class ObjectPropertyFlag(FlagClass):
    IS_TRIGGER = 1 << 0
    CAN_BE_CONTROLLED = 1 << 1
    IS_START_POS = 1 << 2
    IS_INVISIBLE = 1 << 3
    INTRINSIC_DONT_FADE = 1 << 4
    SOLID_COLOR_BLOCK = 1 << 5
    INVISIBLE_BLOCK = 1 << 6
    SLOPE_IS_HAZARD = 1 << 7
    USE_OBJECT_RECT = 1 << 8
    USES_AUDIO_SCALE = 1 << 9
    FIXED_Z_LAYER = 1 << 10
    NOT_COLORABLE = 1 << 11
    SPAWNABLE = 1 << 12
    
class CollisionType(EnumClass):
    NONE = 0
    SOLID = 1
    PASSABLE = 2
    BREAKABLE = 3
    SLOPE = 4
    HAZARD = 5
    PAD = 6
    ORB = 7
    PORTAL = 8
    TRIGGER = 9
    COLLECTIBLE = 10
    SPECIAL = 11