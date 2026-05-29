from gmdkit.remapping.rules import BASE_ID_HANDLER
from gmdkit.remapping import IDType
from gmdkit import Level

lvl = Level.from_file("data/gmd/online/Skeletal Shenanigans.gmd")
objs = lvl.objects
GROUP_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=(IDType.GROUP_ID,))
ids = GROUP_HANDLER.compile_ids(objs)
id_list = ids.get_ids()