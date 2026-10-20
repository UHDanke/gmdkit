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
from gmdkit.models.prop.plist import (
    StrBoolDict, IntBoolDict,
    IntStrDict,
    PlistDict
)
from gmdkit.models.prop.likes import LikeDict
from gmdkit.models.prop.list import StrList, IntList
from gmdkit.models.keybinds import KeybindDict
from gmdkit.models.prop.editor_sfx import EditorSFXString
from gmdkit.utils import enums


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):
    HAS_NODES = True
    
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

    search_filters: StrBoolDict = DictField(
        key="GLM_08",
        decoder=StrBoolDict.from_node,
        encoder=StrBoolDict.to_node,
        is_node=True,
    )

    search_terms: PlistDict = DictField(
        key="GLM_09",
        is_node=True,
    )

    timely_levels: LevelMapping = DictField(
        key="GLM_10",
        default_factory=LevelMapping,
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
    )

    daily_level_id: int = DictField(key="GLM_11")

    liked_levels: LikeDict = DictField(
        key="GLM_12",
        default_factory=LikeDict,
        decoder=LikeDict.from_node,
        encoder=LikeDict.to_node,
        is_node=True,
    )
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

    song_info: SongInfoList = DictField(
        key="MDLM_001",
        default_factory=SongInfoList,
        decoder=SongInfoList.from_node,
        encoder=SongInfoList.to_node,
        is_node=True,
    )
    
    custom_sfx_library: CustomSFXLibrary = DictField(
        key="MDLM_010",
        default_factory=CustomSFXLibrary,
        decoder=CustomSFXLibrary.from_string,
        encoder=CustomSFXLibrary.to_string,
    )

    custom_objects: ObjectGroupDict = DictField(
        key="customObjectDict",
        default_factory=ObjectGroupDict,
        decoder=ObjectGroupDict.from_node,
        encoder=ObjectGroupDict.to_node,
        is_node=True,
    )

    dpad_move_single: str = DictField(
        key="dpad01",
        default_factory=MoveButton,
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_move_p1: str = DictField(
        key="dpad02",
        default_factory=MoveButton,
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_move_p2: str = DictField(
        key="dpad03",
        default_factory=MoveButton,
        decoder=MoveButton.from_string,
        encoder=MoveButton.to_string,
    )

    dpad_jump_p1: str = DictField(
        key="dpad04",
        default_factory=JumpButton,
        decoder=JumpButton.from_string,
        encoder=JumpButton.to_string,
    )

    dpad_jump_p2: str = DictField(
        key="dpad05",
        default_factory=JumpButton,
        decoder=JumpButton.from_string,
        encoder=JumpButton.to_string,
    )

    dpad_layout_1: str = DictField(
        key="dpadLayout01",
        default_factory=SingleLayout,
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_layout_2: str = DictField(
        key="dpadLayout02",
        default_factory=SingleLayout,
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_layout_3: str = DictField(
        key="dpadLayout03",
        default_factory=SingleLayout,
        decoder=SingleLayout.from_string,
        encoder=SingleLayout.to_string,
    )

    dpad_dual_layout_1: str = DictField(
        key="dpadLayoutDual01",
        default_factory=DualLayout,
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    dpad_dual_layout_2: str = DictField(
        key="dpadLayoutDual02",
        default_factory=DualLayout,
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    dpad_dual_layout_3: str = DictField(
        key="dpadLayoutDual03",
        default_factory=DualLayout,
        decoder=DualLayout.from_string,
        encoder=DualLayout.to_string,
    )

    achievements: dict = DictField(
        key="reportedAchievements",
        default_factory=dict,
        is_node=True
    )

    unlocked_items: dict = DictField(
        key="valueKeeper",
        default_factory=dict,
        is_node=True
    )

    unlockable_items: dict = DictField(
        key="unlockValueKeeper",
        default_factory=dict,
        is_node=True
    )

    bg_volume: float = DictField(key="bgVolume", default=1.0)

    binary: int = DictField(key="binaryVersion")

    bootups: int = DictField(key="bootups", default=0)

    opened_editor: bool = DictField(key="clickedEditor", default=False)

    opened_icon_selector: bool = DictField(key="clickedGarage", default=False)

    opened_practice: bool = DictField(key="clickedPractice", default=False)

    custom_fps: float = DictField(key="customFPSTarget", default=0)

    rated_game: bool = DictField(key="hasRatedGame", default=False)

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

    resolution: enums.Resolution = DictField(
        key="resolution",
        decoder=enums.Resolution,
        default=enums.Resolution.AUTO
    )

    secret_number: int = DictField(key="secretNumber", default=0)

    sfx_volume: float = DictField(key="sfxVolume", default=1.0)

    showed_editor_guide: bool = DictField(key="showedEditorGuide", default=False)

    showed_ldm_dialog: bool = DictField(key="showedLowDetailDialog", default=False)

    showed_star_rate_dialog: bool = DictField(key="showedRateStarDialog", default=False)

    has_rating_privilege: enums.ModStatus = DictField(
        key="hasRP",
        decoder=enums.ModStatus,
        default=enums.ModStatus.NONE
    )

    has_leaderboard_privilege: bool = DictField(key="hasDRP", default=False)

    show_song_markers: bool = DictField(key="showSongMarkers", default=True)

    show_progress_bar: bool = DictField(key="showProgressBar", default=True)

    performance_mode: bool = DictField(key="performanceMode", default=False)

    texture_quality: enums.TextureQuality = DictField(
        key="texQuality",
        decoder=enums.TextureQuality,
        default=enums.TextureQuality.AUTO
    )

    time_offset: int = DictField(key="timeOffset", default=0)

    custom_menu_song_id: int = DictField(key="customMenuSongID", default=0)

    custom_practice_song_id: int = DictField(key="customPracticeSongID", default=0)

    player_stats: dict = DictField(
        key="GS_value",
        default_factory=dict,
        is_node=True,
    )

    completed_levels: dict = DictField(
        key="GS_completed",
        default_factory=dict,
        is_node=True,
    )

    completed_levels_coins_1: dict = DictField(
        key="GS_3",
        default_factory=dict,
        is_node=True,
    )

    completed_levels_coins_2: dict = DictField(
        key="GS_4",
        default_factory=dict,
        is_node=True,
    )

    completed_mappacks: dict = DictField(
        key="GS_5",
        default_factory=dict,
        is_node=True,
    )

    purchased_items: dict = DictField(
        key="GS_6",
        default_factory=dict,
        is_node=True,
    )

    level_progress: dict = DictField(
        key="GS_7",
        default_factory=dict,
        is_node=True,
    )

    unk_gs_8: dict = DictField(
        key="GS_8",
        default_factory=dict,
        is_node=True,
    )

    downloaded_level_stars: dict = DictField(
        key="GS_9",
        default_factory=dict,
        is_node=True,
    )

    official_level_progress: dict = DictField(
        key="GS_10",
        default_factory=dict,
        is_node=True,
    )

    daily_chest_rewards: dict = DictField(
        key="GS_11",
        default_factory=dict,
        is_node=True,
    )

    quests: dict = DictField(
        key="GS_12",
        default_factory=dict,
        is_node=True,
    )

    challenge_rewards: dict = DictField(
        key="GS_14",
        default_factory=dict,
        is_node=True,
    )

    upcoming_quests: dict = DictField(
        key="GS_15",
        default_factory=dict,
        is_node=True,
    )

    timely_progress: dict = DictField(
        key="GS_16",
        default_factory=dict,
        is_node=True,
    )

    timely_stars: dict = DictField(
        key="GS_17",
        default_factory=dict,
        is_node=True,
    )

    gauntlet_level_progress: dict = DictField(
        key="GS_18",
        default_factory=dict,
        is_node=True,
    )

    treasure_room_rewards: dict = DictField(
        key="GS_19",
        default_factory=dict,
        is_node=True,
    )

    demon_keys: int = DictField(key="GS_20", default=0)

    gauntlet_completion_rewards: dict = DictField(
        key="GS_21",
        default_factory=dict,
        is_node=True,
    )

    gd_world_rewards: dict = DictField(
        key="GS_22",
        default_factory=dict,
        is_node=True,
    )

    gauntlet_level_progress_2: dict = DictField(
        key="GS_23",
        default_factory=dict,
        is_node=True,
    )

    timely_percentage: dict = DictField(
        key="GS_24",
        default_factory=dict,
        is_node=True,
    )

    weekly_demon_rewards: dict = DictField(
        key="GS_25",
        default_factory=dict,
        is_node=True,
    )

    list_rewards: dict = DictField(
        key="GS_27",
        default_factory=dict,
        is_node=True,
    )

    enabled_animations: dict = DictField(
        key="GS_28",
        default_factory=dict,
        is_node=True,
    )

    path_fix: bool = DictField(key="GS_29", default=False)

    secret_room_rewards: dict = DictField(
        key="GS_30",
        default_factory=dict,
        is_node=True,
    )

    event_level_chest_rewards: dict = DictField(
        key="GS_31",
        default_factory=dict,
        is_node=True,
    )

    unlocked_gauntlets: dict = DictField(
        key="GS_32",
        default_factory=dict,
        is_node=True,
    )
    
    username: str = DictField(key="GJA_001")

    account_id: int = DictField(key="GJA_003")

    password_gjp2: str = DictField(key="GJA_005")
    
    song_priority: int = DictField(key="MDLM_002")
    
    unk_mdlm_003: dict = DictField(
        key="MDLM_003",
        default_factory=dict,
        is_node=True,
    )
    
    news_last_read_id: int = DictField(key="newsLastReadID", default=0)
    
    editor_sfx_volume: float = DictField(key="editorSFXGlobalVolume", default=1.0)
    
    scroll_sensitivity: float = DictField(key="scrollSensitivity")
    
    special_perm_key: int = DictField(key="specialPermKey")
    
    latest_daily_id: int = DictField(key="GLM_24")
    
    latest_weekly_id: int = DictField(key="GLM_25")
    
    latest_event_id: int = DictField(key="GLM_26")
    
    show_bpm_markers: bool = DictField(key="showBPMMarkers", default=False)
 
    record_gameplay: bool = DictField(key="recordGameplay", default=False)
 
    opened_name: bool = DictField(key="clickedName", default=False)
 
    showed_diff_rate_dialog: bool = DictField(key="showedRateDiffDialog", default=False)
 
    id_name_sort_mode: int = DictField(key="idNameSortMode", default=0)
 
    # emote names, newest first, max 15 (GameManager::addRecentEmote)
    recent_emotes: StrList = DictField(
        key="recentEmotes",
        default_factory=StrList,
        decoder=StrList.from_string,
        encoder=StrList.to_string,
    )
 
    # device-local value keeper (e.g. autoBackupDir); not synced with the account
    local_keeper: dict = DictField(
        key="localKeeper",
        default_factory=dict,
        is_node=True,
    )
 
    # editor window states: ws_<i>_k / _cx / _cy / _w / _h / _s / _so / _v, i < winStateCount.
    # The ws_ keys are numbered flat keys, so only the count is a field.
    window_state_count: int = DictField(key="winStateCount", default=0)
 
    # ------------------------------------------------------------------ GameLevelManager
 
    # last seen gauntlet count ("new gauntlets" badge)
    latest_gauntlet_count: int = DictField(key="GLM_27")
 
    # GLM_24-27 initialized from the first content-status response
    latest_ids_initialized: bool = DictField(key="GLM_28", default=False)
 
    # ------------------------------------------------------------------ GameStatsManager
 
    daily_recall_unlocks: dict = DictField(
        key="GS_33",
        default_factory=dict,
        is_node=True,
    )
 
    # ------------------------------------------------------------------ MusicDownloadManager
 
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
 
    # newest first, max 20
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
 
    # custom SFX library node IDs
    favorite_custom_sfx: IntList = DictField(
        key="MDLM_011",
        default_factory=IntList,
        decoder=IntList.from_string,
        encoder=IntList.to_string,
    )
 
    keybinds_version: int = DictField(key="GJKB_Version", default=2)
 
    keybinds: KeybindDict = DictField(
        key="GJKB_Binds",
        default_factory=KeybindDict,
        decoder=KeybindDict.from_string,
        encoder=KeybindDict.to_string,
    )
 
    editor_sfx_version: int = DictField(key="editorSFXVersion", default=1)
 
    editor_sfx: EditorSFXString = DictField(
        key="editorSFX",
        default_factory=EditorSFXString,
        decoder=EditorSFXString.from_string,
        encoder=EditorSFXString.to_string,
    )
 
    editor_sfx_favorite_count: int = DictField(key="editorSFXFavoriteCount", default=0)
 
    editor_sfx_my_count: int = DictField(key="editorSFXMyCount", default=0)
 
    editor_sfx_next_local_id: int = DictField(key="editorSFXNextLocalID", default=0)
    
    active_path: int = DictField(key="GS_26", default=0)
 
