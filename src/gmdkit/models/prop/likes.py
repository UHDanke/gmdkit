# Imports
from typing import Any, ClassVar, Iterator, Optional, Type, TypeVar, Union, overload
from dataclasses import MISSING
import xml.etree.ElementTree as ET


# Package Imports
from gmdkit.utils.types import ListClass
from gmdkit.utils import enums
from gmdkit.serialization.classes import AliasField, BaseInterface
from gmdkit.serialization.functions import validate_dict_node
from gmdkit.serialization.type_cast import to_bool, from_bool
from gmdkit.serialization.mixins import PlistDecoderMixin, DataclassDecoderMixin, DelimiterMixin
from gmdkit.serialization.functions import dataclass_decoder, field_decoder


I = TypeVar("I", bound="LikeInterface")
T = TypeVar("T")


@dataclass_decoder(slots=True, separator="_", from_array=True)
class LikeData(DelimiterMixin, DataclassDecoderMixin):
    START_DELIMITER = "like_"
    DEFAULT_SCHEMA: ClassVar[Type[BaseInterface]] = BaseInterface
    _VIEW_REGISTRY: ClassVar[dict] = {}
 
    item_type: enums.LikeItemType = field_decoder(decoder=enums.LikeItemType.from_string)
    item_id: int
    like: bool = field_decoder(decoder=to_bool, encoder=from_bool)
    special: int = 0
 
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
 
    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)
 
    def __contains__(self, key: str) -> bool:
        return key in self.__dataclass_fields__
 
    @classmethod
    def register_type(cls, item_type: enums.LikeItemType, schema: BaseInterface):
        cls._VIEW_REGISTRY[enums.LikeItemType(item_type)] = schema
 
    @classmethod
    def get_schema(cls, item_type=None) -> Type["LikeInterface"]:
        return cls._VIEW_REGISTRY.get(item_type, cls.DEFAULT_SCHEMA)
 
    @property
    def interface(self) -> "LikeInterface":
        return type(self).get_schema(self.item_type)(self)
 
    @overload
    def require_interface(self, cls: Type[I]) -> I: ...
    @overload
    def require_interface(self, cls: Type[I], fallback: T) -> Union[I, T]: ...
    def require_interface(self, cls, fallback=MISSING):
        schema = type(self).get_schema(self.item_type)
        if issubclass(schema, cls):
            return schema(self)
        if fallback is not MISSING:
            return fallback
        raise TypeError(f"{self.item_type!r} like has interface {schema.__name__}, not {cls.__name__}")
 
 
Field = AliasField


class LikeInterface(BaseInterface):
    item_type: enums.LikeItemType = Field("item_type")
    item_id: int = Field("item_id")
    like: bool = Field("like")
    special: int = Field("special")

    @property
    def dislike(self) -> bool:
        return not self.like

    @dislike.setter
    def dislike(self, value: bool):
        self.like = not value

    @classmethod
    def new(cls, item_id: int, like: bool = True, special: int = 0) -> LikeData:
        if cls.ITEM_TYPE is None:
            raise TypeError(f"{cls.__name__} has no item type")
        return LikeData(cls.ITEM_TYPE, item_id, like, special)


class LevelLike(LikeInterface):
    level_id: int = Field("item_id")


class LevelCommentLike(LikeInterface):
    comment_id: int = Field("item_id")
    level_id: int = Field("special")

    @property
    def is_list_comment(self) -> bool:
        return self.special < 0

    @property
    def list_id(self) -> Optional[int]:
        return -self.special if self.special < 0 else None

    @list_id.setter
    def list_id(self, value: int):
        self.special = -abs(value)


class AccountCommentLike(LikeInterface):
    ITEM_TYPE = enums.LikeItemType.ACCOUNT_COMMENT
    comment_id: int = Field("item_id")
    account_id: int = Field("special")


class ListLike(LikeInterface):
    ITEM_TYPE = enums.LikeItemType.LIST
    list_id: int = Field("item_id")


class SoundPackLike(LikeInterface):
    ITEM_TYPE = enums.LikeItemType.SOUND_PACK
    sound_pack_id: int = Field("item_id")


class SoundPackCommentLike(LikeInterface):
    ITEM_TYPE = enums.LikeItemType.SOUND_PACK_COMMENT
    comment_id: int = Field("item_id")


class ModRoomCommentLike(LikeInterface):
    comment_id: int = Field("item_id")
    level_id: int = Field("special")


class ModRoomLevelCommentLike(ModRoomCommentLike):
    ITEM_TYPE = enums.LikeItemType.MOD_ROOM_LEVEL_COMMENT


class ModRoomUserCommentLike(ModRoomCommentLike):
    ITEM_TYPE = enums.LikeItemType.MOD_ROOM_USER_COMMENT


LikeData.DEFAULT_SCHEMA = LikeInterface
LikeData.register_type(enums.LikeItemType.LEVEL, LevelLike)
LikeData.register_type(enums.LikeItemType.LEVEL_COMMENT, LevelCommentLike)
LikeData.register_type(enums.LikeItemType.ACCOUNT_COMMENT, AccountCommentLike)
LikeData.register_type(enums.LikeItemType.LIST, ListLike)
LikeData.register_type(enums.LikeItemType.SOUND_PACK, SoundPackLike)
LikeData.register_type(enums.LikeItemType.SOUND_PACK_COMMENT, SoundPackCommentLike)
LikeData.register_type(enums.LikeItemType.MOD_ROOM_LEVEL_COMMENT, ModRoomCommentLike)
LikeData.register_type(enums.LikeItemType.MOD_ROOM_USER_COMMENT, ModRoomCommentLike)


class LikeList(PlistDecoderMixin, ListClass[LikeData]):
    DECODER = staticmethod(LikeData.from_string)
    ENCODER = staticmethod(LikeData.to_string)

    def load_data(self, node: ET.Element, decoder=None, **kwargs):
        decoder = type(self).DECODER if decoder is None else decoder

        try:
            validate_dict_node(node)
        except Exception as e:
            raise RuntimeError(f"[{type(self).__name__}] failed to validate node") from e

        self.clear()
        append = self.append
        if kwargs:
            for i in range(0, len(node), 2):
                append(decoder(node[i].text, **kwargs))
        else:
            for i in range(0, len(node), 2):
                append(decoder(node[i].text))

    def save_data(self, encoder=None, **kwargs) -> ET.Element:
        encoder = type(self).ENCODER if encoder is None else encoder
        node = ET.Element("d")
        sub = ET.SubElement
        seen = set()
        for item in self:
            key = encoder(item, **kwargs)
            if key in seen:
                continue
            seen.add(key)
            sub(node, "k").text = key
            sub(node, "s").text = "1"
        return node

    def interfaces(self, cls: Type[I] = LikeInterface) -> Iterator[I]:
        for item in self:
            view = item.require_interface(cls, None)
            if view is not None:
                yield view

    def find(self, item_type: enums.LikeItemType, item_id: int, special: int = 0) -> Optional[LikeData]:
        for item in self:
            if item.item_type == item_type and item.item_id == item_id and item.special == special:
                return item
        return None

    def get_vote(self, item_type: enums.LikeItemType, item_id: int, special: int = 0) -> Optional[bool]:
        item = self.find(item_type, item_id, special)
        return None if item is None else item.like

    def add_vote(self, item_type: enums.LikeItemType, item_id: int, like: bool, special: int = 0) -> bool:
        if self.find(item_type, item_id, special) is not None:
            return False
        if len(self) >= 1000:
            del self[0]
        self.append(LikeData(enums.LikeItemType(item_type), item_id, like, special))
        return True