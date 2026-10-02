# Package Imports
from gmdkit.utils import enums
from gmdkit.mappings import color_id
from gmdkit.serialization.classes import AliasField, BaseInterface
from gmdkit.casting.object_loader import FieldLoaderMixin
from gmdkit.models.prop.groups import IDList
from gmdkit.models.prop.guideline import GuidelineList
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.prop.color import Color, ColorList

Field = AliasField
register_id = FieldLoaderMixin.register_id


class LevelSettings(BaseInterface):
    audio_track: enums.OfficialSongs = Field("kA1")
    gamemode: enums.Gamemode = Field("kA2")
    mini_mode: bool = Field("kA3")
    speed: enums.Speed = Field("kA4")
    object_2_blending: bool = Field("kA5")
    background: int = Field("kA6")
    ground: int = Field("kA7")
    dual_mode: bool = Field("kA8")
    is_start_pos: bool = Field("kA9")
    input_2p: bool = Field("kA10")
    flip_gravity: bool = Field("kA11")
    color_3_blending: bool = Field("kA12")
    song_offset: float = Field("kA13")
    song_guidelines: GuidelineList = Field("kA14")
    song_fade_in: bool = Field("kA15")
    song_fade_out: bool = Field("kA16")
    ground_line: int = Field("kA17")
    font: int = Field("kA18")
    reverse_mode: bool = Field("kA20")
    platformer_mode: bool = Field("kA22")
    middleground: int = Field("kA25")
    allow_multi_rotate: bool = Field("kA27")
    mirror_mode: bool = Field("kA28")
    rotate_mode: bool = Field("kA29")
    enable_player_squeeze: bool = Field("kA31")
    fix_gravity_bug: bool = Field("kA32")
    fix_negative_scale: bool = Field("kA33")
    fix_robot_jump: bool = Field("kA34")
    player_spawn: int = Field("kA36")
    dynamic_height: bool = Field("kA37")
    sort_groups: bool = Field("kA38")
    fix_radius_collision: bool = Field("kA39")
    enable_2_2_changes: bool = Field("kA40")
    allow_static_object_rotate: bool = Field("kA41")
    reverse_sync: bool = Field("kA42")
    disable_time_point_penalty: bool = Field("kA43")
    decrease_boost_slide: bool = Field("kA45")
    song_dont_reset: bool = Field("kA46")
    group_offset: int = Field("kA47")
    enable_impulse_fix: bool = Field("kA48")
 
    # pre 1.9 legacy colors
    background_red: int = Field("kS1")
    background_green: int = Field("kS2")
    background_blue: int = Field("kS3")
    ground_red: int = Field("kS4")
    ground_green: int = Field("kS5")
    ground_blue: int = Field("kS6")
    groundline_red: int = Field("kS7")
    groundline_green: int = Field("kS8")
    groundline_blue: int = Field("kS9")
    object_red: int = Field("kS10")
    object_green: int = Field("kS11")
    object_blue: int = Field("kS12")
    object_2_red: int = Field("kS13")
    object_2_green: int = Field("kS14")
    object_2_blue: int = Field("kS15")
    background_player_color: int = Field("kS16")
    ground_player_color: int = Field("kS17")
    groundline_player_color: int = Field("kS18")
    object_player_color: int = Field("kS19")
    object_2_player_color: int = Field("kS20")
 
    # 1.9 legacy colors
    background_color: Color = Field("kS29")
    ground_color: Color = Field("kS30")
    line_color: Color = Field("kS31")
    object_color: Color = Field("kS32")
    color_1: Color = Field("kS33")
    color_2: Color = Field("kS34")
    color_3: Color = Field("kS35")
    color_4: Color = Field("kS36")
    line_3d_color: Color = Field("kS37")
 
    # colors
    colors: ColorList = Field("kS38")
    color_page: int = Field("kS39")


class BaseObject(BaseInterface):
    obj_id: int = Field(1)
    x: float = Field(2)
    y: float = Field(3)
    flip_x: bool = Field(4)
    flip_y: bool = Field(5)
    rotation: float = Field(6)
    editor_l1: int = Field(20)
    color_1: int = Field(21)
    color_2: int = Field(22)
    z_layer: int = Field(24)
    z_order: int = Field(25)
    group_parent: bool = Field(34)
    hsv_enabled_1: bool = Field(41)
    hsv_enabled_2: bool = Field(42)
    hsv_1: HSV = Field(43)
    hsv_2: HSV = Field(44)
    groups: IDList = Field(57)
    editor_l2: int = Field(61)
    dont_fade: bool = Field(64)
    dont_enter: bool = Field(67)
    no_glow: bool = Field(96)
    high_detail: bool = Field(103)
    linked_group: int = Field(108)
    no_effects: bool = Field(116)
    no_touch: bool = Field(121)
    scale_x: float = Field(128)
    scale_y: float = Field(129)
    skew_x: float = Field(131)
    skew_y: float = Field(132)
    passable: bool = Field(134)
    hide: bool = Field(135)
    nonstick_x: bool = Field(136)
    ice_block: bool = Field(137)
    color_1_index: int = Field(155)
    color_2_index: int = Field(156)
    grip_slope: bool = Field(193)
    parent_groups: IDList = Field(274)
    area_parent: bool = Field(279)
    nonstick_y: bool = Field(289)
    enter_channel: int = Field(343)
    scale_stick: bool = Field(356)
    no_audio_scale: bool = Field(372)
    material: int = Field(446)
    extra_sticky: bool = Field(495)
    dont_boost_y: bool = Field(496)
    single_color_type: enums.SingleColorMode = Field(497)
    no_particle: bool = Field(507)
    dont_boost_x: bool = Field(509)
    extended_collision: bool = Field(511)
    
    @property
    def scale(self) -> float:
        return min(self.scale_x, self.scale_y)

    @scale.setter
    def scale(self, value:float):
        current = self.scale
        if current == 0:
            self.scale_x = self.scale_y = value
            return
        factor = value / current
        self.scale_x *= factor
        self.scale_y *= factor
        
    def clear_transforms(self):
        del self.rotation
        del self.scale_x
        del self.scale_y
        del self.skew_x
        del self.skew_y
        
    def clear_position(self):
        del self.x
        del self.y

    def clear_color(self):
        del self.color_1
        del self.color_2
        del self.color_1_index
        del self.color_2_index
        
    def fix_transform(self):
        if self.scale_x < -1:
            self.scale_x *= -1
            
            if self.flip_x:
                del self.flip_x
            else:
                self.flip_x = not self.flip_x
                
        if self.scale_y < -1:
            self.scale_y *= -1
            
            if self.flip_y:
                del self.flip_y
            else:
                self.flip_y = not self.flip_y
        
        self.skew_x %= 360
        self.skew_y %= 360
        self.rotation %= 360
        
        if self.skew_x == self.skew_y:
            self.rotation += self.skew_x
            self.rotation %= 360
            self.skew_x = self.skew_y =  0
        
        elif self.rotation > 0:
            self.skew_x += self.rotation
            self.skew_y += self.rotation
            self.skew_x %= 360
            self.skew_y %= 360
            self.rotation = 0
        
        if self.skew_x == self.skew_y == 0:
            del self.skew_x
            del self.skew_y
            
        if self.rotation == 0:
            del self.rotation
            
    def fix_groups(self):
        # clean duplicates
        groups = set(self.groups)
        parents = set(self.parent_groups)
        groups = sorted(groups)[:10] # limit groups
        parents &= groups # clean phantom groups
        self.groups[:] = groups
        self.parent_groups[:] = sorted(parents)[:10]
        
    def fix_color(self):
        if self.color_1 == color_id.LIGHTER:
            self.color_1 = color_id.WHITE


class EffectObject(BaseObject):
    editor_preview: bool = Field(13)
    interactible: bool = Field(36)
    order: int = Field(115)
    channel: int = Field(170)
    single_ptouch: bool = Field(284)
    center_effect: bool = Field(369)
    control_id: int = Field(534)


class TriggerObject(EffectObject):
    touch_trigger: bool = Field(11)
    spawn_trigger: bool = Field(62)
    multi_trigger: bool = Field(87)
    multi_activate: bool = Field(99)
    ignore_gparent: bool = Field(280)
    ignore_linked: bool = Field(281)
    
    
    def set_timed_trigger(self):
        self.spawn_trigger = False
        self.touch_trigger = False
        self.multi_trigger = False
        
    def set_spawn_trigger(self, multi_trigger:bool=False):
        self.spawn_trigger = True
        self.touch_trigger = False
        self.multi_trigger = multi_trigger
        
    def set_touch_trigger(self, multi_trigger:bool=False):
        self.spawn_trigger = False
        self.touch_trigger = True
        self.multi_trigger = multi_trigger   


# LevelSettings
FieldLoaderMixin.register_id(None,LevelSettings)
FieldLoaderMixin.register_id(0,LevelSettings)

# BaseObject
FieldLoaderMixin.DEFAULT_SCHEMA = BaseObject
