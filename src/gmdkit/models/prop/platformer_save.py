# Imports
from typing import Optional

# Package Imports
from gmdkit.utils.enums import Easing, GameEvents
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import CompressFileMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.models.prop.archive import ArchiveStruct, ArchiveListMixin, ArchiveDictMixin, inline, nested, rest
from gmdkit.serialization.classes import LazyString, TokenStream
from gmdkit.serialization.type_cast import to_bool, from_bool, from_float
from gmdkit.models.prop.color import HSV
from gmdkit.models.prop.pos_list import Position


@dataclass_decoder(slots=True)
class Color(ArchiveStruct):
    r: int = 0
    g: int = 0
    b: int = 0


def int_keyed(cls: type):
    def decode(stream: TokenStream):
        return int(stream.pop()), cls.from_tokens(stream)

    def encode(key: int, value, out: list):
        out.append(str(key))
        value.to_tokens(out)

    return staticmethod(decode), staticmethod(encode)


def int_pair_keyed(cls: type):
    def decode(stream: TokenStream):
        return (int(stream.pop()), int(stream.pop())), cls.from_tokens(stream)

    def encode(key: tuple[int, int], value, out: list):
        out += (str(key[0]), str(key[1]))
        value.to_tokens(out)

    return staticmethod(decode), staticmethod(encode)


def event_keyed(cls: type):
    def decode(stream: TokenStream):
        return (GameEvents.from_string(stream.pop()), int(stream.pop())), cls.from_tokens(stream)

    def encode(key: tuple[GameEvents, int], value, out: list):
        out += (str(int(key[0].value)), str(key[1]))
        value.to_tokens(out)

    return staticmethod(decode), staticmethod(encode)


def _read_double_pair_entry(stream: TokenStream):
    return int(stream.pop()), (float(stream.pop()), float(stream.pop()))


def _write_double_pair_entry(key: int, value: tuple[float, float], out: list):
    out += (str(key), from_float(value[0]), from_float(value[1]))


def _read_int_pair_key_entry(stream: TokenStream):
    return (int(stream.pop()), int(stream.pop())), int(stream.pop())


def _write_int_pair_key_entry(key: tuple[int, int], value: int, out: list):
    out += (str(key[0]), str(key[1]), str(value))


def _read_event_key_entry(stream: TokenStream):
    return (GameEvents.from_string(stream.pop()), int(stream.pop())), int(stream.pop())


def _write_event_key_entry(key: tuple[GameEvents, int], value: int, out: list):
    out += (str(int(key[0].value)), str(key[1]), str(value))


class ArchiveIntList(ArchiveListMixin, ListClass[int]):
    pass


class ObjectIDList(ArchiveListMixin, ListClass[int]):
    pass


class ArchiveFloatList(ArchiveListMixin, ListClass[float]):
    DECODER = float
    ENCODER = staticmethod(from_float)


class ArchiveIntPairList(ArchiveListMixin, ListClass[tuple[int, int]]):
    GROUP_SIZE = 2
    DECODER = staticmethod(lambda t: (int(t[0]), int(t[1])))
    ENCODER = staticmethod(lambda v: (str(v[0]), str(v[1])))


class ArchiveItemDict(ArchiveDictMixin, DictClass[int, int]):
    pass


class ObjectIDDict(ArchiveDictMixin, DictClass[int, int]):
    pass


class ArchiveBoolDict(ArchiveDictMixin, DictClass[int, bool]):
    DECODER = staticmethod(lambda k, v: (int(k), to_bool(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), from_bool(v)))


class ArchiveFloatDict(ArchiveDictMixin, DictClass[int, float]):
    DECODER = staticmethod(lambda k, v: (int(k), float(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), from_float(v)))


class DoublePairDict(ArchiveDictMixin, DictClass[int, tuple[float, float]]):
    USE_STREAMS = True
    DECODER = staticmethod(_read_double_pair_entry)
    ENCODER = staticmethod(_write_double_pair_entry)


class IntPairKeyDict(ArchiveDictMixin, DictClass[tuple[int, int], int]):
    USE_STREAMS = True
    DECODER = staticmethod(_read_int_pair_key_entry)
    ENCODER = staticmethod(_write_int_pair_key_entry)


class EventCountDict(ArchiveDictMixin, DictClass[tuple[GameEvents, int], int]):
    USE_STREAMS = True
    DECODER = staticmethod(_read_event_key_entry)
    ENCODER = staticmethod(_write_event_key_entry)


class IntListDict(ArchiveDictMixin, DictClass[int, ArchiveIntList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    DECODER = staticmethod(lambda k, v: (int(k), ArchiveIntList.from_string(v)))
    ENCODER = staticmethod(lambda k, v: (str(k), v.to_string()))


@dataclass_decoder(slots=True)
class EnterEffectAnimValue(ArchiveStruct):
    value: float = 0.0
    distance: float = 0.0
    duration: float = 0.0
    elapsed: float = 0.0
    easing_type: Easing = field_decoder(default=Easing.NONE, decoder=Easing.from_string)
    easing_rate: float = 0.0
    easing_buffer: int = 0


class EnterEffectAnimValueDict(ArchiveDictMixin, DictClass[int, EnterEffectAnimValue]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(EnterEffectAnimValue)


@dataclass_decoder(slots=True)
class GJValueTween(ArchiveStruct):
    from_value: float = 0.0
    to_value: float = 0.0
    duration: float = 0.0
    delta_time: float = 0.0
    current_value: float = 0.0
    easing_type: Easing = field_decoder(default=Easing.NONE, decoder=Easing.from_string)
    easing_rate: float = 0.0
    finished: bool = False
    disabled: bool = False
    unique_id: int = 0
    control_id: int = 0


@dataclass_decoder(slots=True)
class GameObjectPhysics(ArchiveStruct):
    object: int = 0
    velocity: Position = inline(Position)
    direction: Position = inline(Position)
    target_angle: float = 0.0
    turn_speed: float = 0.0
    unused_int_20: int = 0
    last_update_step: int = 0
    exclusive_step: int = 0


@dataclass_decoder(slots=True)
class OpacityEffectAction(ArchiveStruct):
    duration: float = 0.0
    from_value: float = 0.0
    to_value: float = 0.0
    finished: bool = False
    disabled: bool = False
    delta_time: float = 0.0
    target_group_id: int = 0
    current_value: float = 0.0
    trigger_unique_id: int = 0
    control_id: int = 0
    editor_seek_offset: float = 0.0
    editor_trigger_time: float = 0.0


@dataclass_decoder(slots=True)
class SongChannelState(ArchiveStruct):
    song_trigger: int = 0
    start_time: float = 0.0
    prepared_trigger: int = 0
    prepare_time: float = 0.0


@dataclass_decoder(slots=True)
class SongTriggerState(ArchiveStruct):
    song_trigger: int = 0
    start_time: float = 0.0


@dataclass_decoder(slots=True)
class FMODSoundTween(ArchiveStruct):
    interval: float = 0.0
    duration: float = 0.0
    start: float = 0.0
    end: float = 0.0
    value: float = 0.0
    finished: bool = False


@dataclass_decoder(slots=True)
class SFXTriggerInstance(ArchiveStruct):
    sfx_trigger: int = 0
    group_id1: int = 0
    group_id2: int = 0
    control_id: int = 0


@dataclass_decoder(slots=True)
class TimerItem(ArchiveStruct):
    item_id: int = 0
    time: float = 0.0
    active: bool = False
    time_mod: float = 0.0
    ignore_time_warp: bool = False
    target_time: float = 0.0
    stop_time_enabled: bool = False
    target_group_id: int = 0
    trigger_unique_id: int = 0
    control_id: int = 0
    remap_keys: ArchiveIntList = nested(ArchiveIntList)
    disabled: bool = False


@dataclass_decoder(slots=True)
class SequenceTriggerState(ArchiveStruct):
    sequence_times: ArchiveFloatDict = nested(ArchiveFloatDict)
    sequence_indices: ArchiveItemDict = nested(ArchiveItemDict)


@dataclass_decoder(slots=True)
class FMODQueuedMusic(ArchiveStruct):
    file_path: str = ""
    pitch: float = 0.0
    unused_float_1c: float = 0.0
    volume: float = 0.0
    start: int = 0
    end: int = 0
    fade_in: int = 0
    fade_out: int = 0
    loop: bool = False
    music_id: int = 0
    stop_music: bool = False
    channel_id: int = 0
    no_prepare: bool = False
    queued_status: int = 0
    dont_reset: bool = False


@dataclass_decoder(slots=True)
class FMODSoundState(ArchiveStruct):
    file_path: str = ""
    speed: float = 0.0
    unused_float_1c: float = 0.0
    volume: float = 0.0
    should_loop: bool = False
    channel_id: int = 0
    fade_point_count: int = 0
    fade_volume1: float = 0.0
    fade_volume2: float = 0.0
    fade_volume3: float = 0.0
    fade_volume4: float = 0.0
    fade_clock1: int = 0
    fade_clock2: int = 0
    fade_clock3: int = 0
    fade_clock4: int = 0
    dsp_clock: int = 0
    loop_start: int = 0
    loop_end: int = 0
    position: int = 0
    delay_start: int = 0
    delay_end: int = 0
    delay_stops: int = 0
    unique_id: int = 0
    sfx_group: int = 0
    pitch: float = 0.0
    fast_fourier_transform: bool = False
    reverb: bool = False
    effect_id: int = 0
    is_music: bool = False
    music_id: int = 0
    unused_bool_b4: bool = False


@dataclass_decoder(slots=True)
class EnterEffectInstance(ArchiveStruct):
    object: int = 0
    reversed: bool = False
    target_id: int = 0
    center_id: int = 0
    paused: bool = False
    pause_pending: bool = False
    start_order: int = 0
    unused_bool_c6: bool = False
    ease_index: int = 0
    target_group_index: int = 0
    ease_indices: ArchiveIntList = nested(ArchiveIntList)
    control_id: int = 0
    length: float = 0.0
    length_variance: float = 0.0
    offset: float = 0.0
    offset_variance: float = 0.0
    offset_y: float = 0.0
    offset_y_variance: float = 0.0
    mod_front: float = 0.0
    mod_back: float = 0.0
    deadzone: float = 0.0
    move_distance: float = 0.0
    move_distance_variance: float = 0.0
    move_angle: float = 0.0
    move_angle_variance: float = 0.0
    move_x: float = 0.0
    move_x_variance: float = 0.0
    move_y: float = 0.0
    move_y_variance: float = 0.0
    relative_fade: float = 0.0
    scale_x: float = 0.0
    scale_x_variance: float = 0.0
    scale_y: float = 0.0
    scale_y_variance: float = 0.0
    rotation: float = 0.0
    rotation_variance: float = 0.0
    tint: float = 0.0
    unused_key_285: float = 0.0
    to_opacity: float = 0.0
    from_opacity: float = 0.0
    hue: float = 0.0
    saturation: float = 0.0
    brightness: float = 0.0
    hsv_abs_s: bool = False
    hsv_abs_v: bool = False
    anim_values: EnterEffectAnimValueDict = nested(EnterEffectAnimValueDict)


@dataclass_decoder(slots=True)
class AdvancedFollowInstance(ArchiveStruct):
    trigger: int = 0
    group: int = 0
    object_key: int = 0
    control_id: int = 0
    other_object_key: int = 0
    start_order: int = 0
    paused: bool = False
    pause_pending: bool = False
    stopped: bool = False
    initialized: bool = False


@dataclass_decoder(slots=True)
class DynamicObjectAction(ArchiveStruct):
    trigger: int = 0
    center_object: int = 0
    aim_target_object: int = 0
    target_object: int = 0
    min_x_object: int = 0
    min_y_object: int = 0
    max_x_object: int = 0
    max_y_object: int = 0
    elapsed: float = 0.0
    eased_elapsed: float = 0.0
    eased_progress: float = 0.0
    just_started: bool = False
    stopped: bool = False
    paused: bool = False
    pause_pending: bool = False
    control_id: int = 0
    target_group_id: int = 0
    center_group_id: int = 0


@dataclass_decoder(slots=True)
class SFXStateContainer(ArchiveStruct):
    start_time: float = 0.0
    duration: float = 0.0
    target: float = 0.0
    unused_from: float = 0.0
    active: bool = False


@dataclass_decoder(slots=True)
class SFXTriggerState(ArchiveStruct):
    sfx_trigger: int = 0
    instance_id: int = 0
    start_time: float = 0.0
    play_position: float = 0.0
    position_time: float = 0.0
    last_update_time: float = 0.0
    speed: float = 0.0
    group_speed: float = 0.0
    volume: float = 0.0
    length: float = 0.0
    index: int = 0
    finished: bool = False
    loop: bool = False
    speed_tween: SFXStateContainer = inline(SFXStateContainer)
    group_speed_tween: SFXStateContainer = inline(SFXStateContainer)
    volume_tween: SFXStateContainer = inline(SFXStateContainer)


@dataclass_decoder(slots=True)
class CAState(ArchiveStruct):
    from_color: Color = inline(Color)
    to_color: Color = inline(Color)
    color: Color = inline(Color)
    paused: bool = False
    blending: bool = False
    copy_opacity: bool = False
    legacy_hsv: bool = False
    player_color: int = 0
    color_id: int = 0
    copy_id: int = 0
    unique_id: int = 0
    duration: float = 0.0
    from_opacity: float = 0.0
    to_opacity: float = 0.0
    delta_time: float = 0.0
    current_opacity: float = 0.0
    copy_hsv: HSV = inline(HSV)


@dataclass_decoder(slots=True)
class PulseEffectAction(ArchiveStruct):
    disabled: bool = False
    fade_in_time: float = 0.0
    hold_time: float = 0.0
    fade_out_time: float = 0.0
    delta_time: float = 0.0
    target_group_id: int = 0
    current_value: float = 0.0
    color: Color = inline(Color)
    pulse_effect_type: int = 0
    hsv: HSV = inline(HSV)
    color_index: int = 0
    main_only: bool = False
    detail_only: bool = False
    is_dynamic_hsv: bool = False
    trigger_unique_id: int = 0
    control_id: int = 0
    start_time: float = 0.0


@dataclass_decoder(slots=True)
class CountTriggerAction(ArchiveStruct):
    disabled: bool = False
    previous_count: int = 0
    target_count: int = 0
    target_group_id: int = 0
    activate_group: bool = False
    trigger_unique_id: int = 0
    control_id: int = 0
    item_id: int = 0
    multi_activate: bool = False
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class TimerTriggerAction(ArchiveStruct):
    disabled: bool = False
    time: float = 0.0
    target_time: float = 0.0
    target_group_id: int = 0
    trigger_unique_id: int = 0
    control_id: int = 0
    item_id: int = 0
    multi_activate: bool = False
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class TouchToggleAction(ArchiveStruct):
    disabled: bool = False
    target_group_id: int = 0
    hold_mode: bool = False
    touch_trigger_type: int = 0
    touch_trigger_control: int = 0
    trigger_unique_id: int = 0
    control_id: int = 0
    dual_mode: bool = False
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class CollisionTriggerAction(ArchiveStruct):
    disabled: bool = False
    block_a_id: int = 0
    block_b_id: int = 0
    target_group_id: int = 0
    trigger_on_exit: int = 0
    activate_group: bool = False
    trigger_unique_id: int = 0
    control_id: int = 0
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class ToggleTriggerAction(ArchiveStruct):
    disabled: bool = False
    target_group_id: int = 0
    activate_group: bool = False
    trigger_unique_id: int = 0
    control_id: int = 0
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class SpawnTriggerAction(ArchiveStruct):
    finished: bool = False
    disabled: bool = False
    duration: float = 0.0
    delta_time: float = 0.0
    target_group_id: int = 0
    trigger_unique_id: int = 0
    control_id: int = 0
    spawn_ordered: bool = False
    object: int = 0
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class EventTriggerInstance(ArchiveStruct):
    target_id: int = 0
    unique_id: int = 0
    control_id: int = 0
    inactive: bool = False
    remap_keys: ArchiveIntList = nested(ArchiveIntList)


@dataclass_decoder(slots=True)
class KeyframeObject(ArchiveStruct):
    duration: float = 0.0
    easing_type: int = 0
    easing_rate: float = 0.0
    ref_only: bool = False
    spawn_group: int = 0
    spawn_delay: float = 0.0
    proximity: bool = False
    spawned: bool = False
    curve: bool = False
    curve_length: float = 0.0
    ref_run_duration: float = 0.0
    time_mode: int = 0
    keyframe_object: int = 0
    position_delta: Position = inline(Position)
    position: Position = inline(Position)
    scale_x: float = 0.0
    scale_y: float = 0.0
    rotation: float = 0.0
    unused_double_1b0: float = 0.0
    opacity: float = 0.0


class KeyframeObjectList(ArchiveListMixin, ListClass[KeyframeObject]):
    USE_STREAMS = True
    DECODER = staticmethod(KeyframeObject.from_tokens)
    ENCODER = staticmethod(KeyframeObject.to_tokens)


@dataclass_decoder(slots=True)
class GroupCommandObject2(ArchiveStruct):
    group_command_unique_id: int = 0
    move_offset: Position = inline(Position)
    easing_type: Easing = field_decoder(default=Easing.NONE, decoder=Easing.from_string)
    easing_rate: float = 0.0
    duration: float = 0.0
    delta_time: float = 0.0
    target_group_id: int = 0
    center_group_id: int = 0
    current_x_offset: float = 0.0
    current_y_offset: float = 0.0
    delta_x: float = 0.0
    delta_y: float = 0.0
    old_delta_x: float = 0.0
    old_delta_y: float = 0.0
    locked_current_x_offset: float = 0.0
    locked_current_y_offset: float = 0.0
    finished: bool = False
    disabled: bool = False
    is_noop: bool = False
    lock_to_player_x: bool = False
    lock_to_player_y: bool = False
    lock_to_camera_x: bool = False
    lock_to_camera_y: bool = False
    locked_in_x: bool = False
    locked_in_y: bool = False
    move_mod_x: float = 0.0
    move_mod_y: float = 0.0
    current_rotate_or_transform_value: float = 0.0
    current_rotate_or_transform_delta: float = 0.0
    applied_value: float = 0.0
    applied_value_optimized: float = 0.0
    rotation_offset: float = 0.0
    lock_object_rotation: bool = False
    target_player: int = 0
    follow_x_mod: float = 0.0
    follow_y_mod: float = 0.0
    command_type: int = 0
    interp1: float = 0.0
    interp2: float = 0.0
    last_keyframe_rotation: float = 0.0
    target_scale_x: float = 0.0
    target_scale_y: float = 0.0
    transform_property_450: float = 0.0
    transform_property_451: float = 0.0
    last_applied_value: float = 0.0
    last_applied_value_optimized: float = 0.0
    only_move: bool = False
    unused_bool_121: bool = False
    relative_rotation: bool = False
    last_scale_x: float = 0.0
    last_scale_y: float = 0.0
    follow_y_speed: float = 0.0
    follow_y_delay: float = 0.0
    follow_y_offset: int = 0
    follow_y_max_speed: float = 0.0
    trigger_unique_id: int = 0
    control_id: int = 0
    delta_x_3: float = 0.0
    delta_y_3: float = 0.0
    old_delta_x_3: float = 0.0
    old_delta_y_3: float = 0.0
    unused_double_180: float = 0.0
    unused_double_188: float = 0.0
    action_type1: int = 0
    action_type2: int = 0
    action_value1: float = 0.0
    action_value2: float = 0.0
    processed_this_step: bool = False
    delta_time_float: float = 0.0
    already_updated: bool = False
    do_update: bool = False
    last_keyframe_position: Position = inline(Position)
    object: int = 0
    object_rotation: float = 0.0
    remap_keys: ArchiveIntList = nested(ArchiveIntList)
    reset_rscale: bool = False
    step_stamp: int = 0
    keyframes: KeyframeObjectList = inline(KeyframeObjectList)


@dataclass_decoder(slots=True)
class SavedObjectStateRef(ArchiveStruct):
    object: int = 0
    position_x: float = 0.0
    position_y: float = 0.0
    rotation_x_offset: float = 0.0
    rotation_y_offset: float = 0.0
    add_to_custom_scale_x: float = 0.0
    add_to_custom_scale_y: float = 0.0
    step_start_x: float = 0.0
    step_start_y: float = 0.0


@dataclass_decoder(slots=True)
class SavedActiveObjectState(ArchiveStruct):
    object: int = 0
    activated_by_player1: bool = False
    activated_by_player2: bool = False


@dataclass_decoder(slots=True)
class SavedSpecialObjectState(ArchiveStruct):
    object: int = 0
    animation_id: int = 0


class GJValueTweenDict(ArchiveDictMixin, DictClass[int, GJValueTween]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(GJValueTween)


class GameObjectPhysicsDict(ArchiveDictMixin, DictClass[int, GameObjectPhysics]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(GameObjectPhysics)


class OpacityEffectActionDict(ArchiveDictMixin, DictClass[int, OpacityEffectAction]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(OpacityEffectAction)


class SongChannelStateDict(ArchiveDictMixin, DictClass[int, SongChannelState]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(SongChannelState)


class SongTriggerStateList(ArchiveListMixin, ListClass[SongTriggerState]):
    USE_STREAMS = True
    DECODER = staticmethod(SongTriggerState.from_tokens)
    ENCODER = staticmethod(SongTriggerState.to_tokens)


class SongTriggerStateListDict(ArchiveDictMixin, DictClass[int, SongTriggerStateList]):
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(SongTriggerStateList)


class FMODSoundTweenPairKeyDict(ArchiveDictMixin, DictClass[tuple[int, int], FMODSoundTween]):
    USE_STREAMS = True
    DECODER, ENCODER = int_pair_keyed(FMODSoundTween)


class SFXTriggerInstancePairKeyDict(ArchiveDictMixin, DictClass[tuple[int, int], SFXTriggerInstance]):
    USE_STREAMS = True
    DECODER, ENCODER = int_pair_keyed(SFXTriggerInstance)


class FMODQueuedMusicDict(ArchiveDictMixin, DictClass[int, FMODQueuedMusic]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(FMODQueuedMusic)


class FMODSoundStateDict(ArchiveDictMixin, DictClass[int, FMODSoundState]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(FMODSoundState)


class TimerItemDict(ArchiveDictMixin, DictClass[int, TimerItem]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(TimerItem)


class SequenceTriggerStateDict(ArchiveDictMixin, DictClass[int, SequenceTriggerState]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(SequenceTriggerState)


class EventTriggerInstanceList(ArchiveListMixin, ListClass[EventTriggerInstance]):
    USE_STREAMS = True
    DECODER = staticmethod(EventTriggerInstance.from_tokens)
    ENCODER = staticmethod(EventTriggerInstance.to_tokens)


class EventTriggerInstanceEventListDict(ArchiveDictMixin, DictClass[tuple[GameEvents, int], EventTriggerInstanceList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = event_keyed(EventTriggerInstanceList)


class EnterEffectInstanceList(ArchiveListMixin, ListClass[EnterEffectInstance]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(EnterEffectInstance.from_tokens)
    ENCODER = staticmethod(EnterEffectInstance.to_tokens)


class EnterEffectInstanceListDict(ArchiveDictMixin, DictClass[int, EnterEffectInstanceList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(EnterEffectInstanceList)


class AdvancedFollowInstanceList(ArchiveListMixin, ListClass[AdvancedFollowInstance]):
    USE_STREAMS = True
    DECODER = staticmethod(AdvancedFollowInstance.from_tokens)
    ENCODER = staticmethod(AdvancedFollowInstance.to_tokens)


class DynamicObjectActionList(ArchiveListMixin, ListClass[DynamicObjectAction]):
    USE_STREAMS = True
    DECODER = staticmethod(DynamicObjectAction.from_tokens)
    ENCODER = staticmethod(DynamicObjectAction.to_tokens)


class SFXTriggerStateList(ArchiveListMixin, ListClass[SFXTriggerState]):
    USE_STREAMS = True
    DECODER = staticmethod(SFXTriggerState.from_tokens)
    ENCODER = staticmethod(SFXTriggerState.to_tokens)


class CAStateList(ArchiveListMixin, ListClass[CAState]):
    USE_STREAMS = True
    DECODER = staticmethod(CAState.from_tokens)
    ENCODER = staticmethod(CAState.to_tokens)


class PulseEffectActionList(ArchiveListMixin, ListClass[PulseEffectAction]):
    USE_STREAMS = True
    DECODER = staticmethod(PulseEffectAction.from_tokens)
    ENCODER = staticmethod(PulseEffectAction.to_tokens)


class PulseEffectActionListDict(ArchiveDictMixin, DictClass[int, PulseEffectActionList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(PulseEffectActionList)


class CountTriggerActionList(ArchiveListMixin, ListClass[CountTriggerAction]):
    USE_STREAMS = True
    DECODER = staticmethod(CountTriggerAction.from_tokens)
    ENCODER = staticmethod(CountTriggerAction.to_tokens)


class CountTriggerActionListDict(ArchiveDictMixin, DictClass[int, CountTriggerActionList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(CountTriggerActionList)


class TimerTriggerActionList(ArchiveListMixin, ListClass[TimerTriggerAction]):
    USE_STREAMS = True
    DECODER = staticmethod(TimerTriggerAction.from_tokens)
    ENCODER = staticmethod(TimerTriggerAction.to_tokens)


class TimerTriggerActionListDict(ArchiveDictMixin, DictClass[int, TimerTriggerActionList]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER, ENCODER = int_keyed(TimerTriggerActionList)


class TouchToggleActionList(ArchiveListMixin, ListClass[TouchToggleAction]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(TouchToggleAction.from_tokens)
    ENCODER = staticmethod(TouchToggleAction.to_tokens)


class CollisionTriggerActionList(ArchiveListMixin, ListClass[CollisionTriggerAction]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(CollisionTriggerAction.from_tokens)
    ENCODER = staticmethod(CollisionTriggerAction.to_tokens)


class ToggleTriggerActionList(ArchiveListMixin, ListClass[ToggleTriggerAction]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(ToggleTriggerAction.from_tokens)
    ENCODER = staticmethod(ToggleTriggerAction.to_tokens)


class SpawnTriggerActionList(ArchiveListMixin, ListClass[SpawnTriggerAction]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(SpawnTriggerAction.from_tokens)
    ENCODER = staticmethod(SpawnTriggerAction.to_tokens)


class GroupCommandObject2List(ArchiveListMixin, ListClass[GroupCommandObject2]):
    SEPARATOR = ":"
    END_DELIMITER = ":"
    USE_STREAMS = True
    DECODER = staticmethod(GroupCommandObject2.from_tokens)
    ENCODER = staticmethod(GroupCommandObject2.to_tokens)


class SavedObjectStateRefList(ArchiveListMixin, ListClass[SavedObjectStateRef]):
    USE_STREAMS = True
    DECODER = staticmethod(SavedObjectStateRef.from_tokens)
    ENCODER = staticmethod(SavedObjectStateRef.to_tokens)


class SavedActiveObjectStateList(ArchiveListMixin, ListClass[SavedActiveObjectState]):
    USE_STREAMS = True
    DECODER = staticmethod(SavedActiveObjectState.from_tokens)
    ENCODER = staticmethod(SavedActiveObjectState.to_tokens)


class SavedSpecialObjectStateList(ArchiveListMixin, ListClass[SavedSpecialObjectState]):
    USE_STREAMS = True
    DECODER = staticmethod(SavedSpecialObjectState.from_tokens)
    ENCODER = staticmethod(SavedSpecialObjectState.to_tokens)


@dataclass_decoder(slots=True, separator=',')
class PlayerCheckpoint(ArchiveStruct):
    position: Position = inline(Position)
    last_position: Position = inline(Position)
    y_velocity_unrounded: float = 0.0
    is_upside_down: bool = False
    is_sideways: bool = False
    is_ship: bool = False
    is_ball: bool = False
    is_bird: bool = False
    is_dart: bool = False
    is_robot: bool = False
    is_spider: bool = False
    is_swing: bool = False
    is_on_ground: bool = False
    ghost_type: int = 0
    is_mini: bool = False
    player_speed: float = 0.0
    is_hidden: bool = False
    is_going_left: bool = False
    reverse_sync_remaining: float = 0.0
    last_flip_time: float = 0.0
    gravity_mod: float = 0.0
    decrease_boost_slide: bool = False
    follow_sample_timer: float = 0.0
    follow_sample_index: int = 0
    player_follow_floats: ArchiveFloatList = nested(ArchiveFloatList)
    object_snapped_to: int = 0
    snap_distance: float = 0.0
    acceleration_or_speed: float = 0.0
    was_on_slope: bool = False
    is_on_slope: bool = False
    slope_velocity: float = 0.0
    is_dashing: bool = False
    dash_angle: float = 0.0
    dash_x: float = 0.0
    dash_y: float = 0.0
    dash_ring: int = 0
    dash_start_time: float = 0.0
    rotation: float = 0.0
    was_teleported: bool = False
    fix_gravity_bug: bool = False
    reverse_sync: bool = False
    y_velocity_before_slope: float = 0.0
    slope_start_time: float = 0.0
    just_placed_streak: bool = False
    last_collision_bottom: int = 0
    last_collision_top: int = 0
    last_collision_left: int = 0
    last_collision_right: int = 0
    prev_collision_bottom: int = 0
    prev_collision_top: int = 0
    ground_slope: int = 0
    pre_last_ground_object: int = 0
    slope_angle: float = 0.0
    slope_flipped: bool = False
    quick_checkpoint_mode: bool = False
    collided_object: int = 0
    last_ground_object: int = 0
    colliding_with_left: int = 0
    colliding_with_right: int = 0
    ground_x_delta: float = 0.0
    ground_y_delta: float = 0.0
    last_ground_y_delta: float = 0.0
    last_ground_x_delta: float = 0.0
    colliding_between_steps: bool = False
    wall_x_delta: float = 0.0
    last_wall_x_delta: float = 0.0
    is_colliding_with_slope: bool = False
    is_ball_rotating: bool = False
    no_potential_slope: bool = False
    current_potential_slope: int = 0
    current_slope: int = 0
    slope_center_offset: float = 0.0
    colliding_with_slope_id: int = 0
    slope_is_downhill: bool = False
    slope_angle_radians: float = 0.0
    rotation_speed: float = 0.0
    rotate_speed: float = 0.0
    is_rotating: bool = False
    ball_spinning: bool = False
    speed_multiplier: float = 0.0
    y_start: float = 0.0
    gravity: float = 0.0
    trailing_particle_life: float = 0.0
    game_mode_changed_time: float = 0.0
    ring_jumped_since_press: bool = False
    has_started_falling: bool = False
    should_try_placing_checkpoint: bool = False
    play_effects: bool = False
    landed_since_flip: bool = False
    last_spider_flip_time: float = 0.0
    unused_bool_7f8: bool = False
    used_ring_this_step: bool = False
    used_rings: ArchiveIntList = nested(ArchiveIntList)
    special_ground_hit: bool = False
    land_particles_angle: float = 0.0
    land_particles_gravity_y: float = 0.0
    slope_rotation: float = 0.0
    current_slope_y_velocity: float = 0.0
    last_slope_snap_y: float = 0.0
    last_slope_snap_offset: float = 0.0
    last_slope_snap_at_far_edge: bool = False
    last_slope_snap_at_near_edge: bool = False
    is_accelerating: bool = False
    is_current_slope_top: bool = False
    collided_top_min_y: float = 0.0
    collided_bottom_max_y: float = 0.0
    collided_left_max_x: float = 0.0
    collided_right_min_x: float = 0.0
    was_jump_buffered: bool = False
    was_robot_jump: bool = False
    jump_held_at_press: bool = False
    press_unused_at_press: bool = False
    touched_ring: bool = False
    touched_custom_ring: bool = False
    touched_gravity_portal: bool = False
    broke_block_since_press: bool = False
    touched_pad: bool = False
    y_velocity: float = 0.0
    fall_speed: float = 0.0
    slope_resnapped: bool = False
    reverse_cooldown: int = 0
    reverse_sync_step: float = 0.0
    ball_roll_speed: float = 0.0
    ship_rotation: Position = inline(Position)
    last_portal_pos: Position = inline(Position)
    unused_float_9c0: float = 0.0
    touching_ground: bool = False
    last_land_time: float = 0.0
    deceleration_ramp: float = 0.0
    is_rising: bool = False
    last_ground_x_delta_time: float = 0.0
    is_locked: bool = False
    controls_disabled: bool = False
    last_grounded_pos: Position = inline(Position)
    touching_rings: ObjectIDList = nested(ObjectIDList)
    touched_rings: ArchiveIntList = nested(ArchiveIntList)
    last_activated_portal: int = 0
    total_time: float = 0.0
    diagonal_y_step: float = 0.0
    default_mini_icon: bool = False
    swap_colors: bool = False
    switch_dash_fire_color: bool = False
    state_on_ground: int = 0
    unused_float_a80: float = 0.0
    state_boost_x: int = 0
    state_boost_y: int = 0
    state_no_wall_push: int = 0
    state_scale: int = 0
    platformer_x_velocity: float = 0.0
    holding_right: bool = False
    holding_left: bool = False
    left_pressed_first: bool = False
    platform_x_move: float = 0.0
    has_platform_momentum: bool = False
    platform_momentum: float = 0.0
    forced_slope_slide: bool = False
    is_sliding: bool = False
    slope_speed_bonus: float = 0.0
    is_on_ice: bool = False
    platform_ride_time: float = 0.0
    was_touching_ground: bool = False
    slope_jump_count: int = 0
    slope_jump_reset_time: float = 0.0
    changed_directions_time: float = 0.0
    slope_end_time: float = 0.0
    is_moving: bool = False
    forced_slide_left: bool = False
    forced_slide_right: bool = False
    last_slide_left: bool = False
    slide_slope_angle: float = 0.0
    unused_float_b08: float = 0.0
    state_no_auto_jump: int = 0
    state_dart_slide: int = 0
    state_hit_head: int = 0
    state_flip_gravity: int = 0
    state_force: int = 0
    state_force_vector: Position = inline(Position)
    affected_by_forces: bool = False
    touched_force_ids: ArchiveBoolDict = nested(ArchiveBoolDict)
    fall_start_y: float = 0.0
    platformer_checkpoint: bool = False


@dataclass_decoder(slots=True, separator=',')
class GJGameState(ArchiveStruct):
    camera_zoom: float = 0.0
    target_camera_zoom: float = 0.0
    camera_offset: Position = inline(Position)
    camera_offset_target: Position = inline(Position)
    last_camera_target: Position = inline(Position)
    last_camera_offset: Position = inline(Position)
    camera_velocity: Position = inline(Position)
    static_camera_start: Position = inline(Position)
    static_camera_position: Position = inline(Position)
    static_camera_target: Position = inline(Position)
    static_exit_offset: Position = inline(Position)
    applied_static_exit_offset: Position = inline(Position)
    static_start_velocity: Position = inline(Position)
    static_camera_duration: Position = inline(Position)
    static_transition_progress: Position = inline(Position)
    last_static_transition_progress: Position = inline(Position)
    static_follow_easing: Position = inline(Position)
    static_follow: Position = inline(Position)
    static_follow_group: Position = inline(Position)
    static_camera_active: Position = inline(Position)
    static_exit_pending: Position = inline(Position)
    static_exit_duration: Position = inline(Position)
    static_exit_easing_rate: Position = inline(Position)
    static_exit_easing: Position = inline(Position)
    static_smooth_velocity: Position = inline(Position)
    static_smooth_velocity_mod: Position = inline(Position)
    static_exit_start_offset: Position = inline(Position)
    unused_point25: Position = inline(Position)
    internal_camera_offset: Position = inline(Position)
    internal_camera_offset_target: Position = inline(Position)
    last_internal_camera_offset_target: Position = inline(Position)
    unused_point29: Position = inline(Position)
    dual_static_camera: bool = False
    gameplay_offset_x: int = 0
    gameplay_offset_x_dont_zoom: bool = False
    gameplay_offset_y: int = 0
    gameplay_offset_y_dont_zoom: bool = False
    snap_internal_camera_offset: Position = inline(Position)
    middle_ground_offset_y: float = 0.0
    middle_ground_offset_y_target: float = 0.0
    middle_ground_offset_y_duration: float = 0.0
    camera_move_x_active: bool = False
    camera_move_y_active: bool = False
    camera_padding: float = 0.0
    camera_easing: float = 0.0
    unused_float5: float = 0.0
    unused_float6: float = 0.0
    unused_float7: float = 0.0
    unused_float8: float = 0.0
    unused_float9: float = 0.0
    fly_camera_y: float = 0.0
    last_mode_height: float = 0.0
    last_camera_zoom: float = 0.0
    zoom_duration: float = 0.0
    portal_y: float = 0.0
    portal_y_during_zoom: bool = False
    camera_center_y: float = 0.0
    camera_move_y_target: float = 0.0
    fly_camera_target_y: float = 0.0
    unused_float15: float = 0.0
    fly_ground_active: bool = False
    is_free_mode: bool = False
    disable_camera_grid_snap: bool = False
    background_speed_x: float = 0.0
    background_speed_y: float = 0.0
    middleground_speed_x: float = 0.0
    middleground_speed_y: float = 0.0
    camera_angle: float = 0.0
    target_camera_angle: float = 0.0
    player_streak_blend: bool = False
    time_warp: float = 0.0
    queued_time_warp: float = 0.0
    requested_time_warp: float = 0.0
    current_channel: int = 0
    rotate_channel: int = 0
    spawn_channel_index: ArchiveItemDict = nested(ArchiveItemDict)
    spawn_channel_reversed: ArchiveBoolDict = nested(ArchiveBoolDict)
    total_time: float = 0.0
    level_time: float = 0.0
    unwarped_total_time: float = 0.0
    command_index: int = 0
    unused_int3: int = 0
    current_progress: int = 0
    step_command_index: int = 0
    position_history_time: int = 0
    position_history_clock: int = 0
    area_effect_counter: int = 0
    advanced_follow_counter: int = 0
    last_activated_portal1: int = 0
    last_activated_portal2: int = 0
    camera_position: Position = inline(Position)
    is_flipped: bool = False
    level_flip_progress: float = 0.0
    in_second_half_of_flip_animation: bool = False
    is_flipping: bool = False
    is_dual_mode: bool = False
    dual_animation_progress: float = 0.0
    tween_actions: GJValueTweenDict = nested(GJValueTweenDict)
    camera_edge_value0: int = 0
    camera_edge_value1: int = 0
    camera_edge_value2: int = 0
    camera_edge_value3: int = 0
    game_object_physics: GameObjectPhysicsDict = nested(GameObjectPhysicsDict)
    position_history: ArchiveFloatList = nested(ArchiveFloatList)
    unused_int10: int = 0
    position_history_index: int = 0
    camera_history_slot: int = 0
    camera_step_diff: Position = inline(Position)
    background_width: float = 0.0
    queued_time_mod: float = 0.0
    queued_time_mod_flag: bool = False
    activated_object_ids: IntPairKeyDict = nested(IntPairKeyDict)
    teleport_camera_ease_timer: float = 0.0
    last_camera_ease: Position = inline(Position)
    camera_last_position: Position = inline(Position)
    last_player_sideways: bool = False
    last_player_going_left: bool = False
    audio_on_death: bool = False
    respawn_time: float = 0.0
    no_death_sfx: bool = False
    camera_shake_enabled: bool = False
    camera_shake_duration: float = 0.0
    camera_shake_strength: float = 0.0
    camera_shake_interval: float = 0.0
    last_shake_time: float = 0.0
    camera_shake_offset: Position = inline(Position)
    ground_mode: int = 0
    state_objects: ObjectIDDict = nested(ObjectIDDict)
    game_event_triggers: EventTriggerInstanceEventListDict = nested(EventTriggerInstanceEventListDict)
    game_event_counts: EventCountDict = nested(EventCountDict)
    enter_effect_instance_vectors: EnterEffectInstanceListDict = nested(EnterEffectInstanceListDict)
    exit_effect_instance_vectors: EnterEffectInstanceListDict = nested(EnterEffectInstanceListDict)
    enter_channel_map: ArchiveIntList = nested(ArchiveIntList)
    exit_channel_map: ArchiveIntList = nested(ArchiveIntList)
    move_effect_instances: EnterEffectInstanceList = nested(EnterEffectInstanceList)
    rotate_effect_instances: EnterEffectInstanceList = nested(EnterEffectInstanceList)
    scale_effect_instances: EnterEffectInstanceList = nested(EnterEffectInstanceList)
    fade_effect_instances: EnterEffectInstanceList = nested(EnterEffectInstanceList)
    tint_effect_instances: EnterEffectInstanceList = nested(EnterEffectInstanceList)
    unsorted_area_effects: ArchiveIntList = nested(ArchiveIntList)
    advanced_follow_needs_sort: bool = False
    advance_follow_instances: AdvancedFollowInstanceList = nested(AdvancedFollowInstanceList)
    dynamic_move_actions: DynamicObjectActionList = nested(DynamicObjectActionList)
    dynamic_rotate_actions: DynamicObjectActionList = nested(DynamicObjectActionList)
    instant_exit_static_camera_x: bool = False
    instant_exit_static_camera_y: bool = False
    max_portal_y: float = 0.0
    sfx_trigger_channels: IntListDict = nested(IntListDict)
    proximity_volume_effects: SFXTriggerInstancePairKeyDict = nested(SFXTriggerInstancePairKeyDict)
    song_channel_states: SongChannelStateDict = nested(SongChannelStateDict)
    song_trigger_state_vectors: SongTriggerStateListDict = nested(SongTriggerStateListDict)
    sfx_trigger_states: SFXTriggerStateList = nested(SFXTriggerStateList)
    main_song_stopped: bool = False
    background: int = 0
    ground: int = 0
    middleground: int = 0
    unlink_dual_gravity: bool = False
    points: int = 0
    has_obtained_points: bool = False
    pause_counter: int = 0
    pause_buffer_timer: int = 0


@dataclass_decoder(slots=True, separator=',')
class GJShaderState(ArchiveStruct):
    tween_actions: GJValueTweenDict = nested(GJValueTweenDict)
    tween_times: ArchiveFloatDict = nested(ArchiveFloatDict)
    time: float = 0.0
    prev_time: float = 0.0
    start_time: float = 0.0
    texture_scale_x: float = 0.0
    texture_scale_y: float = 0.0
    blur_ref_color: Color = inline(Color)
    blur_intensity: float = 0.0
    blur_ref_channel: int = 0
    blur_only_empty: bool = False
    shock_wave_start_time: float = 0.0
    shock_wave_time: float = 0.0
    shock_wave_time_offset: float = 0.0
    shock_wave_speed: float = 0.0
    shock_wave_thickness: float = 0.0
    shock_wave_strength: float = 0.0
    shock_wave_width: float = 0.0
    shock_wave_fade_in: float = 0.0
    shock_wave_fade_out: float = 0.0
    shock_wave_invert: bool = False
    shock_wave_inner: float = 0.0
    shock_wave_outer: float = 0.0
    shock_wave_target_id: int = 0
    shock_wave_target: bool = False
    shock_wave_center_moving: bool = False
    shock_wave_relative: bool = False
    shock_wave_max_size: float = 0.0
    shock_wave_screen_offset: Position = inline(Position)
    shock_wave_center_dirty: bool = False
    shock_wave_center: Position = inline(Position)
    shock_line_start_time: float = 0.0
    shock_line_time: float = 0.0
    shock_line_time_offset: float = 0.0
    shock_line_speed: float = 0.0
    shock_line_axis: bool = False
    shock_line_direction: bool = False
    shock_line_dual: bool = False
    shock_line_invert: bool = False
    shock_line_screen_offset: float = 0.0
    shock_line_strength: float = 0.0
    shock_line_width: float = 0.0
    shock_line_fade_in: float = 0.0
    shock_line_fade_out: float = 0.0
    shock_line_thickness: float = 0.0
    shock_line_target_id: int = 0
    shock_line_target: bool = False
    shock_line_center_moving: bool = False
    shock_line_relative: bool = False
    shock_line_max_size: float = 0.0
    shock_line_unused_offset: Position = inline(Position)
    shock_line_center_dirty: bool = False
    shock_line_center: Position = inline(Position)
    glitch_strength: float = 0.0
    glitch_speed: float = 0.0
    glitch_slice_height: float = 0.0
    glitch_max_slice_x_off: float = 0.0
    glitch_max_col_x_off: float = 0.0
    glitch_max_col_y_off: float = 0.0
    glitch_relative: bool = False
    chromatic_target_x: float = 0.0
    chromatic_target_y: float = 0.0
    chromatic_relative: bool = False
    cg_start_time: float = 0.0
    cg_time: float = 0.0
    cg_speed: float = 0.0
    cg_rgb_offset: float = 0.0
    cg_strength: float = 0.0
    cg_segment_height: float = 0.0
    cg_line_thickness: float = 0.0
    cg_line_strength: float = 0.0
    cg_enable: bool = False
    cg_active: bool = False
    cg_relative: bool = False
    cg_relative_pos: bool = False
    pixelate_target_x: float = 0.0
    pixelate_target_y: float = 0.0
    pixelate_snap_grid: bool = False
    pixelate_pixelating: bool = False
    pixelate_relative: bool = False
    pixelate_hard_edges: bool = False
    lens_circle_size: float = 0.0
    lens_circle_fade: float = 0.0
    lens_circle_strength: float = 0.0
    lens_circle_target_id: int = 0
    lens_circle_tint_channel: int = 0
    lens_circle_relative: bool = False
    lens_circle_additive: bool = False
    lens_circle_tint: Color = inline(Color)
    lens_circle_center: Position = inline(Position)
    lens_circle_screen_offset: Position = inline(Position)
    radial_blur_size: float = 0.0
    radial_blur_fade: float = 0.0
    radial_blur_target: bool = False
    radial_blur_target_id: int = 0
    radial_blur_center: Position = inline(Position)
    radial_blur_screen_offset: Position = inline(Position)
    motion_blur_target_x: float = 0.0
    motion_blur_target_y: float = 0.0
    motion_blur_speed_x: float = 0.0
    motion_blur_speed_y: float = 0.0
    motion_blur_follow_ease_x: float = 0.0
    motion_blur_follow_ease_y: float = 0.0
    motion_blur_target_idx: int = 0
    motion_blur_target_idy: int = 0
    motion_blur_dual: bool = False
    motion_blur_relative: bool = False
    bulge_value: float = 0.0
    bulge_relative: bool = False
    bulge_target_id: int = 0
    bulge_radius: float = 0.0
    bulge_center: Position = inline(Position)
    bulge_screen_offset: Position = inline(Position)
    pinch_target_x: float = 0.0
    pinch_target_y: float = 0.0
    pinch_target_enabled_x: bool = False
    pinch_target_enabled_y: bool = False
    pinch_target_idx: int = 0
    pinch_target_idy: int = 0
    pinch_center: Position = inline(Position)
    pinch_screen_offset: Position = inline(Position)
    pinch_relative: bool = False
    pinch_radius: float = 0.0
    pinch_modifier: Position = inline(Position)
    grayscale_value: float = 0.0
    grayscale_use_lum: bool = False
    grayscale_tint_channel: int = 0
    grayscale_tint: Color = inline(Color)
    sepia_value: float = 0.0
    invert_color_edit_rgb: float = 0.0
    invert_color_r: float = 0.0
    invert_color_g: float = 0.0
    invert_color_b: float = 0.0
    invert_color_clamp_rgb: bool = False
    hue_shift_degrees: float = 0.0
    color_change_cr: float = 0.0
    color_change_cg: float = 0.0
    color_change_cb: float = 0.0
    color_change_br: float = 0.0
    color_change_bg: float = 0.0
    color_change_bb: float = 0.0
    split_target_rows: float = 0.0
    split_target_cols: float = 0.0
    split_active: bool = False
    min_blending_layer: int = 0
    max_blending_layer: int = 0
    z_layer_dirty: bool = False
    no_player_particles: bool = False
    uses_shaders: bool = False


@dataclass_decoder(slots=True, separator=',')
class FMODAudioState(ArchiveStruct):
    interval: float = 0.0
    elapsed: float = 0.0
    tweens_for_effect_channels: FMODSoundTweenPairKeyDict = nested(FMODSoundTweenPairKeyDict)
    tweens_for_effect_groups: FMODSoundTweenPairKeyDict = nested(FMODSoundTweenPairKeyDict)
    tweens_for_music_channels: FMODSoundTweenPairKeyDict = nested(FMODSoundTweenPairKeyDict)
    volume_for_effect_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    volume_mod_for_effect_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    pitch_for_effect_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    volume_for_effect_groups: ArchiveFloatDict = nested(ArchiveFloatDict)
    volume_mod_for_effect_groups: ArchiveFloatDict = nested(ArchiveFloatDict)
    pitch_for_effect_groups: ArchiveFloatDict = nested(ArchiveFloatDict)
    volume_for_music_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    volume_mod_for_music_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    pitch_for_music_channels: ArchiveFloatDict = nested(ArchiveFloatDict)
    interval_for_effects: ArchiveFloatDict = nested(ArchiveFloatDict)
    queued_music_for_channels1: FMODQueuedMusicDict = nested(FMODQueuedMusicDict)
    queued_music_for_channels2: FMODQueuedMusicDict = nested(FMODQueuedMusicDict)
    sound_state_for_channels: FMODSoundStateDict = nested(FMODSoundStateDict)
    unused_u64: int = 0


@dataclass_decoder(slots=True, separator=',')
class EffectManagerState(ArchiveStruct):
    color_actions: CAStateList = nested(CAStateList)
    pulse_actions: PulseEffectActionList = nested(PulseEffectActionList)
    pulse_actions_by_group: PulseEffectActionListDict = nested(PulseEffectActionListDict)
    count_actions: CountTriggerActionListDict = nested(CountTriggerActionListDict)
    disabled_groups: ArchiveIntList = nested(ArchiveIntList)
    triggered_ids: ArchiveIntPairList = nested(ArchiveIntPairList)
    opacity_actions: OpacityEffectActionDict = nested(OpacityEffectActionDict)
    touch_actions: TouchToggleActionList = nested(TouchToggleActionList)
    collision_actions: CollisionTriggerActionList = nested(CollisionTriggerActionList)
    toggle_actions: ToggleTriggerActionList = nested(ToggleTriggerActionList)
    spawn_actions: SpawnTriggerActionList = nested(SpawnTriggerActionList)
    item_counts: ArchiveItemDict = nested(ArchiveItemDict)
    collision_states: ArchiveBoolDict = nested(ArchiveBoolDict)
    group_commands: GroupCommandObject2List = nested(GroupCommandObject2List)
    completed_move_offsets: DoublePairDict = nested(DoublePairDict)
    following_keys: ArchiveIntList = nested(ArchiveIntList)
    timer_items: TimerItemDict = nested(TimerItemDict)
    timer_actions: TimerTriggerActionListDict = nested(TimerTriggerActionListDict)
    platformer_progress: int = 0


@dataclass_decoder(slots=True, separator=',')
class SequenceSection(ArchiveStruct):
    states: SequenceTriggerStateDict = nested(SequenceTriggerStateDict)


@dataclass_decoder(slots=True, separator=',')
class GradientSection(ArchiveStruct):
    objects: ObjectIDList = nested(ObjectIDList)


@dataclass_decoder(slots=True, separator=',')
class DynamicSection(ArchiveStruct):
    objects: SavedObjectStateRefList = inline(SavedObjectStateRefList)


@dataclass_decoder(slots=True, separator=',')
class ActiveSection(ArchiveStruct):
    active: SavedActiveObjectStateList = inline(SavedActiveObjectStateList)
    special: SavedSpecialObjectStateList = inline(SavedSpecialObjectStateList)


def _read_player2(stream: TokenStream) -> Optional[PlayerCheckpoint]:
    if stream.pop() in ("", "0"):
        return None
    return PlayerCheckpoint.from_string(stream.pop())


def _write_player2(value: Optional[PlayerCheckpoint], out: list):
    if value is None:
        out.append("0")
    else:
        out += ("1", value.to_string())


@dataclass_decoder(slots=True, separator="~")
class PlatformerCheckpoint(CompressFileMixin, ArchiveStruct):
    END_DELIMITER = "~"


    COMPRESSED = True
    COMPRESSION = "gzip"

    player1: PlayerCheckpoint = nested(PlayerCheckpoint)
    player2: Optional[PlayerCheckpoint] = field_decoder(
        default=None, use_streams=True, decoder=_read_player2, encoder=_write_player2)
    game_state: GJGameState = nested(GJGameState)
    command_index: int = 0
    shader_state: GJShaderState = nested(GJShaderState)
    audio_state: FMODAudioState = nested(FMODAudioState)
    sequence_triggers: SequenceSection = nested(SequenceSection)
    ground2_invisible: bool = False
    effect_manager: EffectManagerState = nested(EffectManagerState)
    gradients: GradientSection = nested(GradientSection)
    dynamic_objects: DynamicSection = nested(DynamicSection)
    active_objects: ActiveSection = nested(ActiveSection)
    unique_id: int = 0
    respawn_id: int = 0
    attempts: int = 0
    attempt_time: float = 0.0
    longest_attempt_time: float = 0.0
    attempt_clicks: int = 0
    play_timer: float = 0.0
    record_ticks: int = 0
    record_clicks: int = 0
    jumps: int = 0
    persistent_items: ArchiveItemDict = nested(ArchiveItemDict)
    persistent_timers: ArchiveIntList = nested(ArchiveIntList)
    persistent_timer_states: Optional[TimerItemDict] = nested(TimerItemDict, default=None, optional=True)
    extra_tokens: list[str] = rest()

    @classmethod
    def from_text(cls, string: str, **kwargs) -> "PlatformerCheckpoint":
        return cls.from_string(string, compressed=False, **kwargs)

    def to_text(self, **kwargs) -> str:
        return self.to_string(compressed=False, **kwargs)


class PlatformerCheckpointLazy(LazyString):
    PARSER = PlatformerCheckpoint