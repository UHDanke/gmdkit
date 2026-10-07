import pytest
from pathlib import Path
from gmdkit import Level, Object
from gmdkit.models import interfaces
from tests.utils import ONLINE_LEVELS, OFFLINE_LEVELS

level_paths = (ONLINE_LEVELS + OFFLINE_LEVELS)[:10]

@pytest.mark.parametrize("level_file", level_paths, ids=lambda p: p.name)
def test_roundtrip(level_file: Path, tmp_path: Path) -> None:
    """Loads, modifies, saves, and reloads a level, verifying all serialization steps."""
    level = Level.from_file(level_file, load=True)
    initial_count = len(level.objects)
    
    for i, obj in enumerate(level.objects):
        assert len(obj) > 0, f"Object {i} is empty before modification"
    
    obj = Object()
    intf = interfaces.MoveTrigger(obj)
    intf.obj_id = 901
    intf.x = 100.0
    intf.y = 100.0
    intf.duration = 1.0
    intf.target_id = 1
    
    level.objects.append(obj)

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
    app_intf = appended.require_interface(interfaces.MoveTrigger)
    
    assert app_intf.obj_id == 901, "Object ID should survive round-trip"
    assert app_intf.x == 100.0, "X position should survive round-trip"
    assert app_intf.y == 100.0, "Y position should survive round-trip"