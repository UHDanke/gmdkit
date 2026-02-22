from gmdkit.models.object import ObjectList

object_string = "1,1,2,315,3,-75;1,1,2,285,3,-75,21,1004;1,1,2,255,3,-75,21,1004;1,1,2,255,3,-45,21,1004;1,1,2,255,3,-15,21,1004;1,1,2,285,3,-15,21,1004;1,1,2,315,3,-15,21,1004;1,1,2,315,3,-45,21,1004;1,1,2,345,3,-45,21,1004;1,1,2,345,3,-75,21,1004;"

def test_object_string_roundtrip(tmp_path):
    obj_list = ObjectList.from_string(object_string)
    
    out_file = tmp_path / "object_string.txt"
    
    obj_list.to_file(out_file)
    
    exported = out_file.read_text()
    
    assert object_string == exported, "Original and exported object strings do not match.\n"