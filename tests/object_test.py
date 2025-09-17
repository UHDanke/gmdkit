from gmdkit.models.level import Level
from gmdkit.models.object import ObjectList

object_string = "1,1,2,315,3,-75;1,1,2,285,3,-75,21,1004;1,1,2,255,3,-75,21,1004;1,1,2,255,3,-45,21,1004;1,1,2,255,3,-15,21,1004;1,1,2,285,3,-15,21,1004;1,1,2,315,3,-15,21,1004;1,1,2,315,3,-45,21,1004;1,1,2,345,3,-45,21,1004;1,1,2,345,3,-75,21,1004;"

obj_list = ObjectList.from_string(object_string)

obj_list.to_file("object_string.txt")

