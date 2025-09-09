from gmdkit.models.level_pack import LevelPack
from gmdkit.models.object import ObjectList

#level = Level.from_file('../data/gmd/Skeletal Shenanigans.gmd',load=False)
#objects = level.objects
#print(level.keys())


test_level = LevelPack.from_file('d:/Downloads/Chill Dash.gmdl')
test_dict = test_level.to_plist()
test_level.to_file('d:/Downloads/test.gmdl')