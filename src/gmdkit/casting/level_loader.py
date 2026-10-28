# Package Imports
from gmdkit.utils import enums
from gmdkit.models.object import Object, ObjectList, ObjectStringLazy
from gmdkit.models.prop.replay import ReplayStringLazy
from gmdkit.models.prop.platformer_save import PlatformerCheckpointLazy
from gmdkit.models.prop.list import IntList
from gmdkit.models.prop.pos_list import PositionList
from gmdkit.models.prop.death_markers import (
    DeathMarkerList, DeathCounts, AttemptHistory, SessionStringLazy,
    StartPosDeathCounts, StartPosAttemptHistory, GlobalDeathDataLazy
    )
from gmdkit.models.prop.controls import LevelControls
from gmdkit.models.prop.editor_stats import EditorStats
from gmdkit.serialization.classes import DictField, FieldMetaclass, AliasAttr
from gmdkit.serialization.mixins import PlistLoaderMixin
from gmdkit.serialization.helpers import serial_field, lazy_field, base64_field, encoded_field
from gmdkit.utils.functions import create_uid

class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):
    
    HAS_NODES = True
    
    level_id: int = DictField(key="k1")

    name: str = DictField(key="k2", default="Unnamed")

    description: str = encoded_field(key="k3")

    object_string: ObjectStringLazy = lazy_field("k4", ObjectStringLazy)
    
    start: Object = AliasAttr("object_string.start")
    
    objects: ObjectList = AliasAttr("object_string.objects")

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

    level_type: enums.LevelType = DictField(
        key="k21",
        decoder=enums.LevelType,
        default=enums.LevelType.LOCAL,
    )

    like_rating: int = DictField(key="k22", default=0)

    dislikes: int = DictField(key="k24", default=0)

    length_type: enums.LevelLength = DictField(
        key="k23",
        decoder=enums.LevelLength,
        default=enums.LevelLength.TINY,
    )

    is_demon: bool = DictField(key="k25", default=False)

    stars: int = DictField(key="k26", default=0)

    feature_score: int = DictField(key="k27", default=0)

    is_auto: bool = DictField(key="k33", default=False)

    replay_data: ReplayStringLazy = lazy_field("k34", ReplayStringLazy)

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

    level_progress: IntList = serial_field("k88", IntList)

    verified_check: bool = DictField(key="k89", default=False)

    leaderboard_percentage: int = DictField(key="k90")

    locked_layers: IntList = serial_field("k91", IntList)

    bypass_unlimited_objs: bool = DictField(key="k93", default=False)

    friends_only: bool = DictField(key="k94", default=False)

    verification_time: int = DictField(key="k95", default=0)

    upload_date: int = DictField(key="k98")

    update_date: int = DictField(key="k99")

    saved_camera_positions: PositionList = serial_field("k101", PositionList)

    preview_lock_x: int = DictField(key="k102", default=0)

    preview_lock_y: int = DictField(key="k103", default=0)

    songs: IntList = serial_field("k104", IntList)

    sfx: IntList = serial_field("k105", IntList)

    best_time: int = DictField(key="k107")

    best_points: int = DictField(key="k108")

    local_best_time: IntList = serial_field("k109", IntList)

    local_best_points: IntList = serial_field("k110", IntList)

    platformer_seed: int = DictField(key="k111")

    shake_disabled: bool = DictField(key="k112", default=False)

    ticks_best_time: int = DictField(key="k115")

    ticks_best_points: int = DictField(key="k116")

    clicks_best_time: int = DictField(key="k117")

    clicks_best_points: int = DictField(key="k118")

    replay_best_time: ReplayStringLazy = lazy_field("k119", ReplayStringLazy)

    replay_best_points: ReplayStringLazy = lazy_field("k120", ReplayStringLazy)

    coins_best_time: int = DictField(key="k121")

    coins_best_points: int = DictField(key="k122")

    saved_best_time: bool = DictField(key="k123", default=False)

    saved_best_points: bool = DictField(key="k124", default=False)

    toggle_cbs: enums.ToggleCBS = DictField(
        key="k125",
        decoder=enums.ToggleCBS,
        default=enums.ToggleCBS.DEFAULT,
    )
    
    autobackup_id: str = DictField(key="k126", default_factory=lambda: create_uid(length=16))
    
    last_autobackup_time: int = DictField(key="k127", default=0)
    
    platformer_save: PlatformerCheckpointLazy = lazy_field("k128", PlatformerCheckpointLazy)
    
    enable_platformer_save: bool = DictField("k129", default=False)
    
    platformer_save_level_version: int = DictField(key="k130", default=0)
    
    platformer_save_replay: ReplayStringLazy = lazy_field("k131", ReplayStringLazy)
    
    platformer_save_format_version: int = DictField(key="k132", default=0)
    
    death_tracker_format_version: int = DictField(key="k133", default=0)
    
    death_counts: DeathCounts = serial_field("k134", DeathCounts)
    
    startpos_death_counts: StartPosDeathCounts = serial_field("k135", StartPosDeathCounts)
    
    attempt_history: AttemptHistory = serial_field("k136", AttemptHistory)
    
    startpos_attempt_history: StartPosAttemptHistory = serial_field("k137", StartPosAttemptHistory)
    
    session_start: int = DictField(key="k138")
    
    session_last_played: int = DictField(key="k139")
    
    death_markers: DeathMarkerList = serial_field("k140", DeathMarkerList)
    
    death_data_pending_upload: bool = DictField(key="k141", default=False)
    
    session_play_time: int = DictField(key="k142")
    
    total_play_time: int = DictField(key="k143")
    
    completions: int = DictField(key="k145")

    archived_sessions: SessionStringLazy = lazy_field("k146", SessionStringLazy)
    
    creator_controls: LevelControls = base64_field("k147",LevelControls)

    creator_controls_version: int = DictField(key="k148")

    custom_controls: LevelControls = base64_field("k149",LevelControls)

    custom_controls_source: int = DictField(
        key="k150",
        decoder=enums.ControlSource,
        default=enums.ControlSource.CREATOR,
        )
    
    death_upload_rate: int = DictField(key="k151", default=0)
    
    global_death_stats: GlobalDeathDataLazy = lazy_field("k152", GlobalDeathDataLazy)
    
    edited_custom_controls: bool = DictField(key="k153", default=False)
    
    practice_attempts: int = DictField(key="k154", default=0)
    
    custom_controls_type: int = DictField(
        key="k155",
        decoder=enums.ControlType,
        default=enums.ControlType.NONE,
        )
    
    editor_stats: EditorStats = serial_field("k156", EditorStats)
    
    editor_camera_x: float = DictField(key="kI1", default=0.0)

    editor_camera_y: float = DictField(key="kI2", default=0.0)

    editor_camera_zoom: float = DictField(key="kI3", default=1.0)

    editor_build_tab_page: int = DictField(key="kI4", default=0)

    editor_build_tab: int = DictField(key="kI5", default=0)

    editor_build_tab_pages: dict = DictField(key="kI6", default_factory=dict, is_node=True)

    editor_layer: int = DictField(key="kI7", default=0)
        
    @property
    def difficulty(self) -> enums.LevelDifficulty:
        """
        Gets the difficulty rating of a level.

        Returns
        -------
        enums.LevelDifficulty
            An enum specifying the level's difficulty.
        """
        if self.rating == 0:
            return enums.LevelDifficulty.NA

        match self.rating_sum:
            case enums.LevelRating.NONE:
                return enums.LevelDifficulty.NA
            case enums.LevelRating.EASY:
                if self.is_auto:
                    return enums.LevelDifficulty.AUTO
                else:
                    return enums.LevelDifficulty.EASY
            case enums.LevelRating.NORMAL:
                return enums.LevelDifficulty.NORMAL
            case enums.LevelRating.HARD:
                return enums.LevelDifficulty.HARD

            case enums.LevelRating.HARDER:
                return enums.LevelDifficulty.HARDER

            case enums.LevelRating.INSANE:
                if self.is_demon:

                    match self.demon_type:

                        case enums.DemonRating.EASY:
                            return enums.LevelDifficulty.EASY_DEMON

                        case enums.DemonRating.MEDIUM:
                            return enums.LevelDifficulty.MEDIUM_DEMON

                        case enums.DemonRating.HARD:
                            return enums.LevelDifficulty.HARD_DEMON

                        case enums.DemonRating.INSANE:
                            return enums.LevelDifficulty.INSANE_DEMON

                        case enums.DemonRating.EXTREME:
                            return enums.LevelDifficulty.EXTREME_DEMON

                        case _:
                            return enums.LevelDifficulty.HARD_DEMON
                else:
                    return enums.LevelDifficulty.INSANE

            case _:
                return enums.LevelDifficulty.NA
    
    @difficulty.setter
    def difficulty(self, value: enums.LevelDifficulty):
        del self.is_auto
        del self.is_demon
        self.rating = 10
        
        match value:
            case enums.LevelDifficulty.NA:
                del self.rating
                self.rating_sum = enums.LevelRating.NONE
                
            case enums.LevelDifficulty.AUTO:
                self.rating_sum = enums.LevelRating.EASY
                self.is_auto = True
                
            case enums.LevelDifficulty.EASY:
                self.rating_sum = enums.LevelRating.EASY
                
            case enums.LevelDifficulty.NORMAL:
                self.rating_sum = enums.LevelRating.NORMAL
                
            case enums.LevelDifficulty.HARD:
                self.rating_sum = enums.LevelRating.HARD
                
            case enums.LevelDifficulty.HARDER:
                self.rating_sum = enums.LevelRating.HARDER
                
            case enums.LevelDifficulty.INSANE:
                self.rating_sum = enums.LevelRating.INSANE
                
            case (
                enums.LevelDifficulty.EASY_DEMON
                | enums.LevelDifficulty.MEDIUM_DEMON
                | enums.LevelDifficulty.HARD_DEMON
                | enums.LevelDifficulty.INSANE_DEMON
                | enums.LevelDifficulty.EXTREME_DEMON
            ):
                self.rating_sum = enums.LevelRating.INSANE
                self.is_demon = True
                
                match value:
                    case enums.LevelDifficulty.EASY_DEMON: 
                        self.demon_type = enums.DemonRating.EASY
                    case enums.LevelDifficulty.MEDIUM_DEMON: 
                        self.demon_type = enums.DemonRating.MEDIUM
                    case enums.LevelDifficulty.HARD_DEMON: 
                        self.demon_type = enums.DemonRating.HARD
                    case enums.LevelDifficulty.INSANE_DEMON: 
                        self.demon_type = enums.DemonRating.INSANE
                    case enums.LevelDifficulty.EXTREME_DEMON: 
                        self.demon_type = enums.DemonRating.EXTREME
                        
            case _:
                raise ValueError(f"Unsupported level difficulty: {value!r}")

    @property
    def feature_rating(self) -> enums.FeatureRating:
        match self.epic_rating:

            case enums.EpicRating.EPIC:
                return enums.FeatureRating.EPIC

            case enums.EpicRating.LEGENDARY:
                return enums.FeatureRating.LEGENDARY

            case enums.EpicRating.MYTHIC:
                return enums.FeatureRating.MYTHIC

            case _:
                if self.feature_score:
                    return enums.FeatureRating.FEATURED

                elif self.stars:
                    return enums.FeatureRating.RATED

                else:
                    return enums.FeatureRating.UNRATED

    @feature_rating.setter
    def feature_rating(self, value: enums.FeatureRating) -> None:
        match value:
            case enums.FeatureRating.UNRATED:
                self.epic_rating = enums.EpicRating.NONE
                self.feature_score = 0
                self.stars = 0

            case enums.FeatureRating.RATED:
                self.epic_rating = enums.EpicRating.NONE
                self.feature_score = 0

            case enums.FeatureRating.FEATURED:
                self.epic_rating = enums.EpicRating.NONE
                self.feature_score = self.feature_score or 1

            case enums.FeatureRating.EPIC:
                self.epic_rating = enums.EpicRating.EPIC

            case enums.FeatureRating.LEGENDARY:
                self.epic_rating = enums.EpicRating.LEGENDARY

            case enums.FeatureRating.MYTHIC:
                self.epic_rating = enums.EpicRating.MYTHIC

            case _:
                raise ValueError(f"Unsupported feature rating: {value!r}")

    @property
    def timely_type(self) -> enums.TimelyType:
        """
        Gets the timely (daily, weekly, event) type of a level.
            
        Returns
        -------
        enums.TimelyType
            An enum specifying the level's timely type.
        """
        tid = self.timely_id
        
        if tid is None:
            return enums.TimelyType.NONE
        elif (0<tid<=10000):
            return enums.TimelyType.DAILY
        elif (10000<tid<=20000):
            return enums.TimelyType.WEEKLY
        elif (20000<tid<=30000):
            return enums.TimelyType.EVENT
        else:
            return enums.TimelyType.NONE
    

FieldLoaderMixin.add_field(key="k106") # unknown