import pytest
import tempfile
import shutil
from pathlib import Path

from gmdkit.models.object import Object, ObjectList
from gmdkit.models.level import Level
from gmdkit.models.prop.list import IDList
from gmdkit.mappings import obj_prop


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
