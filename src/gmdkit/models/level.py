# Imports
from typing import Any, Self
from pathlib import Path
from datetime import datetime
import re

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.serialization.mixins import (
    FilePathMixin,
    FolderLoaderMixin,
    PlistLoaderMixin,
    CompressFileMixin,
    PathString
)
from gmdkit.serialization.functions import (
    kv_wrap, args_wrap
)
from gmdkit.utils import enums
from gmdkit.casting.level_loader import FieldLoaderMixin
from gmdkit.models.interfaces import LevelSettings
from gmdkit.constants.paths.save import AUTOBACKUPS_PATH


class Level(FilePathMixin,CompressFileMixin,FieldLoaderMixin,DictClass[str,Any]):
    
    ENCODER_KEY = 4
    EXTENSION = "gdlvl"
    COMPRESSED = True
    COMPRESSION = "gzip"

    def _name_fallback_(self):
        name = re.sub(r"\s+", "_", str(self.name).strip())
        name = re.sub(r"[^A-Za-z0-9_]", "", name)
        return name or None
    
    def _duplicate_file_(self, path:Path) -> Path:
        stem, suffix, index = path.stem, path.suffix, 1
        while path.exists():
            path = path.with_name(f"{stem}_{index}{suffix}")
            index += 1
        return path

    @classmethod
    def from_editor(cls, name:str="Unnamed") -> Self:
        new = cls()
        new.name = name
        obj_str = new.object_string
        new.saved_camera_positions
        new.editable = True
        new.level_type = enums.LevelType.LOCAL
        new.binary_version = 51
        new.editor_camera_zoom = 1.0
        new.editor_build_tab_pages = {str(tab): "0" for tab in range(14)}
        
        start = obj_str.start
        settings = start.require_interface(LevelSettings)
        colors = settings.colors
        colors.set_defaults(
            enums.ColorID.BACKGROUND,
            enums.ColorID.GROUND,
            enums.ColorID.GROUND_2,
            enums.ColorID.LINE,
            enums.ColorID.MIDDLEGROUND,
            enums.ColorID.MIDDLEGROUND_2,
            enums.ColorID.PLAYER_1,
            enums.ColorID.PLAYER_2)
        settings.allow_multi_rotate = True
        settings.enable_2_2_changes = True
        settings.track_edit_time = True
        settings.track_edit_time_copies = True
        settings.enable_impulse_fix = True
        settings.allow_static_object_rotate = True
        settings.reverse_sync = True
        settings.enable_player_squeeze = True
        settings.fix_gravity_bug = True
        settings.decrease_boost_slide = True
        settings.fix_negative_scale = True
        settings.fix_robot_jump = True
        settings.dynamic_height = True
        settings.sort_groups = True
        settings.fix_radius_collision = True
        return new

    def clean_export(self) -> Self:
        del self.level_id
        del self.creator
        del self.user_id
        del self.account_id
        del self.uploaded
        del self.version
        del self.upload_date
        del self.update_date
        del self.password
        del self.original_id
        del self.modified
        del self.capacity_string
        del self.verified
        del self.coins_verified
        del self.coin_1_verified
        del self.coin_2_verified
        del self.coin_3_verified
        del self.rating
        del self.rating_sum
        del self.downloads
        del self.like_rating
        del self.dislikes
        del self.feature_score
        del self.epic_rating
        del self.official_difficulty
        del self.stars
        del self.is_demon
        del self.demon_type
        del self.timely_id
        del self.gauntlet
        del self.alt_game
        del self.favorite
        del self.folder
        del self.index
        del self.attempts
        del self.practice_attempts
        del self.jumps
        del self.clicks_best
        del self.time_best
        del self.score_seed
        del self.level_progress
        del self.verified_check
        del self.normal_mode_best
        del self.orb_percentage
        del self.leaderboard_percentage
        del self.practice_mode_best
        del self.anticheat_triggered
        del self.best_time
        del self.ticks_best_time
        del self.clicks_best_time
        del self.coins_best_time
        del self.replay_best_time
        del self.best_points
        del self.ticks_best_points
        del self.clicks_best_points
        del self.coins_best_points
        del self.replay_best_points
        del self.platformer_seed
        del self.saved_best_time
        del self.saved_best_points
        del self.platformer_save
        del self.platformer_save_level_version
        del self.platformer_save_format_version
        del self.platformer_save_replay
        del self.enable_platformer_save
        del self.local_best_time
        del self.local_best_points
        del self.death_tracker_format_version
        del self.death_counts
        del self.startpos_death_counts
        del self.attempt_history
        del self.startpos_attempt_history
        del self.session_start
        del self.session_last_played
        del self.session_play_time
        del self.total_play_time
        del self.completions
        del self.archived_sessions
        del self.death_markers
        del self.death_data_pending_upload
        del self.death_upload_rate
        del self.global_death_stats
        del self.bypass_high_objs
        del self.bypass_unlimited_objs
        del self.ldm_enabled
        del self.shake_disabled
        del self.autobackup_id
        del self.last_autobackup_time
        return self

    @classmethod
    def from_gmd(cls, path:PathString, **kwargs) -> Self:
        return super().from_file(path=path,extension="gmd",compressed=False, **kwargs)

    def to_gmd(self, path:PathString, **kwargs) -> Path:
        path = super().to_file(path=path,extension="gmd",compressed=False, **kwargs)
        assert isinstance(path, Path)
        return path
    
    def create_backup(self, backup_folder:PathString=AUTOBACKUPS_PATH, **kwargs):
        if backup_folder is None:
            raise RuntimeError(f"[{type(self)}] Invalid backup folder")
        
        uid = self.autobackup_id
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = re.sub(r'[<>:"/\\|?*]', "_", self._name_fallback_())
        path = backup_folder / f"{uid}_{file_name}_{timestamp}.gdlvl"        
        path = super().to_file(path=path, **kwargs)
        assert isinstance(path, Path)
        return path
    
        
        

class LevelList(FolderLoaderMixin,FilePathMixin,PlistLoaderMixin,ListClass[Level]):

    __slots__ = ()

    DECODER = Level.from_node
    ENCODER = Level.to_node
    IS_ARRAY = True
    EXTENSION = "plist"

    FOLDER_DECODER = staticmethod(args_wrap(Level.from_file,1))
    FOLDER_ENCODER = staticmethod(args_wrap(Level.to_file,2))
    FOLDER_EXTENSION = Level.EXTENSION

    LOAD_CONTENT = False

    def _name_fallback_(self):
        return "level_list"

class LevelMapping(PlistLoaderMixin,DictClass[int,Level]):
    DECODER = staticmethod(kv_wrap(int, Level.from_node))
    ENCODER = staticmethod(kv_wrap(str, Level.to_node))
    LOAD_CONTENT = False