# Package Imports
from gmdkit.serialization.types import EnumClass


class OldColor(EnumClass):
    PLAYER_1 = 1
    PLAYER_2 = 2
    COLOR_1 = 3
    COLOR_2 = 4
    LIGHT_BG = 5
    COLOR_3 = 6
    COLOR_4 = 7
    LINE_3D = 8


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
    
     
class ColorPlayer(EnumClass):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


class ItemLabelAlignment(EnumClass):
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    
class ItemLabelSpecialID(EnumClass):
    MAINTIME = -1
    POINTS = -2
    ATTEMPTS = -3
    

class UIRefX(EnumClass):
    AUTO = 1
    CENTER = 2
    LEFT = 3
    RIGHT = 4
    
class UIRefY(EnumClass):
    AUTO = 1
    CENTER = 2
    BOTTOM = 3
    TOP = 4

class TouchMode(EnumClass):
    FLIP = 0
    ON = 1
    OFF = 2
    
class SelectPlayer(EnumClass):
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


class SelectAxis(EnumClass):
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
    
class ReverbPresets(EnumClass):
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

class KeyframeSpinDir(EnumClass):
    NONE = 0
    CW = 1
    CCW = 2
    
class KeyframeRefMode(EnumClass):
    TIME = 0
    EVEN = 1
    DIST = 2

class ItemOperation(EnumClass):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4

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
    
class Edge(EnumClass):
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
    
    
class LevelDifficulty(EnumClass):    
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