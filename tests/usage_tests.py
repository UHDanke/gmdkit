"""Core usage tests for gmdkit - testing fundamental interface/usage for game project workflow."""

import pytest
import tempfile
import shutil
from pathlib import Path

from gmdkit.models.object import Object, ObjectList
from gmdkit.models.level import Level
from gmdkit.models.prop.list import IDList
from gmdkit.mappings import obj_prop

ExceptionInfo = pytest.ExceptionInfo

def assert_error(exc_info: ExceptionInfo[BaseException], *patterns: str) -> None:
    msg = str(exc_info.value).lower()
    for pattern in patterns:
        p = pattern.lower()
        assert p in msg, f"Expected '{pattern}' in: {str(exc_info.value)}"


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def temp_dir():
    temp = tempfile.mkdtemp()
    yield Path(temp)
    shutil.rmtree(temp)


@pytest.fixture
def example_level_path():
    return Path(__file__).parent / "example_level.gmd"


class TestObjectCreation:
    
    def test_create_object_with_properties(self):
        obj = Object({
            obj_prop.ID: 1899,
            obj_prop.X: 100.5,
            obj_prop.Y: 200.0,
        })
        
        assert obj[obj_prop.ID] == 1899
        assert obj[obj_prop.X] == 100.5
        assert obj[obj_prop.Y] == 200.0
    
    def test_set_numeric_key_properties(self):
        # GD triggers use numeric keys
        obj = Object()
        
        obj[1] = 1268
        obj[2] = 150.0
        obj[3] = 300.0
        obj[51] = 10
        obj[57] = IDList([1, 2, 3])
        
        assert obj[1] == 1268
        assert obj[2] == 150.0
        assert obj[57] == IDList([1, 2, 3])
    
    def test_group_array_property(self):
        # Groups are stored as IDList
        obj = Object({obj_prop.GROUPS: IDList([1, 2, 3, 4, 5])})
        assert list(obj[obj_prop.GROUPS]) == [1, 2, 3, 4, 5]


class TestObjectListBasics:
    
    def test_objectlist_operations(self):
        # ObjectList supports standard list operations
        obj_list = ObjectList()
        
        obj1 = Object({obj_prop.ID: 1, obj_prop.X: 100})
        obj2 = Object({obj_prop.ID: 2, obj_prop.X: 200})
        
        obj_list.append(obj1)
        obj_list.extend([obj2])
        
        assert len(obj_list) == 2
        assert obj_list[0][obj_prop.ID] == 1
        assert obj_list[1][obj_prop.ID] == 2


class TestSerialization:
    
    def test_object_roundtrip(self):
        # Ensure object -> string -> object preserves data
        original = Object({
            obj_prop.ID: 1899,
            obj_prop.X: 150.5,
            obj_prop.Y: 250.75,
            obj_prop.GROUPS: IDList([1, 2, 3]),
        })
        
        string = original.to_string()
        restored = Object.from_string(string)
        
        assert restored[obj_prop.ID] == original[obj_prop.ID]
        assert restored[obj_prop.X] == original[obj_prop.X]
        assert restored[obj_prop.Y] == original[obj_prop.Y]
        assert list(restored[obj_prop.GROUPS]) == [1, 2, 3]
    
    def test_objectlist_roundtrip(self):
        # Ensure ObjectList -> string -> ObjectList preserves data
        original = ObjectList([
            Object({obj_prop.ID: 1, obj_prop.X: 100.5, obj_prop.Y: 150.5}),
            Object({obj_prop.ID: 2, obj_prop.X: 200.5, obj_prop.Y: 250.5}),
            Object({obj_prop.ID: 3, obj_prop.X: 300.5, obj_prop.Y: 350.5}),
        ])
        
        string = original.to_string()
        restored = ObjectList.from_string(string)
        
        assert len(restored) == len(original)
        for i, obj in enumerate(restored):
            assert obj[obj_prop.ID] == original[i][obj_prop.ID]
            assert obj[obj_prop.X] == original[i][obj_prop.X]
            assert obj[obj_prop.Y] == original[i][obj_prop.Y]
    
    def test_empty_objectlist_string(self):
        # Empty ObjectList should roundtrip correctly
        obj_list = ObjectList()
        string = obj_list.to_string()
        restored = ObjectList.from_string(string)
        assert len(restored) == 0
    
    def test_large_objectlist(self):
        obj_list = ObjectList([
            Object({obj_prop.ID: 1, obj_prop.X: i * 10, obj_prop.Y: i * 20})
            for i in range(150)
        ])
        
        string = obj_list.to_string()
        restored = ObjectList.from_string(string)
        
        assert len(restored) == 150
        assert restored[0][obj_prop.X] == 0
        assert restored[149][obj_prop.X] == 1490


class TestLevelOperations:
    
    def test_level_with_objects(self):
        level = Level.default("Test Level", load=True)
        
        level.objects.append(Object({obj_prop.ID: 1, obj_prop.X: 100}))
        level.objects.append(Object({obj_prop.ID: 2, obj_prop.X: 200}))
        
        assert len(level.objects) == 2
    
    def test_load_level_lazy(self, example_level_path):
        # Objects not loaded yet should raise error
        level = Level.from_file(example_level_path, load=False)
        
        with pytest.raises(RuntimeError) as exc_info:
            _ = level.objects
        
        assert_error(exc_info, "not loaded")
    
    def test_load_level_then_load_objects(self, example_level_path):
        level = Level.from_file(example_level_path, load=False)
        level.load()
        
        objects = level.objects
        assert isinstance(objects, ObjectList)
    
    def test_save_level_with_objects(self, temp_dir):
        level = Level.default("Object Test", load=True)
        level.objects.extend([
            Object({obj_prop.ID: 1, obj_prop.X: 100, obj_prop.Y: 200}),
            Object({obj_prop.ID: 2, obj_prop.X: 300, obj_prop.Y: 400}),
        ])
        
        output_path = temp_dir / "object_test.gmd"
        level.to_file(output_path, save=True)
        
        assert output_path.exists()
    
    def test_save_level_auto_filename(self, temp_dir):
        level = Level.default("My Test Level", load=False)
        level.to_file(temp_dir)
        
        expected = temp_dir / "My Test Level.gmd"
        assert expected.exists()


class TestRoundTrip:
    
    def test_roundtrip_basic_level(self, temp_dir):
        # Create level, save, load, verify
        original = Level.default("Roundtrip Test", load=False)
        original["k3"] = "Test description"
        
        path = temp_dir / "roundtrip.gmd"
        original.to_file(path)
        
        loaded = Level.from_file(path, load=False)
        
        assert loaded["k2"] == "Roundtrip Test"
        assert loaded["k3"] == "Test description"
    
    def test_roundtrip_with_objects(self, temp_dir):
        # Create level with objects, save, load, verify objects intact
        level = Level.default("Object Roundtrip", load=True)
        
        level.objects.extend([
            Object({obj_prop.ID: 1, obj_prop.X: 100.5, obj_prop.Y: 200.5}),
            Object({obj_prop.ID: 2, obj_prop.X: 300.5, obj_prop.Y: 400.5}),
            Object({obj_prop.ID: 3, obj_prop.X: 500.5, obj_prop.Y: 600.5}),
        ])
        
        original_count = len(level.objects)
        original_objects = [
            {obj_prop.ID: obj[obj_prop.ID], obj_prop.X: obj[obj_prop.X], obj_prop.Y: obj[obj_prop.Y]}
            for obj in level.objects
        ]
        
        path = temp_dir / "object_roundtrip.gmd"
        level.to_file(path, save=True)
        
        loaded = Level.from_file(path, load=True)
        loaded_objects = loaded.objects
        
        assert len(loaded_objects) == original_count
        for i, obj in enumerate(loaded_objects):
            assert obj[obj_prop.ID] == original_objects[i][obj_prop.ID]
            assert obj[obj_prop.X] == original_objects[i][obj_prop.X]
            assert obj[obj_prop.Y] == original_objects[i][obj_prop.Y]
    
    def test_roundtrip_property_types(self, temp_dir):
        # Verify property types survive round-trip
        level = Level.default("Type Test", load=True)
        
        level.objects.append(Object({
            obj_prop.ID: 1899,
            obj_prop.X: 150.5,
            obj_prop.Y: 250.75,
            obj_prop.GROUPS: IDList([1, 2, 3]),
            62: 1,
        }))
        
        path = temp_dir / "type_test.gmd"
        level.to_file(path, save=True)
        
        loaded = Level.from_file(path, load=True)
        obj = loaded.objects[0]
        
        assert isinstance(obj[obj_prop.ID], int)
        assert isinstance(obj[obj_prop.X], (int, float))
        assert isinstance(obj[obj_prop.Y], (int, float))
        assert isinstance(obj[obj_prop.GROUPS], IDList)
        assert list(obj[obj_prop.GROUPS]) == [1, 2, 3]
        assert obj[62] is True or obj[62] == 1


class TestTriggerCreation:
    
    def test_create_multiple_trigger_types(self):
        # Spawn trigger
        spawn = Object({
            1: 1268,
            2: 150.0,
            51: 100,
            57: IDList([10, 20]),
            20: 4,
            62: 1,
        })
        assert spawn[1] == 1268
        assert spawn[51] == 100
        
        # Move trigger
        move = Object({
            1: 901,
            2: 200.0,
            51: 50,
            57: IDList([10]),
            10: 2.5,
            28: 15.0,
            29: 25.0,
        })
        assert move[1] == 901
        assert move[10] == 2.5
        
        # Pulse trigger
        pulse = Object({
            1: 1006,
            2: 300.0,
            51: 75,
            57: IDList([1, 2]),
            49: 1,
            50: "180a1a0a1a1",
        })
        assert pulse[1] == 1006
        assert pulse[49] == 1
    
    def test_create_many_triggers(self):
        # Generate patterns with 100+ triggers
        triggers = ObjectList()
        
        for i in range(100):
            trigger = Object({
                1: 1268,
                2: float(i * 10),
                3: 100.0,
                51: 100 + i,
                57: IDList([10, 20, 30]),
            })
            triggers.append(trigger)
        
        assert len(triggers) == 100
        assert triggers[0][2] == 0.0
        assert triggers[99][2] == 990.0
        
        # Verify serialization works
        string = triggers.to_string()
        restored = ObjectList.from_string(string)
        assert len(restored) == 100


class TestComplexProperties:
    
    def test_multiple_property_types_together(self):
        # Object with mixed types should roundtrip correctly
        obj = Object({
            1: 1899,
            2: 150.5,
            3: 250.75,
            57: IDList([1, 2, 3, 4, 5]),
            62: 1,
            87: 0,
            31: "test_string",
            442: "1.2.3.4",
        })
        
        string = obj.to_string()
        restored = Object.from_string(string)
        
        assert restored[1] == 1899
        assert restored[2] == 150.5
        assert list(restored[57]) == [1, 2, 3, 4, 5]
    
    def test_groups_edge_cases(self):
        # Empty groups array
        empty = Object({1: 1, 57: IDList([])})
        assert list(empty[57]) == []
        
        # Large groups array (50 groups)
        groups = IDList(range(1, 51))
        large = Object({1: 1, 57: groups})
        assert len(large[57]) == 50
        assert large[57][0] == 1
        assert large[57][-1] == 50


class TestEdgeCases:
    
    def test_empty_object_string(self):
        # Empty ObjectList should parse correctly
        empty_string = ""
        obj_list = ObjectList.from_string(empty_string)
        assert len(obj_list) == 0
    
    def test_missing_object_string_in_level(self):
        # Level without object string should raise error
        level = Level({"k2": "Test"})
        
        with pytest.raises(RuntimeError) as exc_info:
            _ = level.objects
        
        assert_error(exc_info, "missing")
    
    def test_objectlist_with_one_object(self):
        # Single object ObjectList should roundtrip
        obj_list = ObjectList([
            Object({obj_prop.ID: 1, obj_prop.X: 100})
        ])
        
        string = obj_list.to_string()
        restored = ObjectList.from_string(string)
        
        assert len(restored) == 1
        assert restored[0][obj_prop.ID] == 1


class TestFullWorkflow:
    
    def test_complete_game_workflow(self, temp_dir):
        # Simulate complete workflow: create triggers, save level, load it back
        level = Level.default("Game Test Level", load=True)
        level["k3"] = "Generated by game code"
        
        spawn = Object({
            1: 1268,
            2: 100.0,
            51: 1000,
            57: IDList([1, 2]),
            20: 4,
            62: 1,
            87: 1,
        })
        level.objects.append(spawn)
        
        move = Object({
            1: 901,
            2: 200.0,
            51: 2000,
            57: IDList([1, 2]),
            10: 2.5,
            28: 50.0,
            29: 100.0,
        })
        level.objects.append(move)
        
        pulse = Object({
            1: 1006,
            2: 300.0,
            51: 3000,
            57: IDList([1, 2]),
            45: 0.1,
            46: 1.0,
            47: 0.3,
        })
        level.objects.append(pulse)
        
        save_path = temp_dir / "game_test.gmd"
        level.to_file(save_path, save=True)
        
        loaded = Level.from_file(save_path, load=True)
        
        assert loaded["k2"] == "Game Test Level"
        assert loaded["k3"] == "Generated by game code"
        
        loaded_triggers = loaded.objects
        assert len(loaded_triggers) == 3
        
        assert loaded_triggers[0][1] == 1268
        assert loaded_triggers[0][51] == 1000
        
        assert loaded_triggers[1][1] == 901
        assert loaded_triggers[1][10] == 2.5
        
        assert loaded_triggers[2][1] == 1006