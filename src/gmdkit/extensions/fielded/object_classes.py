# Package Imports
from gmdkit.utils.classes import DictField
from gmdkit.utils import enums
from gmdkit.models.object import Object
from gmdkit.models.prop.groups import IDList
from gmdkit.models.prop.events import EventList
from gmdkit.models.prop.sequence import SequenceList
from gmdkit.models.prop.random import RandomWeightsList
from gmdkit.models.prop.remaps import RemapList
from gmdkit.models.prop.guideline import GuidelineList
from gmdkit.models.prop.hsv import HSV
from gmdkit.models.prop.particle import Particle
from gmdkit.models.prop.color import Color, ColorList


class FieldedObject(Object):
    READONLY_KEYS = frozenset({1})

    def __setitem__(self, key, value):
        if key in self.READONLY_KEYS and key in self:
            raise TypeError(
                f"Key {key!r} is read-only and cannot be modified after initialisation."
            )
        super().__setitem__(key, value)

    def __setattr__(self, name, value):
        cls = type(self)
        for c in cls.__mro__:
            if name in c.__dict__:
                object.__setattr__(self, name, value)
                return
        raise AttributeError(
            f"{cls.__name__!r} has no field {name!r}."
        )

    id: int = DictField[int](1)
    x: float = DictField[float](2)
    y: float = DictField[float](3)
    flip_x: bool = DictField[bool](4)
    flip_y: bool = DictField[bool](5)
    rotation: float = DictField[float](6)
    old_color_id: enums.OldColor = DictField[enums.OldColor](19)
    editor_l1: int = DictField[int](20)
    color_1: int = DictField[int](21)
    color_2: int = DictField[int](22)
    z_layer: int = DictField[int](24)
    z_order: int = DictField[int](25)
    old_scale: float = DictField[float](32)
    group_parent: bool = DictField[bool](34)
    hsv_enabled_1: bool = DictField[bool](41)
    hsv_enabled_2: bool = DictField[bool](42)
    hsv_1: HSV = DictField[HSV](43)
    hsv_2: HSV = DictField[HSV](44)
    groups: IDList = DictField[IDList](57)
    editor_l2: int = DictField[int](61)
    dont_fade: bool = DictField[bool](64)
    dont_enter: bool = DictField[bool](67)
    no_glow: bool = DictField[bool](96)
    high_detail: bool = DictField[bool](103)
    linked_group: int = DictField[int](108)
    no_effects: bool = DictField[bool](116)
    no_touch: bool = DictField[bool](121)
    scale_x: float = DictField[float](128)
    scale_y: float = DictField[float](129)
    skew_x: float = DictField[float](131)
    skew_y: float = DictField[float](132)
    passable: bool = DictField[bool](134)
    hide: bool = DictField[bool](135)
    nonstick_x: bool = DictField[bool](136)
    ice_block: bool = DictField[bool](137)
    color_1_index: int = DictField[int](155)
    color_2_index: int = DictField[int](156)
    grip_slope: bool = DictField[bool](193)
    target_player_2: bool = DictField[bool](200)
    parent_groups: IDList = DictField[IDList](274)
    area_parent: bool = DictField[bool](279)
    nonstick_y: bool = DictField[bool](289)
    enter_channel: int = DictField[int](343)
    scale_stick: bool = DictField[bool](356)
    disable_grid_snap: bool = DictField[bool](370)
    no_audio_scale: bool = DictField[bool](372)
    material: int = DictField[int](446)
    extra_sticky: bool = DictField[bool](495)
    dont_boost_y: bool = DictField[bool](496)
    single_color_type: enums.SingleColorMode = DictField[enums.SingleColorMode](497)
    no_particle: bool = DictField[bool](507)
    dont_boost_x: bool = DictField[bool](509)
    extended_collision: bool = DictField[bool](511)


class Animated(FieldedObject):
    randomize_start: bool = DictField[bool](106)
    animation_speed: float = DictField[float](107)
    use_speed: bool = DictField[bool](122)
    animate_on_trigger: bool = DictField[bool](123)
    delayed_loop: bool = DictField[bool](126)
    animate_active_only: bool = DictField[bool](214)
    single_frame: int = DictField[int](462)
    offset_anim: bool = DictField[bool](592)


class AnimatedExplosion(Animated):
    disable_shine: bool = DictField[bool](127)


class ItemLabel(FieldedObject):
    item_id: int = DictField[int](80)
    seconds_only: bool = DictField[bool](389)
    special_id: enums.ItemLabelSpecialID = DictField[enums.ItemLabelSpecialID](390)
    alignment: enums.ItemLabelAlignment = DictField[enums.ItemLabelAlignment](391)
    time_counter: bool = DictField[bool](466)
    kerning: int = DictField[int](488)


class Level(FieldedObject):
    audio_track: int = DictField[int]('kA1')
    gamemode: enums.Gamemode = DictField[enums.Gamemode]('kA2')
    mini_mode: bool = DictField[bool]('kA3')
    speed: enums.Speed = DictField[enums.Speed]('kA4')
    object_2_blending: bool = DictField[bool]('kA5')
    background: int = DictField[int]('kA6')
    ground: int = DictField[int]('kA7')
    dual_mode: bool = DictField[bool]('kA8')
    is_start_pos: bool = DictField[bool]('kA9')
    input_2p: bool = DictField[bool]('kA10')
    flip_gravity: bool = DictField[bool]('kA11')
    color_3_blending: bool = DictField[bool]('kA12')
    song_offset: float = DictField[float]('kA13')
    song_guidelines: GuidelineList = DictField[GuidelineList]('kA14')
    song_fade_in: bool = DictField[bool]('kA15')
    song_fade_out: bool = DictField[bool]('kA16')
    ground_line: int = DictField[int]('kA17')
    font: int = DictField[int]('kA18')
    reverse_mode: bool = DictField[bool]('kA20')
    platformer_mode: bool = DictField[bool]('kA22')
    middleground: int = DictField[int]('kA25')
    allow_multi_rotate: bool = DictField[bool]('kA27')
    mirror_mode: bool = DictField[bool]('kA28')
    rotate_mode: bool = DictField[bool]('kA29')
    enable_player_squeeze: bool = DictField[bool]('kA31')
    fix_gravity_bug: bool = DictField[bool]('kA32')
    fix_negative_scale: bool = DictField[bool]('kA33')
    fix_robot_jump: bool = DictField[bool]('kA34')
    player_spawn: int = DictField[int]('kA36')
    dynamic_height: bool = DictField[bool]('kA37')
    sort_groups: bool = DictField[bool]('kA38')
    fix_radius_collision: bool = DictField[bool]('kA39')
    enable_2_2_changes: bool = DictField[bool]('kA40')
    allow_static_object_rotate: bool = DictField[bool]('kA41')
    reverse_sync: bool = DictField[bool]('kA42')
    disable_time_point_penalty: bool = DictField[bool]('kA43')
    decrease_boost_slide: bool = DictField[bool]('kA45')
    song_dont_reset: bool = DictField[bool]('kA46')
    colors: ColorList = DictField[ColorList]('kS38')
    color_page: int = DictField[int]('kS39')


class LevelColor17(Level):
    red: int = DictField[int]('kS1')
    green: int = DictField[int]('kS2')
    blue: int = DictField[int]('kS3')
    player_color: enums.TargetPlayer = DictField[enums.TargetPlayer]('kS16')


class LevelColor17Background(LevelColor17):
    pass


class LevelColor17Ground(LevelColor17):
    pass


class LevelColor17Line(LevelColor17):
    pass


class LevelColor17Object(LevelColor17):
    pass


class LevelColor17Object2(LevelColor17):
    pass


class LevelColor19(Level):
    background: Color = DictField[Color]('kS29')
    ground: Color = DictField[Color]('kS30')
    line: Color = DictField[Color]('kS31')
    object: Color = DictField[Color]('kS32')
    color_1: Color = DictField[Color]('kS33')
    color_2: Color = DictField[Color]('kS34')
    color_3: Color = DictField[Color]('kS35')
    color_4: Color = DictField[Color]('kS36')
    line_3d: Color = DictField[Color]('kS37')


class Particle(FieldedObject):
    data: Particle = DictField[Particle](145)
    use_obj_color: bool = DictField[bool](146)
    uniform_obj_color: bool = DictField[bool](147)
    quick_start: bool = DictField[bool](211)


class Saw(FieldedObject):
    rotation_speed: float = DictField[float](97)
    disable_rotation: bool = DictField[bool](98)


class StartPos(FieldedObject):
    target_order: int = DictField[int]('kA19')
    reverse_mode: bool = DictField[bool]('kA20')
    disable: bool = DictField[bool]('kA21')
    platformer_mode: bool = DictField[bool]('kA22')
    target_channel: int = DictField[int]('kA26')
    allow_multi_rotate: bool = DictField[bool]('kA27')
    mirror_mode: bool = DictField[bool]('kA28')
    rotate_mode: bool = DictField[bool]('kA29')
    enable_player_squeeze: bool = DictField[bool]('kA31')
    fix_gravity_bug: bool = DictField[bool]('kA32')
    fix_negative_scale: bool = DictField[bool]('kA33')
    fix_robot_jump: bool = DictField[bool]('kA34')
    reset_camera: bool = DictField[bool]('kA35')
    dynamic_height: bool = DictField[bool]('kA37')
    sort_groups: bool = DictField[bool]('kA38')
    fix_radius_collision: bool = DictField[bool]('kA39')
    enable_2_2_changes: bool = DictField[bool]('kA40')
    allow_static_object_rotate: bool = DictField[bool]('kA41')
    reverse_sync: bool = DictField[bool]('kA42')
    disable_time_point_penalty: bool = DictField[bool]('kA43')
    decrease_boost_slide: bool = DictField[bool]('kA45')
    song_dont_reset: bool = DictField[bool]('kA46')


class Template(FieldedObject):
    reference_only: bool = DictField[bool](157)


class Text(FieldedObject):
    data: str = DictField[str](31)
    kerning: int = DictField[int](488)


class Timewarp(FieldedObject):
    mod: float = DictField[float](120)


class Trigger(FieldedObject):
    touch_trigger: bool = DictField[bool](11)
    editor_preview: bool = DictField[bool](13)
    interactible: bool = DictField[bool](36)
    spawn_trigger: bool = DictField[bool](62)
    multi_trigger: bool = DictField[bool](87)
    multi_activate: bool = DictField[bool](99)
    order: int = DictField[int](115)
    reverse: bool = DictField[bool](117)
    channel: int = DictField[int](170)
    ignore_gparent: bool = DictField[bool](280)
    ignore_linked: bool = DictField[bool](281)
    single_ptouch: bool = DictField[bool](284)
    center_effect: bool = DictField[bool](369)
    disable_multi_activate: bool = DictField[bool](444)
    control_id: int = DictField[int](534)


class TriggerAdvFollow(Trigger):
    target_id: int = DictField[int](51)
    follow_id: int = DictField[int](71)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    corner: bool = DictField[bool](201)
    delay: float = DictField[float](292)
    delay_rand: float = DictField[float](293)
    max_speed: float = DictField[float](298)
    max_speed_rand: float = DictField[float](299)
    start_speed: float = DictField[float](300)
    start_speed_rand: float = DictField[float](301)
    target_dir: bool = DictField[bool](305)
    x_only: bool = DictField[bool](306)
    y_only: bool = DictField[bool](307)
    max_range: float = DictField[float](308)
    max_range_rand: float = DictField[float](309)
    steer: float = DictField[float](316)
    steer_rand: float = DictField[float](317)
    steer_low: float = DictField[float](318)
    steer_low_rand: float = DictField[float](319)
    steer_high: float = DictField[float](320)
    steer_high_rand: float = DictField[float](321)
    speed_range_low: float = DictField[float](322)
    speed_range_low_rand: float = DictField[float](323)
    speed_range_high: float = DictField[float](324)
    speed_range_high_rand: float = DictField[float](325)
    break_force: float = DictField[float](326)
    break_force_rand: float = DictField[float](327)
    break_angle: float = DictField[float](328)
    break_angle_rand: float = DictField[float](329)
    break_steer: float = DictField[float](330)
    break_steer_rand: float = DictField[float](331)
    break_steer_speed_limit: float = DictField[float](332)
    break_steer_speed_limit_rand: float = DictField[float](333)
    acceleration: float = DictField[float](334)
    acceleration_rand: float = DictField[float](335)
    ignore_disabled: bool = DictField[bool](336)
    steer_low_check: bool = DictField[bool](337)
    steer_high_check: bool = DictField[bool](338)
    rotate_dir: bool = DictField[bool](339)
    rot_offset: float = DictField[float](340)
    near_accel: float = DictField[float](357)
    near_accel_rand: float = DictField[float](358)
    near_dist: float = DictField[float](359)
    near_dist_rand: float = DictField[float](360)
    easing: float = DictField[float](361)
    easing_rand: float = DictField[float](362)
    rot_easing: float = DictField[float](363)
    rot_deadzone: float = DictField[float](364)
    priority: int = DictField[int](365)
    max_range_ref: int = DictField[int](366)
    mode: enums.AdvFollowMode = DictField[enums.AdvFollowMode](367)
    friction: float = DictField[float](558)
    friction_rand: float = DictField[float](559)
    start_speed_ref: int = DictField[int](560)
    near_friction: float = DictField[float](561)
    near_friction_rand: float = DictField[float](562)
    start_dir: float = DictField[float](563)
    start_dir_rand: float = DictField[float](564)
    start_dir_ref: int = DictField[int](565)
    exclusive: bool = DictField[bool](571)
    init: enums.AdvFollowInit = DictField[enums.AdvFollowInit](572)


class TriggerAdvRandom(Trigger):
    targets: RandomWeightsList = DictField[RandomWeightsList](152)


class TriggerAlpha(Trigger):
    duration: float = DictField[float](10)
    opacity: float = DictField[float](35)
    group_id: int = DictField[int](51)


class TriggerAnimate(Trigger):
    target_id: int = DictField[int](51)
    animation_id: int = DictField[int](76)


class TriggerAnimateKeyframe(Trigger):
    target_id: int = DictField[int](51)
    parent_id: int = DictField[int](71)
    animation_id: int = DictField[int](76)
    time_mod: float = DictField[float](520)
    pos_x_mod: float = DictField[float](521)
    rotation_mod: float = DictField[float](522)
    scale_x_mod: float = DictField[float](523)
    pos_y_mod: float = DictField[float](545)
    scale_y_mod: float = DictField[float](546)


class TriggerArrow(Trigger):
    dir_y_neg: enums.ArrowDir = DictField[enums.ArrowDir](166)
    dir_x_pos: enums.ArrowDir = DictField[enums.ArrowDir](167)
    edit_velocity: bool = DictField[bool](169)
    change_channel: bool = DictField[bool](171)
    channel_only: bool = DictField[bool](172)
    target_channel: int = DictField[int](173)
    instant_offset: bool = DictField[bool](368)
    velocity_mod_x: float = DictField[float](582)
    velocity_mod_y: float = DictField[float](583)
    override_velocity: bool = DictField[bool](584)
    dont_slide: bool = DictField[bool](585)


class TriggerBgSpeed(Trigger):
    x_mod: float = DictField[float](143)
    y_mod: float = DictField[float](144)


class TriggerBpm(Trigger):
    duration: float = DictField[float](10)
    bpm: int = DictField[int](498)
    speed: enums.Speed = DictField[enums.Speed](499)
    disable: bool = DictField[bool](500)
    bpb: int = DictField[int](501)


class TriggerCameraEdge(Trigger):
    target_id: int = DictField[int](51)
    direction: enums.CameraEdge = DictField[enums.CameraEdge](164)


class TriggerCameraGuide(Trigger):
    offset_x: float = DictField[float](28)
    offset_y: float = DictField[float](29)
    zoom: float = DictField[float](371)
    preview_opacity: float = DictField[float](506)


class TriggerCameraMode(Trigger):
    free_mode: bool = DictField[bool](111)
    edit_settings: bool = DictField[bool](112)
    easing: float = DictField[float](113)
    padding: float = DictField[float](114)


class TriggerChangeBg(Trigger):
    bg_id: int = DictField[int](533)


class TriggerChangeGr(Trigger):
    gr_id: int = DictField[int](533)


class TriggerChangeMg(Trigger):
    mg_id: int = DictField[int](533)


class TriggerCheckpoint(Trigger):
    spawn_id: int = DictField[int](51)
    target_pos: int = DictField[int](71)
    player_pos: bool = DictField[bool](138)
    respawn_id: int = DictField[int](448)


class TriggerCollectible(Trigger):
    group_id: int = DictField[int](51)
    sub_count: bool = DictField[bool](78)
    item_id: int = DictField[int](80)
    pickup_item: bool = DictField[bool](381)
    toggle_trigger: bool = DictField[bool](382)
    points: int = DictField[int](383)
    particle: int = DictField[int](440)
    no_anim: bool = DictField[bool](463)


class TriggerCollectibleCoin(TriggerCollectible):
    coin_id: int = DictField[int](12)


class TriggerCollision(Trigger):
    target_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)
    block_a: int = DictField[int](80)
    exit: bool = DictField[bool](93)
    block_b: int = DictField[int](95)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    between_players: bool = DictField[bool](201)


class TriggerCollisionBlock(Trigger):
    block_id: int = DictField[int](80)
    dynamic: bool = DictField[bool](94)


class TriggerColor(Trigger):
    red: int = DictField[int](7)
    green: int = DictField[int](8)
    blue: int = DictField[int](9)
    duration: float = DictField[float](10)
    tint_ground: bool = DictField[bool](14)
    player_1: bool = DictField[bool](15)
    player_2: bool = DictField[bool](16)
    blending: bool = DictField[bool](17)
    channel: int = DictField[int](23)
    opacity: float = DictField[float](35)
    hsv: HSV = DictField[HSV](49)
    copy_id: int = DictField[int](50)
    copy_opacity: bool = DictField[bool](60)
    disable_legacy_hsv: bool = DictField[bool](210)


class TriggerCount(Trigger):
    target_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)
    count: int = DictField[int](77)
    item_id: int = DictField[int](80)
    multi_activate: bool = DictField[bool](104)


class TriggerDash(Trigger):
    speed: float = DictField[float](586)
    collide: bool = DictField[bool](587)
    end_boost: float = DictField[float](588)
    stop_slide: bool = DictField[bool](589)
    max_duration: float = DictField[float](590)


class TriggerEditAdvFollow(Trigger):
    target_id: int = DictField[int](51)
    follow_id: int = DictField[int](71)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    corner: bool = DictField[bool](201)
    speed: float = DictField[float](300)
    speed_rand: float = DictField[float](301)
    x_only: bool = DictField[bool](306)
    y_only: bool = DictField[bool](307)
    use_control_id: bool = DictField[bool](535)
    speed_ref: int = DictField[int](560)
    dir: float = DictField[float](563)
    dir_rand: float = DictField[float](564)
    dir_ref: int = DictField[int](565)
    mod_x: float = DictField[float](566)
    mod_x_rand: float = DictField[float](567)
    mod_y: float = DictField[float](568)
    mod_y_rand: float = DictField[float](569)
    redirect_dir: bool = DictField[bool](570)


class TriggerEffect(Trigger):
    duration: float = DictField[float](10)
    hsv: HSV = DictField[HSV](49)
    target_id: int = DictField[int](51)
    main_only: bool = DictField[bool](65)
    detail_only: bool = DictField[bool](66)
    center_id: int = DictField[int](71)
    enter_only: enums.EnterMode = DictField[enums.EnterMode](217)
    move_dist: int = DictField[int](218)
    move_dist_rand: int = DictField[int](219)
    offset: int = DictField[int](220)
    offset_rand: int = DictField[int](221)
    length: int = DictField[int](222)
    length_rand: int = DictField[int](223)
    effect_id: int = DictField[int](225)
    move_angle: int = DictField[int](231)
    move_angle_rand: int = DictField[int](232)
    scale_x: float = DictField[float](233)
    scale_x_rand: float = DictField[float](234)
    scale_y: float = DictField[float](235)
    scale_y_rand: float = DictField[float](236)
    move_x: int = DictField[int](237)
    move_x_rand: int = DictField[int](238)
    move_y: int = DictField[int](239)
    move_y_rand: int = DictField[int](240)
    xy_mode: bool = DictField[bool](241)
    easing: enums.Easing = DictField[enums.Easing](242)
    easing_rate: float = DictField[float](243)
    easing_2: enums.Easing = DictField[enums.Easing](248)
    easing_rate_2: float = DictField[float](249)
    offset_y: int = DictField[int](252)
    offset_y_rand: int = DictField[int](253)
    tint_channel: int = DictField[int](260)
    ease_out: bool = DictField[bool](261)
    direction: int = DictField[int](262)
    mod_front: float = DictField[float](263)
    mod_back: float = DictField[float](264)
    tint: float = DictField[float](265)
    rotate: float = DictField[float](270)
    rotate_rand: float = DictField[float](271)
    to_opacity: float = DictField[float](275)
    inwards: bool = DictField[bool](276)
    enable_hsv: bool = DictField[bool](278)
    deadzone: float = DictField[float](282)
    mirrored: bool = DictField[bool](283)
    from_opacity: float = DictField[float](286)
    relative: bool = DictField[bool](287)
    rfade: float = DictField[float](288)
    priority: int = DictField[int](341)
    enter_channel: int = DictField[int](344)
    use_effect_id: bool = DictField[bool](355)
    special_center: enums.EffectSpecialCenter = DictField[enums.EffectSpecialCenter](538)
    deap: bool = DictField[bool](539)


class TriggerEnd(Trigger):
    spawn_id: int = DictField[int](51)
    target_pos: int = DictField[int](71)
    no_effects: bool = DictField[bool](460)
    no_sfx: bool = DictField[bool](461)
    instant: bool = DictField[bool](487)


class TriggerEndWall(Trigger):
    group_id: int = DictField[int](51)
    lock_y: bool = DictField[bool](59)
    reverse: bool = DictField[bool](118)


class TriggerEnterPreset(Trigger):
    enter_only: enums.EnterMode = DictField[enums.EnterMode](217)
    enter_channel: int = DictField[int](344)


class TriggerEvent(Trigger):
    spawn_id: int = DictField[int](51)
    events: EventList = DictField[EventList](430)
    extra_id_1: int = DictField[int](447)
    extra_id_2: enums.TargetPlayer = DictField[enums.TargetPlayer](525)


class TriggerFollow(Trigger):
    duration: float = DictField[float](10)
    target_id: int = DictField[int](51)
    follow_target: int = DictField[int](71)
    mod_x: float = DictField[float](72)
    mod_y: float = DictField[float](73)


class TriggerFollowPlayerY(Trigger):
    duration: float = DictField[float](10)
    target_id: int = DictField[int](51)
    speed: float = DictField[float](90)
    delay: float = DictField[float](91)
    offset: int = DictField[int](92)
    max_speed: float = DictField[float](105)


class TriggerForceBlock(Trigger):
    value: float = DictField[float](149)
    value_min: float = DictField[float](526)
    value_max: float = DictField[float](527)
    relative: bool = DictField[bool](528)
    range: bool = DictField[bool](529)
    force_id: int = DictField[int](530)


class TriggerGamemodePortal(Trigger):
    free_mode: bool = DictField[bool](111)
    edit_settings: bool = DictField[bool](112)
    easing: float = DictField[float](113)
    padding: float = DictField[float](114)


class TriggerGameplayOffset(Trigger):
    offset_x: float = DictField[float](28)
    offset_y: float = DictField[float](29)
    dont_zoom_x: bool = DictField[bool](58)
    dont_zoom_y: bool = DictField[bool](59)


class TriggerGradient(Trigger):
    blending: enums.GradientBlending = DictField[enums.GradientBlending](174)
    layer: enums.GradientLayer = DictField[enums.GradientLayer](202)
    u: int = DictField[int](203)
    bl: int = DictField[int](203)
    d: int = DictField[int](204)
    br: int = DictField[int](204)
    l: int = DictField[int](205)
    tl: int = DictField[int](205)
    r: int = DictField[int](206)
    tr: int = DictField[int](206)
    vertex_mode: bool = DictField[bool](207)
    disable: bool = DictField[bool](208)
    gradient_id: int = DictField[int](209)
    preview_opacity: float = DictField[float](456)
    disable_all: bool = DictField[bool](508)


class TriggerGravity(Trigger):
    player_1: bool = DictField[bool](138)
    value: float = DictField[float](148)
    player_2: bool = DictField[bool](200)
    player_touch: bool = DictField[bool](201)


class TriggerInstantCollision(Trigger):
    true_id: int = DictField[int](51)
    false_id: int = DictField[int](71)
    block_a: int = DictField[int](80)
    block_b: int = DictField[int](95)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    between_players: bool = DictField[bool](201)
    dont_reset_remap: bool = DictField[bool](600)


class TriggerInstantCount(Trigger):
    target_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)
    count: int = DictField[int](77)
    item_id: int = DictField[int](80)
    mode: enums.InstantCountMode = DictField[enums.InstantCountMode](88)


class TriggerItemCompare(Trigger):
    true_id: int = DictField[int](51)
    false_id: int = DictField[int](71)
    item_id_1: int = DictField[int](80)
    item_id_2: int = DictField[int](95)
    item_type_1: enums.ItemType = DictField[enums.ItemType](476)
    item_type_2: enums.ItemType = DictField[enums.ItemType](477)
    mod_1: float = DictField[float](479)
    item_op_1: enums.ItemOperation = DictField[enums.ItemOperation](480)
    item_op_2: enums.ItemOperation = DictField[enums.ItemOperation](481)
    item_op_3: enums.ItemOperation = DictField[enums.ItemOperation](482)
    mod_2: float = DictField[float](483)
    tolerance: float = DictField[float](484)
    round_op_1: enums.ItemRoundOp = DictField[enums.ItemRoundOp](485)
    round_op_2: enums.ItemRoundOp = DictField[enums.ItemRoundOp](486)
    sign_op_1: enums.ItemSignOp = DictField[enums.ItemSignOp](578)
    sign_op_2: enums.ItemSignOp = DictField[enums.ItemSignOp](579)


class TriggerItemEdit(Trigger):
    target_item_id: int = DictField[int](51)
    item_id_1: int = DictField[int](80)
    item_id_2: int = DictField[int](95)
    item_type_1: enums.ItemType = DictField[enums.ItemType](476)
    item_type_2: enums.ItemType = DictField[enums.ItemType](477)
    item_type_3: enums.ItemType = DictField[enums.ItemType](478)
    mod: float = DictField[float](479)
    item_op_1: enums.ItemOperation = DictField[enums.ItemOperation](480)
    item_op_2: enums.ItemOperation = DictField[enums.ItemOperation](481)
    item_op_3: enums.ItemOperation = DictField[enums.ItemOperation](482)
    round_op_1: enums.ItemRoundOp = DictField[enums.ItemRoundOp](485)
    round_op_2: enums.ItemRoundOp = DictField[enums.ItemRoundOp](486)
    sign_op_1: enums.ItemSignOp = DictField[enums.ItemSignOp](578)
    sign_op_2: enums.ItemSignOp = DictField[enums.ItemSignOp](579)


class TriggerItemPersist(Trigger):
    item_id: int = DictField[int](80)
    set_persistent: bool = DictField[bool](491)
    target_all: bool = DictField[bool](492)
    reset: bool = DictField[bool](493)
    timer: bool = DictField[bool](494)


class TriggerKeyframe(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    group_id: int = DictField[int](51)
    spawn_id: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    key_id: int = DictField[int](373)
    index: int = DictField[int](374)
    ref_only: bool = DictField[bool](375)
    close_loop: bool = DictField[bool](376)
    prox: bool = DictField[bool](377)
    curve: bool = DictField[bool](378)
    time_mode: enums.KeyframeRefMode = DictField[enums.KeyframeRefMode](379)
    preview_art: bool = DictField[bool](380)
    auto_layer: bool = DictField[bool](459)
    line_opacity: float = DictField[float](524)
    spin_direction: enums.KeyframeSpin = DictField[enums.KeyframeSpin](536)
    full_rotations: int = DictField[int](537)
    spawn_delay: float = DictField[float](557)


class TriggerLinkVisible(Trigger):
    group_id: int = DictField[int](51)


class TriggerMgEdit(Trigger):
    duration: float = DictField[float](10)
    offset_y: float = DictField[float](29)
    easing: enums.Easing = DictField[enums.Easing](30)
    ease_rate: float = DictField[float](85)


class TriggerMgSpeed(Trigger):
    x_mod: float = DictField[float](143)
    y_mod: float = DictField[float](144)


class TriggerMove(Trigger):
    duration: float = DictField[float](10)
    move_x: float = DictField[float](28)
    move_y: float = DictField[float](29)
    easing: enums.Easing = DictField[enums.Easing](30)
    target_id: int = DictField[int](51)
    lock_player_x: bool = DictField[bool](58)
    lock_player_y: bool = DictField[bool](59)
    target_pos: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    target_mode: bool = DictField[bool](100)
    target_axis: enums.TargetAxis = DictField[enums.TargetAxis](101)
    player_1: bool = DictField[bool](138)
    lock_camera_x: bool = DictField[bool](141)
    lock_camera_y: bool = DictField[bool](142)
    follow_x_mod: float = DictField[float](143)
    follow_y_mod: float = DictField[float](144)
    player_2: bool = DictField[bool](200)
    use_small_step: bool = DictField[bool](393)
    direction_mode: bool = DictField[bool](394)
    target_center_id: int = DictField[int](395)
    target_distance: float = DictField[float](396)
    dynamic_mode: bool = DictField[bool](397)
    silent: bool = DictField[bool](544)


class TriggerObjectControl(Trigger):
    target_id: int = DictField[int](51)


class TriggerOffsetCamera(Trigger):
    offset_x: float = DictField[float](28)
    offset_y: float = DictField[float](29)
    easing: enums.Easing = DictField[enums.Easing](30)
    ease_rate: float = DictField[float](85)
    axis: enums.TargetAxis = DictField[enums.TargetAxis](101)


class TriggerOffsetGameplay(Trigger):
    axis: enums.TargetAxis = DictField[enums.TargetAxis](101)


class TriggerOnDeath(Trigger):
    group_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)


class TriggerOptions(Trigger):
    streak_additive: enums.Option = DictField[enums.Option](159)
    unlink_dual_gravity: enums.Option = DictField[enums.Option](160)
    hide_ground: enums.Option = DictField[enums.Option](161)
    hide_p1: enums.Option = DictField[enums.Option](162)
    hide_p2: enums.Option = DictField[enums.Option](163)
    disable_p1_controls: enums.Option = DictField[enums.Option](165)
    hide_mg: enums.Option = DictField[enums.Option](195)
    disable_controls_p1: enums.Option = DictField[enums.Option](199)
    hide_attempts: enums.Option = DictField[enums.Option](532)
    edit_respawn_time: enums.Option = DictField[enums.Option](573)
    respawn_time: float = DictField[float](574)
    audio_on_death: enums.Option = DictField[enums.Option](575)
    disable_death_sfx: enums.Option = DictField[enums.Option](576)
    boost_slide: enums.Option = DictField[enums.Option](593)


class TriggerOrbSaw(Trigger):
    rotation_speed: float = DictField[float](97)
    disable_rotation: bool = DictField[bool](98)


class TriggerPickup(Trigger):
    count: int = DictField[int](77)
    item_id: int = DictField[int](80)
    mode: enums.PickupMode = DictField[enums.PickupMode](88)
    override: bool = DictField[bool](139)
    mod: float = DictField[float](449)


class TriggerPlayerControl(Trigger):
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    stop_jump: bool = DictField[bool](540)
    stop_move: bool = DictField[bool](541)
    stop_rotation: bool = DictField[bool](542)
    stop_slide: bool = DictField[bool](543)


class TriggerPulse(Trigger):
    red: int = DictField[int](7)
    green: int = DictField[int](8)
    blue: int = DictField[int](9)
    fade_in: float = DictField[float](45)
    hold: float = DictField[float](46)
    fade_out: float = DictField[float](47)
    color_type: enums.PulseColorType = DictField[enums.PulseColorType](48)
    hsv: HSV = DictField[HSV](49)
    copy_id: int = DictField[int](50)
    target_id: int = DictField[int](51)
    target_type: enums.PulseTarget = DictField[enums.PulseTarget](52)
    main_only: bool = DictField[bool](65)
    detail_only: bool = DictField[bool](66)
    exclusive: bool = DictField[bool](86)
    disable_static_hsv: bool = DictField[bool](210)


class TriggerRandom(Trigger):
    chance: float = DictField[float](10)
    true_id: int = DictField[int](51)
    false_id: int = DictField[int](71)


class TriggerReset(Trigger):
    group_id: int = DictField[int](51)


class TriggerRotate(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    target_id: int = DictField[int](51)
    degrees: float = DictField[float](68)
    full: int = DictField[int](69)
    lock_rotation: bool = DictField[bool](70)
    center_id: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    aim_mode: bool = DictField[bool](100)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    follow_mode: bool = DictField[bool](394)
    dynamic_mode: bool = DictField[bool](397)
    aim_target: int = DictField[int](401)
    aim_offset: float = DictField[float](402)
    aim_easing: int = DictField[int](403)
    min_x_id: int = DictField[int](516)
    min_y_id: int = DictField[int](517)
    max_x_id: int = DictField[int](518)
    max_y_id: int = DictField[int](519)


class TriggerRotateCamera(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    degrees: float = DictField[float](68)
    add: bool = DictField[bool](70)
    ease_rate: float = DictField[float](85)
    snap_360: bool = DictField[bool](394)


class TriggerScale(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    target_id: int = DictField[int](51)
    center_id: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    only_move: bool = DictField[bool](133)
    scale_by_x: float = DictField[float](150)
    scale_by_y: float = DictField[float](151)
    div_by_x: bool = DictField[bool](153)
    div_by_y: bool = DictField[bool](154)
    relative_rotation: bool = DictField[bool](452)
    relative_scale: bool = DictField[bool](577)


class TriggerSequence(Trigger):
    sequence: SequenceList = DictField[SequenceList](435)
    mode: enums.SequenceMode = DictField[enums.SequenceMode](436)
    min_interval: float = DictField[float](437)
    reset_time: float = DictField[float](438)
    reset_type: enums.SequenceResetType = DictField[enums.SequenceResetType](439)
    unique_remap: bool = DictField[bool](505)


class TriggerSfx(Trigger):
    duration: float = DictField[float](10)
    group_id_1: int = DictField[int](51)
    group_id_2: int = DictField[int](71)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    sfx_id: int = DictField[int](392)
    speed: int = DictField[int](404)
    pitch: int = DictField[int](405)
    volume: float = DictField[float](406)
    use_reverb: bool = DictField[bool](407)
    start: int = DictField[int](408)
    fade_in: int = DictField[int](409)
    end: int = DictField[int](410)
    fade_out: int = DictField[int](411)
    fft: bool = DictField[bool](412)
    loop: bool = DictField[bool](413)
    stop_loop: bool = DictField[bool](414)
    unique: bool = DictField[bool](415)
    unique_id: int = DictField[int](416)
    stop: bool = DictField[bool](417)
    change_volume: bool = DictField[bool](418)
    change_speed: bool = DictField[bool](419)
    override: bool = DictField[bool](420)
    vol_near: float = DictField[float](421)
    vol_med: float = DictField[float](422)
    vol_far: float = DictField[float](423)
    dist_1: int = DictField[int](424)
    dist_2: int = DictField[int](425)
    dist_3: int = DictField[int](426)
    camera: bool = DictField[bool](428)
    pre_load: bool = DictField[bool](433)
    min_int: float = DictField[float](434)
    group: int = DictField[int](455)
    group_id: int = DictField[int](457)
    direction: enums.VolumeDirection = DictField[enums.VolumeDirection](458)
    ignore_volume: bool = DictField[bool](489)
    sfx_duration: float = DictField[float](490)
    reverb: enums.ReverbPreset = DictField[enums.ReverbPreset](502)
    override_reverb: bool = DictField[bool](503)
    speed_rand: int = DictField[int](596)
    pitch_rand: int = DictField[int](597)
    volume_rand: float = DictField[float](598)
    pitch_steps: bool = DictField[bool](599)


class TriggerShader(Trigger):
    fade_time: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    shockwave_center_id: int = DictField[int](51)
    shockline_center_id: int = DictField[int](51)
    lens_circle_center_id: int = DictField[int](51)
    radial_blur_center_id: int = DictField[int](51)
    motion_blur_center_id: int = DictField[int](51)
    bulge_center_id: int = DictField[int](51)
    pinch_center_id: int = DictField[int](51)
    gray_scale_tint_channel: int = DictField[int](51)
    lens_circle_tint_channel: int = DictField[int](71)
    radial_blur_ref_channel: int = DictField[int](71)
    motion_blur_ref_channel: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    shockwave_player_1: bool = DictField[bool](138)
    shockline_player_1: bool = DictField[bool](138)
    lens_circle_player_1: bool = DictField[bool](138)
    radial_blur_player_1: bool = DictField[bool](138)
    motion_blur_player_1: bool = DictField[bool](138)
    bulge_player_1: bool = DictField[bool](138)
    pinch_player_1: bool = DictField[bool](138)
    shockwave_speed: float = DictField[float](175)
    shockline_speed: float = DictField[float](175)
    glitch_speed: float = DictField[float](175)
    chromatic_glitch_speed: float = DictField[float](175)
    edit_color_cb: float = DictField[float](175)
    shockwave_strength: float = DictField[float](176)
    shockline_strength: float = DictField[float](176)
    glitch_strength: float = DictField[float](176)
    chromatic_glitch_strength: float = DictField[float](176)
    lens_circle_strength: float = DictField[float](176)
    radial_blur_intensity: float = DictField[float](176)
    motion_blur_intensity: float = DictField[float](176)
    bulge_bulge: float = DictField[float](176)
    gray_scale_target: float = DictField[float](176)
    sepia_target: float = DictField[float](176)
    invert_color_target: float = DictField[float](176)
    hue_degrees: float = DictField[float](176)
    edit_color_cr: float = DictField[float](176)
    shockwave_time_offset: float = DictField[float](177)
    shockline_time_offset: float = DictField[float](177)
    shockwave_wave_width: float = DictField[float](179)
    shockline_wave_width: float = DictField[float](179)
    glitch_slice_height: float = DictField[float](179)
    chromatic_glitch_line_thickness: float = DictField[float](179)
    lens_circle_size: float = DictField[float](179)
    radial_blur_size: float = DictField[float](179)
    pinch_modifier: float = DictField[float](179)
    invert_color_r: float = DictField[float](179)
    edit_color_br: float = DictField[float](179)
    shockwave_thickness: float = DictField[float](180)
    shockline_thickness: float = DictField[float](180)
    chromatic_target_x: float = DictField[float](180)
    chromatic_glitch_rgb_offset: float = DictField[float](180)
    pixelate_target_x: float = DictField[float](180)
    motion_blur_target_x: float = DictField[float](180)
    bulge_radius: float = DictField[float](180)
    pinch_target_x: float = DictField[float](180)
    invert_color_g: float = DictField[float](180)
    edit_color_bg: float = DictField[float](180)
    split_screen_target_x: float = DictField[float](180)
    shockwave_fade_in: float = DictField[float](181)
    shockline_fade_in: float = DictField[float](181)
    glitch_max_col_x_offset: float = DictField[float](181)
    lens_circle_fade: float = DictField[float](181)
    radial_blur_fade: float = DictField[float](181)
    motion_blur_fade: float = DictField[float](181)
    shockwave_fade_out: float = DictField[float](182)
    shockline_fade_out: float = DictField[float](182)
    glitch_max_col_y_offset: float = DictField[float](182)
    shockwave_inner: float = DictField[float](183)
    shockwave_invert: bool = DictField[bool](184)
    shockline_invert: bool = DictField[bool](184)
    shockline_flip: bool = DictField[bool](185)
    shockline_rotate: bool = DictField[bool](186)
    shockline_dual: bool = DictField[bool](187)
    shader_opt_ignore_player_particles: bool = DictField[bool](188)
    shockwave_target: bool = DictField[bool](188)
    shockline_target: bool = DictField[bool](188)
    chromatic_use_x: bool = DictField[bool](188)
    pixelate_use_x: bool = DictField[bool](188)
    radial_blur_target: bool = DictField[bool](188)
    motion_blur_use_x: bool = DictField[bool](188)
    bulge_target: bool = DictField[bool](188)
    pinch_target: bool = DictField[bool](188)
    gray_scale_use_lum: bool = DictField[bool](188)
    invert_color_edit_rgb: bool = DictField[bool](188)
    split_screen_use_x: bool = DictField[bool](188)
    chromatic_target_y: float = DictField[float](189)
    chromatic_glitch_segment_h: float = DictField[float](189)
    pixelate_target_y: float = DictField[float](189)
    motion_blur_target_y: float = DictField[float](189)
    invert_color_b: float = DictField[float](189)
    edit_color_bb: float = DictField[float](189)
    split_screen_target_y: float = DictField[float](189)
    shockwave_follow: bool = DictField[bool](190)
    shockline_follow: bool = DictField[bool](190)
    chromatic_use_y: bool = DictField[bool](190)
    pixelate_use_y: bool = DictField[bool](190)
    motion_blur_use_y: bool = DictField[bool](190)
    pinch_use_x: bool = DictField[bool](190)
    gray_scale_use_tint: bool = DictField[bool](190)
    invert_color_tween_rgb: bool = DictField[bool](190)
    split_screen_use_y: bool = DictField[bool](190)
    shockwave_outer: float = DictField[float](191)
    glitch_max_slice_x_offset: float = DictField[float](191)
    chromatic_glitch_line_strength: float = DictField[float](191)
    motion_blur_follow_ease: float = DictField[float](191)
    edit_color_cg: float = DictField[float](191)
    shader_opt_disable_all: bool = DictField[bool](192)
    chromatic_glitch_disable: bool = DictField[bool](192)
    chromatic_glitch_relative_pos: bool = DictField[bool](194)
    pixelate_snap_grid: bool = DictField[bool](194)
    motion_blur_dual_dir: bool = DictField[bool](194)
    pinch_use_y: bool = DictField[bool](194)
    invert_color_clamp_rgb: bool = DictField[bool](194)
    shader_opt_layer_min: enums.GradientLayer = DictField[enums.GradientLayer](196)
    shader_opt_layer_max: enums.GradientLayer = DictField[enums.GradientLayer](197)
    shockwave_player_2: bool = DictField[bool](200)
    shockline_player_2: bool = DictField[bool](200)
    lens_circle_player_2: bool = DictField[bool](200)
    radial_blur_player_2: bool = DictField[bool](200)
    motion_blur_player_2: bool = DictField[bool](200)
    bulge_player_2: bool = DictField[bool](200)
    pinch_player_2: bool = DictField[bool](200)
    motion_blur_center: bool = DictField[bool](201)
    shockwave_screen_offset_x: float = DictField[float](290)
    shockline_screen_offset: float = DictField[float](290)
    lens_circle_screen_offset_x: float = DictField[float](290)
    radial_blur_screen_offset_x: float = DictField[float](290)
    bulge_screen_offset_x: float = DictField[float](290)
    pinch_screen_offset_x: float = DictField[float](290)
    shockwave_screen_offset_y: float = DictField[float](291)
    lens_circle_screen_offset_y: float = DictField[float](291)
    radial_blur_screen_offset_y: float = DictField[float](291)
    bulge_screen_offset_y: float = DictField[float](291)
    pinch_screen_offset_y: float = DictField[float](291)
    shockwave_max_size: float = DictField[float](512)
    shockline_max_size: float = DictField[float](512)
    pinch_radius: float = DictField[float](512)
    shockwave_animate: bool = DictField[bool](513)
    shockline_animate: bool = DictField[bool](513)
    shockwave_relative: bool = DictField[bool](514)
    shockline_relative: bool = DictField[bool](514)
    glitch_relative: bool = DictField[bool](514)
    chromatic_relative: bool = DictField[bool](514)
    chromatic_glitch_relative: bool = DictField[bool](514)
    pixelate_relative: bool = DictField[bool](514)
    lens_circle_relative: bool = DictField[bool](514)
    motion_blur_relative: bool = DictField[bool](514)
    bulge_relative: bool = DictField[bool](514)
    relative: bool = DictField[bool](514)
    pixelate_hard_edges: bool = DictField[bool](515)
    radial_blur_empty_only: bool = DictField[bool](515)
    motion_blur_empty_only: bool = DictField[bool](515)
    disable_preview: bool = DictField[bool](531)


class TriggerShake(Trigger):
    duration: float = DictField[float](10)
    strength: float = DictField[float](75)
    interval: float = DictField[float](84)


class TriggerSong(Trigger):
    duration: float = DictField[float](10)
    group_id_1: int = DictField[int](51)
    group_id_2: int = DictField[int](71)
    player_1: bool = DictField[bool](138)
    player_2: bool = DictField[bool](200)
    song_id: int = DictField[int](392)
    prep: bool = DictField[bool](399)
    load_prep: bool = DictField[bool](400)
    speed: int = DictField[int](404)
    volume: float = DictField[float](406)
    start: int = DictField[int](408)
    fade_in: int = DictField[int](409)
    end: int = DictField[int](410)
    fade_out: int = DictField[int](411)
    loop: bool = DictField[bool](413)
    stop_loop: bool = DictField[bool](414)
    stop: bool = DictField[bool](417)
    change_volume: bool = DictField[bool](418)
    change_speed: bool = DictField[bool](419)
    vol_near: float = DictField[float](421)
    vol_med: float = DictField[float](422)
    fol_var: float = DictField[float](423)
    dist_1: int = DictField[int](424)
    dist_2: int = DictField[int](425)
    dist_3: int = DictField[int](426)
    camera: bool = DictField[bool](428)
    channel: int = DictField[int](432)
    direction: enums.VolumeDirection = DictField[enums.VolumeDirection](458)
    dont_reset: bool = DictField[bool](595)


class TriggerSpawn(Trigger):
    group_id: int = DictField[int](51)
    delay: float = DictField[float](63)
    disable_preview: bool = DictField[bool](102)
    ordered: bool = DictField[bool](441)
    remaps: RemapList = DictField[RemapList](442)
    delay_rand: float = DictField[float](556)
    reset_remap: bool = DictField[bool](581)


class TriggerSpawnParticle(Trigger):
    particle_group: int = DictField[int](51)
    position_group: int = DictField[int](71)
    offset_x: float = DictField[float](547)
    offset_y: float = DictField[float](548)
    offvar_x: float = DictField[float](549)
    offvar_y: float = DictField[float](550)
    match_rot: bool = DictField[bool](551)
    rotation: float = DictField[float](552)
    rotation_rand: float = DictField[float](553)
    scale: float = DictField[float](554)
    scale_rand: float = DictField[float](555)


class TriggerStateBlock(Trigger):
    state_on: int = DictField[int](51)
    state_off: int = DictField[int](71)


class TriggerStaticCamera(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    target_id: int = DictField[int](71)
    ease_rate: float = DictField[float](85)
    axis: enums.TargetAxis = DictField[enums.TargetAxis](101)
    exit: bool = DictField[bool](110)
    follow_group: bool = DictField[bool](212)
    follow_easing: float = DictField[float](213)
    smooth_velocity: bool = DictField[bool](453)
    velocity_mod: float = DictField[float](454)
    exit_instant: bool = DictField[bool](465)


class TriggerStop(Trigger):
    target_id: int = DictField[int](51)
    use_control_id: bool = DictField[bool](535)
    mode: enums.StopMode = DictField[enums.StopMode](580)


class TriggerTeleport(Trigger):
    target_id: int = DictField[int](51)
    smooth_ease: bool = DictField[bool](55)
    use_force: bool = DictField[bool](345)
    force: float = DictField[float](346)
    redirect_force: bool = DictField[bool](347)
    force_min: float = DictField[float](348)
    force_max: float = DictField[float](349)
    force_mod: float = DictField[float](350)
    keep_offset: bool = DictField[bool](351)
    ignore_x: bool = DictField[bool](352)
    ignore_y: bool = DictField[bool](353)
    gravity: enums.GravityMode = DictField[enums.GravityMode](354)
    additive_force: bool = DictField[bool](443)
    instant_camera: bool = DictField[bool](464)
    snap_ground: bool = DictField[bool](510)
    redirect_dash: bool = DictField[bool](591)


class TriggerTeleportPortal(TriggerTeleport):
    distance: float = DictField[float](54)


class TriggerTime(Trigger):
    target_id: int = DictField[int](51)
    item_id: int = DictField[int](80)
    start_time: float = DictField[float](467)
    dont_override: bool = DictField[bool](468)
    ignore_timewarp: bool = DictField[bool](469)
    mod: float = DictField[float](470)
    start_paused: bool = DictField[bool](471)
    stop_time: float = DictField[float](473)
    stop: bool = DictField[bool](474)


class TriggerTimeControl(Trigger):
    item_id: int = DictField[int](80)
    stop: enums.TimeControlType = DictField[enums.TimeControlType](472)


class TriggerTimeEvent(Trigger):
    target_id: int = DictField[int](51)
    item_id: int = DictField[int](80)
    target_time: float = DictField[float](473)
    multi_activate: bool = DictField[bool](475)


class TriggerToggle(Trigger):
    group_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)


class TriggerToggleBlock(Trigger):
    group_id: int = DictField[int](51)
    activate_group: bool = DictField[bool](56)
    claim_touch: bool = DictField[bool](445)
    spawn_only: bool = DictField[bool](504)


class TriggerTouch(Trigger):
    group_id: int = DictField[int](51)
    hold_mode: bool = DictField[bool](81)
    toggle_mode: enums.TouchMode = DictField[enums.TouchMode](82)
    dual_mode: bool = DictField[bool](89)
    only_player: enums.TargetPlayer = DictField[enums.TargetPlayer](198)


class TriggerUi(Trigger):
    group_id: int = DictField[int](51)
    ui_target: int = DictField[int](71)
    ref_x: enums.UIRef = DictField[enums.UIRef](385)
    ref_y: enums.UIRef = DictField[enums.UIRef](386)
    relative_x: bool = DictField[bool](387)
    relative_y: bool = DictField[bool](388)


class TriggerZoomCamera(Trigger):
    duration: float = DictField[float](10)
    easing: enums.Easing = DictField[enums.Easing](30)
    ease_rate: float = DictField[float](85)
    zoom: float = DictField[float](371)