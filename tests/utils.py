import pytest
import tempfile
import shutil
import warnings
from pathlib import Path
from gmdkit import Object, ObjectList
from gmdkit.models import interfaces

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
    obj = Object()
    intf = interfaces.BaseObject(obj)
    intf.obj_id = 1899
    intf.x = 100.5
    intf.y = 200.0
    intf.groups[:] = [1,2,3]
    return obj


@pytest.fixture
def sample_object_list():
    objs = ObjectList()
    
    for i in range(3):
        obj = Object()
        intf = interfaces.BaseObject(obj)
        intf.obj_id = 1+i
        intf.x = 100.5+i*100
        intf.y = 150.5+i*100
        objs.append(obj)
    
    return objs