# Package Imports
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList


LEVEL_SAVE_DECODER = {
    "LLM_01": LevelList.from_node,
    "LLM_03": LevelPackList.from_node    
    }

LEVEL_SAVE_ENCODER = {
    "LLM_01": LevelList.to_node,
    "LLM_03": LevelPackList.to_node   
    }

LEVEL_SAVE_NODES = {"LLM_01","LLM_03"}