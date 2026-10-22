# Package Imports
from gmdkit.models.level import LevelMapping
from gmdkit.models.level_pack import LevelPackList
from gmdkit.models.template import SmartTemplateList
from gmdkit.models.object import ObjectGroupDict
from gmdkit.models.prop.dpad import (
    MoveButton, JumpButton,
    SingleLayout, DualLayout
)
from gmdkit.models.prop.audio_info import SongInfoList, RecentSFXList, UseCountDict
from gmdkit.models.custom_sfx import CustomSFXLibrary
from gmdkit.serialization.classes import DictField, FieldMetaclass
from gmdkit.serialization.mixins import PlistLoaderMixin
from gmdkit.models.prop.loaders import (
    StrBoolDict, IntBoolDict, IntStrDict, IntIntDict, StrIntDict, node_field
)
from gmdkit.models.prop.likes import LikeList
from gmdkit.models.prop.rewards import RewardItemDict, IntRewardItemDict, ChallengeDict
from gmdkit.models.prop.value_keepers import (
    ValueKeeper, UnlockValueKeeper, LocalKeeper, SearchFilters,
    PlayerStats, SpecialChests, ReportedAchievements
)
from gmdkit.models.prop.list import StrList, IntList
from gmdkit.models.keybinds import KeybindDict
from gmdkit.models.prop.editor_sfx import EditorSFXString
from gmdkit.utils import enums


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):
    HAS_NODES = True

    username: str = DictField(key="GJA_001")

    account_id: int = DictField(key="GJA_003")

    password_gjp2: str = DictField(key="GJA_005")

    keybinds: KeybindDict = DictField(
        key="GJKB_Binds",
        default_factory=KeybindDict,
        decoder=KeybindDict.from_string,
        encoder=KeybindDict.to_string,
    )

    keybinds_version: int = DictField(key="GJKB_Version", default=2)

    official_levels: LevelMapping = DictField(
        key="GLM_01",
        default_factory=LevelMapping,
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
    )

    online_levels: LevelMapping = DictField(
        key="GLM_03",
        default_factory=LevelMapping,
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
    )

    followed_accounts: IntBoolDict = DictField(
        key="GLM_06",
        default_factory=IntBoolDict,
        decoder=IntBoolDict.from_node,
        encoder=IntBoolDict.to_node,
        is_node=True,
    )

    last_sessions_levels: IntBoolDict = DictField(
        key="GLM_07",
        default_factory=IntBoolDict,
        decoder=IntBoolDict.from_node,
        encoder=IntBoolDict.to_node,
        is_node=True,
    )

    search_filters: SearchFilters = node_field("GLM_09", SearchFilters)

    timely_levels: LevelMapping = DictField(
        key="GLM_10",
        default_factory=LevelMapping,
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
    )

    daily_level_id: int = DictField(key="GLM_11")

    liked_items: LikeList = node_field("GLM_12", LikeList)

    rated_levels: IntBoolDict = DictField(
        key="GLM_13",
        default_factory=IntBoolDict,
        decoder=IntBoolDict.from_node,
        encoder=IntBoolDict.to_node,
        is_node=True,
    )

    reported_levels: IntBoolDict = DictField(
        key="GLM_14",
        default_factory=IntBoolDict,
        decoder=IntBoolDict.from_node,
        encoder=IntBoolDict.to_node,
        is_node=True,
    )

    rated_demons: IntBoolDict = DictField(
        key="GLM_15",
        default_factory=IntBoolDict,
        decoder=IntBoolDict.from_node,
        encoder=IntBoolDict.to_node,
        is_node=True,
    )

    gauntlet_levels: LevelMapping = DictField(
        key="GLM_16",
        default_factory=LevelMapping,
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
    )

    weekly_level_id: int = DictField(key="GLM_17")

    online_folder_names: IntStrDict = DictField(
        key="GLM_18",
        default_factory=IntStrDict,
        decoder=IntStrDict.from_node,
        encoder=IntStrDict.to_node,
        is_node=True,
    )

    offline_folder_names: IntStrDict = DictField(
        key="GLM_19",
        default_factory=IntStrDict,
        decoder=IntStrDict.from_node,
        encoder=IntStrDict.to_node,
        is_node=True,
    )

    smart_templates: SmartTemplateList = DictField(
        key="GLM_20",
        default_factory=SmartTemplateList,
        decoder=SmartTemplateList.from_node,
        encoder=SmartTemplateList.to_node,
        is_node=True,
    )

    favorite_lists: LevelPackList = DictField(
        key="GLM_22",
        default_factory=LevelPackList,
        decoder=LevelPackList.from_node,
        encoder=LevelPackList.to_node,
        is_node=True,
    )

    event_level_id: int = DictField(key="GLM_23")

    latest_daily_id: int = DictField(key="GLM_24")

    latest_weekly_id: int = DictField(key="GLM_25")

    latest_event_id: int = DictField(key="GLM_26")

    latest_gauntlet_count: int = DictField(key="GLM_27")

    latest_ids_initialized: bool = DictField(key="GLM_28", default=False)

    verified_user_coins: StrBoolDict = node_field("GS_3", StrBoolDict)

    pending_user_coins: StrBoolDict = node_field("GS_4", StrBoolDict)

    map_pack_stars: StrIntDict = node_field("GS_5", StrIntDict)

    purchased_items: IntIntDict = node_field("GS_6", IntIntDict)

    online_orb_percent: IntIntDict = node_field("GS_7", IntIntDict)

    unk_gs_8: StrIntDict = node_field("GS_8", StrIntDict)

    online_orb_stars: IntIntDict = node_field("GS_9", IntIntDict)

    official_orb_percent: IntIntDict = node_field("GS_10", IntIntDict)

    daily_chest_rewards: RewardItemDict = node_field("GS_11", RewardItemDict)

    quests: ChallengeDict = node_field("GS_12", ChallengeDict)

    challenge_rewards: StrIntDict = node_field("GS_14", StrIntDict)

    upcoming_quests: ChallengeDict = node_field("GS_15", ChallengeDict)

    timely_orb_percent: IntIntDict = node_field("GS_16", IntIntDict)

    timely_orb_stars: IntIntDict = node_field("GS_17", IntIntDict)

    diamond_percent: IntIntDict = node_field("GS_18", IntIntDict)

    treasure_room_rewards: IntRewardItemDict = node_field("GS_19", IntRewardItemDict)

    demon_keys: int = DictField(key="GS_20", default=0)

    special_chests: SpecialChests = node_field("GS_21", SpecialChests)

    gd_world_rewards: StrIntDict = node_field("GS_22", StrIntDict)

    gauntlet_orb_percent: IntIntDict = node_field("GS_23", IntIntDict)

    timely_diamond_percent: IntIntDict = node_field("GS_24", IntIntDict)

    weekly_demon_rewards: RewardItemDict = node_field("GS_25", RewardItemDict)

    active_path: int = DictField(key="GS_26", default=0)

    list_rewards: StrIntDict = node_field("GS_27", StrIntDict)

    enabled_animations: StrBoolDict = node_field("GS_28", StrBoolDict)

    path_fix: bool = DictField(key="GS_29", default=False)

    secret_room_rewards: StrBoolDict = node_field("GS_30", StrBoolDict)

    event_level_chest_rewards: RewardItemDict = node_field("GS_31", RewardItemDict)

    unlocked_gauntlets: StrBoolDict = node_field("GS_32", StrBoolDict)

    daily_recall_unlocks: IntIntDict = node_field("GS_33", IntIntDict)

    completed_levels: StrBoolDict = node_field("GS_completed", StrBoolDict)

    player_stats: PlayerStats = node_field("GS_value", PlayerStats)

    song_info: SongInfoList = DictField(
        key="MDLM_001",
        default_factory=SongInfoList,
        decoder=SongInfoList.from_node,
        encoder=SongInfoList.to_node,
        is_node=True,
    )

    song_priority: int = DictField(key="MDLM_002")

    unk_mdlm_003: dict = DictField(
        key="MDLM_003",
        default_factory=dict,
        is_node=True,
    )

    favorite_sfx: IntList = DictField(
        key="MDLM_004",
        default_factory=IntList,
        decoder=IntList.from_string,
        encoder=IntList.to_string,
    )

    favorite_songs: IntList = DictField(
        key="MDLM_005",
        default_factory=IntList,
        decoder=IntList.from_string,
        encoder=IntList.to_string,
    )

    recent_sfx: RecentSFXList = DictField(
        key="MDLM_006",
        default_factory=RecentSFXList,
        decoder=RecentSFXList.from_string,
        encoder=RecentSFXList.to_string,
    )

    recent_songs: IntList = DictField(
        key="MDLM_007",
        default_factory=IntList,
        decoder=IntList.from_string,
        encoder=IntList.to_string,
    )

    sfx_use_counts: UseCountDict = DictField(
        key="MDLM_008",
        default_factory=UseCountDict,
        decoder=UseCountDict.from_string,
        encoder=UseCountDict.to_string,
    )

    song_use_counts: UseCountDict = DictField(
        key="MDLM_009",
        default_factory=UseCountDict,
        decoder=UseCountDict.from_string,
        encoder=UseCountDict.to_string,
    )

    custom_sfx_library: CustomSFXLibrary = DictField(
        key="MDLM_010",
        default_factory=CustomSFXLibrary,
        decoder=CustomSFXLibrary.from_string,
        encoder=CustomSFXLibrary.to_string,
    )

    favorite_custom_sfx: IntList = DictField(
        key="MDLM_011",
        default_factory=IntList,
        decoder=IntList.from_string,
        encoder=IntList.to_string,
    )

    bg_volume: float = DictField(key="bgVolume", default=1.0)

    binary: int = DictField(key="binaryVersion")

    bootups: int = DictField(key="bootups", default=0)

    opened_editor: bool = DictField(key="clickedEditor", default=False)

    opened_icon_selector: bool = DictField(key="clickedGarage", default=False)

    opened_name: bool = DictField(key="clickedName", default=False)

    opened_practice: bool = DictField(key="clickedPractice", default=False)

    custom_fps: float = DictField(key="customFPSTarget", default=0)

    custom_menu_song_id: int = DictField(key="customMenuSongID", default=0)

    custom_objects: ObjectGroupDict = DictField(
        key="customObjectDict",
        default_factory=ObjectGroupDict,
        decoder=ObjectGroupDict.from_node,
        encoder=ObjectGroupDict.to_node,
        is_node=True,
    )

    custom_practice_song_id: int = DictField(key="customPracticeSongID", default=0)

    dpad_move_single: MoveButton = DictField(
        key="dpad01",
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_move_p1: MoveButton = DictField(
        key="dpad02",
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_move_p2: MoveButton = DictField(
        key="dpad03",
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_jump_p1: JumpButton = DictField(
        key="dpad04",
        decoder=JumpButton.from_string,
        encoder=JumpButton.to_string,
    )

    dpad_jump_p2: JumpButton = DictField(
        key="dpad05",
        decoder=JumpButton.from_string,
        encoder=JumpButton.to_string,
    )

    dpad_layout_1: SingleLayout = DictField(
        key="dpadLayout01",
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_layout_2: SingleLayout = DictField(
        key="dpadLayout02",
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_layout_3: SingleLayout = DictField(
        key="dpadLayout03",
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_dual_layout_1: DualLayout = DictField(
        key="dpadLayoutDual01",
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    dpad_dual_layout_2: DualLayout = DictField(
        key="dpadLayoutDual02",
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    dpad_dual_layout_3: DualLayout = DictField(
        key="dpadLayoutDual03",
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    editor_sfx: EditorSFXString = DictField(
        key="editorSFX",
        default_factory=EditorSFXString,
        decoder=EditorSFXString.from_string,
        encoder=EditorSFXString.to_string,
    )

    editor_sfx_favorite_count: int = DictField(key="editorSFXFavoriteCount", default=0)

    editor_sfx_volume: float = DictField(key="editorSFXGlobalVolume", default=1.0)

    editor_sfx_my_count: int = DictField(key="editorSFXMyCount", default=0)

    editor_sfx_next_local_id: int = DictField(key="editorSFXNextLocalID", default=0)

    editor_sfx_version: int = DictField(key="editorSFXVersion", default=1)

    has_leaderboard_privilege: bool = DictField(key="hasDRP", default=False)

    has_rating_privilege: enums.ModStatus = DictField(
        key="hasRP",
        decoder=enums.ModStatus,
        default=enums.ModStatus.NONE
    )

    rated_game: bool = DictField(key="hasRatedGame", default=False)

    id_name_sort_mode: int = DictField(key="idNameSortMode", default=0)

    local_keeper: LocalKeeper = node_field("localKeeper", LocalKeeper)

    news_last_read_id: int = DictField(key="newsLastReadID", default=0)

    performance_mode: bool = DictField(key="performanceMode", default=False)

    player_ball_icon: int = DictField(key="playerBall", default=1)

    player_ufo_icon: int = DictField(key="playerBird", default=1)

    player_color_1: int = DictField(key="playerColor", default=1)

    player_color_2: int = DictField(key="playerColor2", default=2)

    player_glow_color: int = DictField(key="playerColor3", default=-1)

    player_wave_icon: int = DictField(key="playerDart", default=1)

    player_death_effect: int = DictField(key="playerDeathEffect", default=1)

    player_cube_icon: int = DictField(key="playerFrame", default=1)

    player_uses_glow: bool = DictField(key="playerGlow", default=False)

    player_displayed_icon: enums.DisplayIcon = DictField(
        key="playerIconType",
        decoder=enums.DisplayIcon,
        default=enums.DisplayIcon.CUBE
    )

    player_jetpack_icon: int = DictField(key="playerJetpack", default=1)

    player_username: str = DictField(key="playerName")

    player_robot_icon: int = DictField(key="playerRobot", default=1)

    player_ship_icon: int = DictField(key="playerShip", default=1)

    player_ship_streak: int = DictField(key="playerShipStreak", default=1)

    player_spider_icon: int = DictField(key="playerSpider", default=1)

    player_streak: int = DictField(key="playerStreak", default=1)

    player_swing_icon: int = DictField(key="playerSwing", default=1)

    player_udid: str = DictField(key="playerUDID")

    player_user_id: int = DictField(key="playerUserID")

    practice_icon_opacity: float = DictField(key="practiceOpacity", default=1.0)

    practice_icon_x_pos: float = DictField(key="practicePosX", default=284.5)

    practice_icon_y_pos: float = DictField(key="practicePosY", default=40.0)

    recent_emotes: StrList = DictField(
        key="recentEmotes",
        default_factory=StrList,
        decoder=StrList.from_string,
        encoder=StrList.to_string,
    )

    record_gameplay: bool = DictField(key="recordGameplay", default=False)

    achievements: ReportedAchievements = node_field("reportedAchievements", ReportedAchievements)

    resolution: enums.Resolution = DictField(
        key="resolution",
        decoder=enums.Resolution,
        default=enums.Resolution.AUTO
    )

    scroll_sensitivity: float = DictField(key="scrollSensitivity")

    secret_number: int = DictField(key="secretNumber", default=0)

    sfx_volume: float = DictField(key="sfxVolume", default=1.0)

    show_bpm_markers: bool = DictField(key="showBPMMarkers", default=False)

    show_progress_bar: bool = DictField(key="showProgressBar", default=True)

    show_song_markers: bool = DictField(key="showSongMarkers", default=True)

    showed_editor_guide: bool = DictField(key="showedEditorGuide", default=False)

    showed_ldm_dialog: bool = DictField(key="showedLowDetailDialog", default=False)

    showed_diff_rate_dialog: bool = DictField(key="showedRateDiffDialog", default=False)

    showed_star_rate_dialog: bool = DictField(key="showedRateStarDialog", default=False)

    special_perm_key: int = DictField(key="specialPermKey")

    texture_quality: enums.TextureQuality = DictField(
        key="texQuality",
        decoder=enums.TextureQuality,
        default=enums.TextureQuality.AUTO
    )

    time_offset: int = DictField(key="timeOffset", default=0)

    unlock_value_keeper: UnlockValueKeeper = node_field("unlockValueKeeper", UnlockValueKeeper)

    value_keeper: ValueKeeper = node_field("valueKeeper", ValueKeeper)

    window_state_count: int = DictField(key="winStateCount", default=0)