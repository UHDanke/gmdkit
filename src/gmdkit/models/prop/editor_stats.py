# Package Imports
from gmdkit.serialization.functions import dataclass_decoder
from gmdkit.serialization.mixins import DataclassDecoderMixin


@dataclass_decoder(slots=True, separator=",", from_array=True)
class EditorStats(DataclassDecoderMixin):
    format_version: int = 0
    objects_created: int = 0
    objects_pasted: int = 0
    objects_deleted: int = 0
    transform_actions: int = 0
    edit_popups_opened: int = 0
    undo_redo: int = 0
    playtest_count: int = 0
    playtest_time: int = 0
    editor_frames: int = 0
    action_gap_0_1: int = 0
    action_gap_2_3: int = 0
    action_gap_4_7: int = 0
    action_gap_8_15: int = 0
    action_gap_16_31: int = 0
    action_gap_32_63: int = 0
    action_gap_64_127: int = 0
    action_gap_128_plus: int = 0
    editor_inputs: int = 0
    editor_sessions: int = 0
    first_open: int = 0
    original_level_id: int = 0
    original_level_version: int = 0

    @property
    def action_gap_histogram(self) -> list[int]:
        return [
            self.action_gap_0_1, self.action_gap_2_3, self.action_gap_4_7,
            self.action_gap_8_15, self.action_gap_16_31, self.action_gap_32_63,
            self.action_gap_64_127, self.action_gap_128_plus,
        ]