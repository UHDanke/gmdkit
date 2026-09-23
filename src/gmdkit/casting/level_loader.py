# Package Imports
from gmdkit.utils import enums
from gmdkit.serialization.type_cast import decode_text, encode_text, get_string
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.pos_list import PositionList
from gmdkit.models.prop.gzip import ObjectString, ReplayString
from gmdkit.serialization.classes import DictField, FieldMetaclass
from gmdkit.serialization.mixins import PlistLoaderMixin


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):

    level_id: int = DictField(key="k1")

    name: str = DictField(key="k2", default="Unnamed")

    description: str = DictField(
        key="k3",
        decoder=decode_text,
        encoder=encode_text,
        default="",
    )

    object_string: ObjectString = DictField(
        key="k4",
        decoder=ObjectString,
        encoder=get_string,
        default_factory=ObjectString,
    )

    creator: str = DictField(key="k5")

    user_id: int = DictField(key="k6")

    official_difficulty: enums.LevelDifficulty = DictField(
        key="k7",
        decoder=enums.LevelDifficulty,
        default=enums.LevelDifficulty.NA,
    )

    official_song_id: enums.OfficialSongs = DictField(
        key="k8",
        decoder=enums.OfficialSongs,
        default=enums.OfficialSongs.STEREO_MADNESS,
    )

    rating: int = DictField(key="k9", default=0)

    rating_sum: enums.LevelRating = DictField(
        key="k10",
        decoder=enums.LevelRating,
        default=enums.LevelRating.NONE,
    )

    downloads: int = DictField(key="k11", default=0)

    editable: bool = DictField(key="k13", default=False)

    verified: bool = DictField(key="k14", default=False)

    uploaded: bool = DictField(key="k15", default=False)

    version: int = DictField(key="k16", default=0)

    game_version: int = DictField(key="k17")

    attempts: int = DictField(key="k18", default=0)

    normal_mode_best: int = DictField(key="k19", default=0)

    practice_mode_best: int = DictField(key="k20", default=0)

    list_type: enums.LevelType = DictField(
        key="k21",
        decoder=enums.LevelType,
        default=enums.LevelType.LOCAL,
    )

    like_rating: int = DictField(key="k22", default=0)

    length_type: enums.LevelLength = DictField(
        key="k23",
        decoder=enums.LevelLength,
        default=enums.LevelLength.TINY,
    )

    is_demon: bool = DictField(key="k25", default=False)

    stars: int = DictField(key="k26", default=0)

    feature_score: int = DictField(key="k27", default=0)

    is_auto: bool = DictField(key="k33", default=False)

    replay_data: ReplayString = DictField(
        key="k34",
        decoder=ReplayString,
        encoder=get_string,
        default_factory=ReplayString,
    )

    not_downloaded: bool = DictField(key="k35", default=False)

    jumps: int = DictField(key="k36", default=0)

    official_required_coins: int = DictField(key="k37", default=0)

    official_is_unlocked: bool = DictField(key="k38", default=False)

    password: str = DictField(key="k41")

    original_id: int = DictField(key="k42")

    two_player_mode: bool = DictField(key="k43", default=False)

    song_id: int = DictField(key="k45")

    revision: int = DictField(key="k46", default=0)

    modified: bool = DictField(key="k47", default=False)

    object_count: int = DictField(key="k48", default=0)

    binary_version: int = DictField(key="k50")

    account_id: int = DictField(key="k60")

    coin_1_verified: bool = DictField(key="k61", default=False)

    coin_2_verified: bool = DictField(key="k62", default=False)

    coin_3_verified: bool = DictField(key="k63", default=False)

    coins: int = DictField(key="k64", default=0)

    coins_verified: bool = DictField(key="k65", default=False)

    stars_requested: int = DictField(key="k66", default=0)

    capacity_string: str = DictField(key="k67")

    anticheat_triggered: bool = DictField(key="k68", default=False)

    bypass_high_objs: bool = DictField(key="k69", default=False)

    orb_percentage: int = DictField(key="k71", default=0)

    ldm: bool = DictField(key="k72", default=False)

    ldm_enabled: bool = DictField(key="k73", default=False)

    timely_id: int = DictField(key="k74")

    epic_rating: enums.EpicRating = DictField(
        key="k75",
        decoder=enums.EpicRating,
        default=enums.EpicRating.NONE,
    )

    demon_type: enums.DemonRating = DictField(
        key="k76",
        decoder=enums.DemonRating,
    )

    gauntlet: bool = DictField(key="k77", default=False)

    alt_game: bool = DictField(key="k78", default=False)

    unlisted: bool = DictField(key="k79", default=False)

    edit_time: int = DictField(key="k80", default=0)

    edit_time_copies: int = DictField(key="k81", default=0)

    favorite: bool = DictField(key="k82", default=False)

    index: int = DictField(key="k83")

    folder: int = DictField(key="k84", default=0)

    clicks_best: int = DictField(key="k85")

    time_best: int = DictField(key="k86")

    score_seed: int = DictField(key="k87")

    level_progress: IntList = DictField(
        key="k88",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    verified_check: bool = DictField(key="k89", default=False)

    leaderboard_percentage: int = DictField(key="k90")

    locked_layers: IntList = DictField(
        key="k91",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    bypass_unlimited_objs: bool = DictField(key="k93", default=False)

    friends_only: bool = DictField(key="k94", default=False)

    verification_time: int = DictField(key="k95", default=0)

    saved_camera_positions: PositionList = DictField(
        key="k101",
        decoder=PositionList.from_string,
        encoder=PositionList.to_string,
        default_factory=PositionList,
    )

    preview_lock_x: int = DictField(key="k102", default=0)

    preview_lock_y: int = DictField(key="k103", default=0)

    songs: IntList = DictField(
        key="k104",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    sfx: IntList = DictField(
        key="k105",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    best_time: int = DictField(key="k107")

    best_points: int = DictField(key="k108")

    local_best_time: IntList = DictField(
        key="k109",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    local_best_points: IntList = DictField(
        key="k110",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    platformer_seed: int = DictField(key="k111")

    shake_disabled: bool = DictField(key="k112", default=False)

    ticks_best_time: int = DictField(key="k115")

    ticks_best_points: int = DictField(key="k116")

    clicks_best_time: int = DictField(key="k117")

    clicks_best_points: int = DictField(key="k118")

    replay_best_time: ReplayString = DictField(
        key="k119",
        decoder=ReplayString,
        default_factory=ReplayString,
    )

    replay_best_points: ReplayString = DictField(
        key="k120",
        decoder=ReplayString,
        default_factory=ReplayString,
    )

    coins_best_time: int = DictField(key="k121")

    coins_best_points: int = DictField(key="k122")

    saved_best_time: bool = DictField(key="k123", default=False)

    saved_best_points: bool = DictField(key="k124", default=False)

    toggle_cbs: enums.ToggleCBS = DictField(
        key="k125",
        decoder=enums.ToggleCBS,
        default=enums.ToggleCBS.DEFAULT,
    )

    editor_camera_x: float = DictField(key="kI1", default=0.0)

    editor_camera_y: float = DictField(key="kI2", default=0.0)

    editor_camera_zoom: float = DictField(key="kI3", default=1.0)

    editor_build_tab_page: int = DictField(key="kI4", default=0)

    editor_build_tab: int = DictField(key="kI5", default=0)

    editor_build_tab_pages: dict = DictField(key="kI6", default_factory=dict, is_node=True)

    editor_layer: int = DictField(key="kI7", default=0)

FieldLoaderMixin.add_field(key="k24") # dislikes, unused
FieldLoaderMixin.add_field(key="k106") # unknown
