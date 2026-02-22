import pytest
import tempfile
import shutil
import warnings
from pathlib import Path

from gmdkit.models.object import Object, ObjectList
from gmdkit.models.prop.list import IDList
from gmdkit.mappings import obj_prop


LEVELS_DIR = Path(__file__).parent.parent / "data" / "gmd"

ALL_STORED_LEVELS = [p for p in LEVELS_DIR.rglob("*.gmd")]
ONLINE_LEVELS = [p for p in (LEVELS_DIR / "online").rglob("*.gmd")]
OFFLINE_LEVELS = [p for p in (LEVELS_DIR / "offline").rglob("*.gmd")]

def assert_error(exc_info: pytest.ExceptionInfo[BaseException], *patterns: str) -> None:
    """Assert exception message contains all patterns (case-insensitive)."""
    msg = str(exc_info.value).lower()
    for pattern in patterns:
        p = pattern.lower()
        assert p in msg, f"Expected '{pattern}' in: {str(exc_info.value)}"


def assert_warning(warning_list: list[warnings.WarningMessage], *patterns: str) -> None:
    """Assert warning list contains all patterns (case-insensitive)."""
    combined_msgs = " ".join(str(w.message).lower() for w in warning_list)
    for pattern in patterns:
        p = pattern.lower()
        assert p in combined_msgs, f"Expected '{pattern}' in warnings."


@pytest.fixture
def temp_dir():
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)


@pytest.fixture
def example_level_path():
    return Path(__file__).parent / "example_level.gmd"


@pytest.fixture
def sample_object():
    return Object({
        obj_prop.ID: 1899,
        obj_prop.X: 100.5,
        obj_prop.Y: 200.0,
        obj_prop.GROUPS: IDList([1, 2, 3])
    })


@pytest.fixture
def sample_object_list():
    return ObjectList([
        Object({obj_prop.ID: 1, obj_prop.X: 100.5, obj_prop.Y: 150.5}),
        Object({obj_prop.ID: 2, obj_prop.X: 200.5, obj_prop.Y: 250.5}),
        Object({obj_prop.ID: 3, obj_prop.X: 300.5, obj_prop.Y: 350.5}),
    ])
