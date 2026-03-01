# Package Imports
from gmdkit.models.level import LevelMapping
from gmdkit.models.level_pack import LevelPackList
from gmdkit.models.template import SmartTemplateList
from gmdkit.models.object import ObjectGroupDict
from gmdkit.models.prop.dpad import MoveButton, JumpButton, SingleLayout, DualLayout
from gmdkit.models.prop.song_info import SongInfoList

GAME_SAVE_DECODERS = {
    "customObjectDict": ObjectGroupDict.from_node,
    "GLM_01": LevelMapping.from_node,
    "GLM_03": LevelMapping.from_node,
    "GLM_10": LevelMapping.from_node,
    "GLM_16": LevelMapping.from_node,
    "GLM_20": SmartTemplateList.from_node,
    "GLM_22": LevelPackList.from_node,
    "dpad01": MoveButton.from_string,
    "dpad02": MoveButton.from_string,
    "dpad03": MoveButton.from_string,
    "dpad04": JumpButton.from_string,
    "dpad05": JumpButton.from_string,
    "dpadLayout01": SingleLayout.from_string,
    "dpadLayout02": SingleLayout.from_string,
    "dpadLayout03": SingleLayout.from_string,
    "dpadLayoutDual01": DualLayout.from_string,
    "dpadLayoutDual02": DualLayout.from_string,
    "dpadLayoutDual03": DualLayout.from_string,
    "MDLM_001": SongInfoList.from_node,
    }


GAME_SAVE_ENCODERS = {
    "customObjectDict": ObjectGroupDict.to_node,
    "GLM_01": LevelMapping.to_node,
    "GLM_03": LevelMapping.to_node,
    "GLM_10": LevelMapping.to_node,
    "GLM_16": LevelMapping.to_node,
    "GLM_20": SmartTemplateList.to_node,
    "GLM_22": LevelPackList.to_node,
    "dpad01": MoveButton.to_string,
    "dpad02": MoveButton.to_string,
    "dpad03": MoveButton.to_string,
    "dpad04": JumpButton.to_string,
    "dpad05": JumpButton.to_string,
    "dpadLayout01": SingleLayout.to_string,
    "dpadLayout02": SingleLayout.to_string,
    "dpadLayout03": SingleLayout.to_string,
    "dpadLayoutDual01": DualLayout.to_string,
    "dpadLayoutDual02": DualLayout.to_string,
    "dpadLayoutDual03": DualLayout.to_string,
    "MDLM_001": SongInfoList.to_node,
    }


GAME_SAVE_NODES = {"customObjectDict","GLM_01","GLM_03","GLM_10","GLM_16","GLM_20","GLM_22","MDLM_001"}
