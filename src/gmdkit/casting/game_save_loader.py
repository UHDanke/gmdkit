# Package Imports
from gmdkit.models.level import LevelMapping
from gmdkit.models.level_pack import LevelPackList
from gmdkit.models.template import SmartTemplateList
from gmdkit.models.object import ObjectGroupDict
from gmdkit.models.prop.dpad import (
    MoveButton, JumpButton,
    SingleLayout, DualLayout
)
from gmdkit.models.prop.song_info import SongInfoList
from gmdkit.serialization.classes import DictField, FieldMetaclass
from gmdkit.serialization.mixins import PlistLoaderMixin
from gmdkit.models.prop.plist import (
    StrBoolDict, IntBoolDict,
    IntStrDict,
    PlistDict
)
from gmdkit.models.prop.likes import LikeDict
from gmdkit.utils import enums


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):

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

    unused_8: dict = DictField(
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

    active_path: str = DictField(key="GS_26", default="")

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
