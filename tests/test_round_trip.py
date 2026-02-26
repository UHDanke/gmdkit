
import pytest
from pathlib import Path

from gmdkit.models.level import Level
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop

from tests.utils import ONLINE_LEVELS, OFFLINE_LEVELS

level_paths = (ONLINE_LEVELS + OFFLINE_LEVELS)[:10]

@pytest.mark.parametrize("level_file", level_paths, ids=lambda p: p.name)
def test_roundtrip(level_file: Path, tmp_path: Path) -> None:
    """Loads, modifies, saves, and reloads a level, verifying all serialization steps."""
    level = Level.from_file(level_file, load=True)
    initial_count = len(level.objects)
    
    for i, obj in enumerate(level.objects):
        assert len(obj) > 0, f"Object {i} is empty before modification"

    level.objects.append(Object({
        obj_prop.ID: 901,
        obj_prop.X: 100.0,
        obj_prop.Y: 100.0,
        obj_prop.trigger.move.DURATION: 1.0,
        obj_prop.trigger.move.TARGET_ID: 1,
    }))

    assert len(level.objects) == initial_count + 1, (
        "Object count should increase by exactly 1 after append"
    )
    
    out_file = tmp_path / level_file.name
    level.to_file(out_file, save=True)
    
    assert out_file.exists(), "Export should have created the output file"
    
    reloaded = Level.from_file(out_file, load=True)

    for i, obj in enumerate(reloaded.objects):
        assert len(obj) > 0, f"Object {i} is empty after round-trip"
    
    assert len(reloaded.objects) == initial_count + 1, (
        "After reload, the appended object should still be present"
    )
    
    appended = reloaded.objects[-1]
    assert appended[obj_prop.ID] == 901, "Object ID should survive round-trip"
    assert appended[obj_prop.X] == 100.0, "X position should survive round-trip"
    assert appended[obj_prop.Y] == 100.0, "Y position should survive round-trip"