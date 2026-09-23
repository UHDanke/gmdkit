# Package Imports
from gmdkit.utils import enums
from gmdkit.serialization.type_cast import decode_text, encode_text
from gmdkit.models.prop.list import IntList
from gmdkit.models.level import LevelMapping
from gmdkit.serialization.classes import DictField, FieldMetaclass
from gmdkit.serialization.mixins import PlistLoaderMixin


class FieldLoaderMixin(PlistLoaderMixin, metaclass=FieldMetaclass):

    list_id: int = DictField(key="k1", default=0)

    name: str = DictField(key="k2")

    description: str = DictField(
        key="k3",
        decoder=decode_text,
        encoder=encode_text
    )

    creator: str = DictField(key="k5")

    difficulty: enums.ListDifficulty = DictField(
        key="k7",
        decoder=enums.ListDifficulty,
        default=enums.ListDifficulty.NA,
    )

    downloads: int = DictField(key="k11", default=0)

    uploaded: bool = DictField(
        key="k15",
        decoder=bool,
        encoder=int,
        default=False,
    )

    version: int = DictField(key="k16", default=0)

    list_type: enums.LevelType = DictField(
        key="k21",
        decoder=enums.LevelType,
        default=enums.LevelType.LOCAL,
    )

    like_rating: int = DictField(key="k22")

    featured: bool = DictField(key="k27", default=False)

    original_id: int = DictField(key="k42")

    revision: int = DictField(key="k46", default=0)

    account_id: int = DictField(key="k60")

    unlisted: bool = DictField(key="k79", default=False)

    favorite: bool = DictField(key="k82", default=False)

    index: int = DictField(key="k83", default=0)

    friends_only: bool = DictField(key="k94", default=False)

    level_ids: IntList = DictField(
        key="k96",
        decoder=IntList.from_string,
        encoder=IntList.to_string,
        default_factory=IntList,
    )

    level_info: LevelMapping = DictField(
        key="k97",
        decoder=LevelMapping.from_node,
        encoder=LevelMapping.to_node,
        is_node=True,
        default_factory=LevelMapping,
    )

    upload_time: int = DictField(key="k98")

    update_time: int = DictField(key="k99")

    online_levels_loaded: bool = DictField(key="k100", default=False)

    diamond_reward: int = DictField(key="k113")

    levels_to_claim: int = DictField(key="k114")


FieldLoaderMixin.add_field(key="k47")
FieldLoaderMixin.add_field(key="k84")
