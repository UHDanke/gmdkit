from gmdkit.remapping.rules import BASE_ID_HANDLER
from gmdkit.remapping import IDType
from gmdkit import Level


def test_group_ids():
    lvl = Level.from_gmd("data/gmd/online/Skeletal Shenanigans.gmd")
    objs = lvl.objects
    GROUP_HANDLER = BASE_ID_HANDLER.compile_rules(id_types=(IDType.GROUP_ID,))
    ids = GROUP_HANDLER.compile_ids(objs)
    id_list = ids[IDType.GROUP_ID].get_ids()
    assert id_list
    assert id_list == ids.all.get_ids()