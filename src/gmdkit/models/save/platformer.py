# Imports
from typing import Any, Optional
 
# Package Imports
from gmdkit.utils import enums
from gmdkit.utils.types import DictClass
from gmdkit.serialization.classes import DictField, FieldMetaclass
from gmdkit.serialization.functions import kv_wrap, decompress_string, compress_string
from gmdkit.serialization.mixins import (
    PlistDecoderMixin,
    PlistLoaderMixin,
    CompressFileMixin,
    FilePathMixin,
    DefaultPathMixin
    )
from gmdkit.models.prop.replay import ReplayStringLazy
from gmdkit.models.prop.platformer_save import PlatformerCheckpointLazy
from gmdkit.constants.paths.save import PLATFORMER_SAVE_PATH

 
def owner_hash(key: str, account_id: int) -> int:
    """Entry "ow": 32-bit FNV-1a of the journal key, seeded with account ID * 0x9E3779B1."""
    h = (account_id * 0x9E3779B1) & 0xFFFFFFFF
    for b in key.encode():
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h & 0x7FFFFFFF
 
 
class PlatformerSaveEntry(PlistLoaderMixin, DictClass[str, Any], metaclass=FieldMetaclass):
    HAS_NODES = True

    level_type: enums.LevelType = DictField(
        key="t", decoder=enums.LevelType.from_string, encoder=int, default=enums.LevelType.SAVED
        )
 
    level_id: int = DictField(key="id", default=0)
 
    daily_id: int = DictField(key="did", default=0)
 
    gauntlet: bool = DictField(key="g", default=False)
 
    autosave_uid: str = DictField(key="uid", default="")
 
    platformer_save: PlatformerCheckpointLazy = DictField(
        key="cs",
        decoder=lambda s: PlatformerCheckpointLazy.load_string(s or ""),
        encoder=PlatformerCheckpointLazy.save_string,
        default_factory=PlatformerCheckpointLazy,
        )
 
    platformer_save_level_version: int = DictField(key="cv", default=0)
 
    platformer_save_format_version: int = DictField(key="fv", default=0)
 
    platformer_save_replay: ReplayStringLazy = DictField(
        key="rs",
        decoder=lambda s: ReplayStringLazy.load_string(s or ""),
        encoder=ReplayStringLazy.save_string,
        default_factory=ReplayStringLazy,
    )
 
    enable_platformer_save: bool = DictField(key="ps", default=False)
 
    sequence: int = DictField(key="sq", default=0)
 
    owner: int = DictField(key="ow", default=0)
 
    @property
    def journal_key(self) -> str:
        if self.level_type == enums.LevelType.LOCAL:
            return f"l{self.autosave_uid}"
        if self.daily_id > 0:
            return f"d{self.daily_id}_{self.level_id}"
        if self.gauntlet:
            return f"g{self.level_id}"
        return f"o{self.level_id}"
 
    def is_owned_by(self, account_id: int, key: Optional[str] = None) -> bool:
        return self.owner == owner_hash(self.journal_key if key is None else key, account_id)
 
    def set_owner(self, account_id: int, key: Optional[str] = None):
        self.owner = owner_hash(self.journal_key if key is None else key, account_id)
 
 
class PlatformerSave(
        DefaultPathMixin,
        FilePathMixin,
        CompressFileMixin,
        PlistDecoderMixin,
        DictClass[str, PlatformerSaveEntry]
        ):
 
    COMPRESSED = True
    COMPRESSION = "gzip"
    EXTENSION = "dat"
    DEFAULT_PATH = PLATFORMER_SAVE_PATH
    CLEANUP_ROOT = True
 
    DECODER = staticmethod(kv_wrap(None, PlatformerSaveEntry.from_node))
    ENCODER = staticmethod(kv_wrap(None, PlatformerSaveEntry.to_node))
 
    def _name_fallback_(self):
        return "CCPlatformerSave"
 
    def add(self, entry: PlatformerSaveEntry, account_id: Optional[int] = None) -> str:
        key = entry.journal_key
        entry.sequence = max((e.sequence for e in self.values()), default=0) + 1
        if account_id is not None:
            entry.set_owner(account_id, key)
        self[key] = entry
        return key
 
    def owned_by(self, account_id: int) -> dict[str, PlatformerSaveEntry]:
        return {k: e for k, e in self.items() if e.is_owned_by(account_id, k)}
 
 
if __name__ == "__main__":
 
    from gmdkit.utils.classes import Timer
 
    _t = Timer(start=True)
    platformer_save = PlatformerSave.from_default_path()
    print("Load took", _t.end(), "seconds")