# Package Imports
from gmdkit.models.level import LevelList
from gmdkit.models.level_pack import LevelPackList
from gmdkit.serialization.classes import DictField,FieldMetaclass
from gmdkit.serialization.mixins import PlistLoaderMixin


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):

    levels: LevelList = DictField(
        key="LLM_01",
        default_factory=LevelList,
        decoder=LevelList.from_node,
        encoder=LevelList.to_node,
        is_node=True,
        pass_kwargs=True,
    )

    binary: int = DictField(
        key="LLM_02"
        )

    lists: LevelPackList = DictField(
        key="LLM_03",
        default_factory=LevelPackList,
        decoder=LevelPackList.from_node,
        encoder=LevelPackList.to_node,
        is_node=True,
        pass_kwargs=True,
    )
