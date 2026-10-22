from typing import Any

from gmdkit.utils.types import DictClass, ListClass
from gmdkit.utils import enums
from gmdkit.serialization.functions import kv_wrap
from gmdkit.serialization.mixins import PlistDecoderMixin, PlistLoaderMixin
from gmdkit.serialization.classes import DictField, FieldMetaclass


class RewardObject(PlistLoaderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    HAS_NODES = True
    KEY_DECODER = int
    KEY_ENCODER = str
    ENCODER_KEY = 9

    item: enums.SpecialRewardItem = DictField(key=1, decoder=enums.SpecialRewardItem.from_string, encoder=int)
    item_id: int = DictField(key=2, default=0)
    amount: int = DictField(key=3, default=0)
    unlock_type: enums.UnlockType = DictField(
        key=4, decoder=enums.UnlockType.from_string, encoder=int, default=enums.UnlockType.NONE
        )


class RewardObjectList(PlistLoaderMixin, ListClass[RewardObject]):
    IS_ARRAY = True
    DECODER = RewardObject.from_node
    ENCODER = RewardObject.to_node


class RewardItem(PlistLoaderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    HAS_NODES = True
    KEY_DECODER = int
    KEY_ENCODER = str
    ENCODER_KEY = 8

    chest_id: int = DictField(key=1, default=0)
    reward_type: enums.RewardType = DictField(
        key=2, decoder=enums.RewardType.from_string, encoder=int, default=enums.RewardType.UNKNOWN
        )
    rewards: RewardObjectList = DictField(
        key=3,
        default_factory=RewardObjectList,
        decoder=RewardObjectList.from_node,
        encoder=RewardObjectList.to_node,
        is_node=True,
    )


class RewardItemDict(PlistDecoderMixin, DictClass[str, RewardItem]):
    DECODER = staticmethod(kv_wrap(None, RewardItem.from_node))
    ENCODER = staticmethod(kv_wrap(None, RewardItem.to_node))


class IntRewardItemDict(PlistDecoderMixin, DictClass[int, RewardItem]):
    DECODER = staticmethod(kv_wrap(int, RewardItem.from_node))
    ENCODER = staticmethod(kv_wrap(str, RewardItem.to_node))


class ChallengeItem(PlistLoaderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    HAS_NODES = True
    KEY_DECODER = int
    KEY_ENCODER = str
    ENCODER_KEY = 7

    challenge_type: enums.ChallengeType = DictField(
        key=1, decoder=enums.ChallengeType.from_string, encoder=int, default=enums.ChallengeType.UNKNOWN
        )
    progress: int = DictField(key=2, default=0)
    goal: int = DictField(key=3, default=0)
    reward: int = DictField(key=4, default=0)
    time_left: int = DictField(key=5, default=0)
    can_claim: bool = DictField(key=6, default=False)
    name: str = DictField(key=7, default="")
    position: int = DictField(key=8, default=0)


class ChallengeDict(PlistDecoderMixin, DictClass[int, ChallengeItem]):
    DECODER = staticmethod(kv_wrap(int, ChallengeItem.from_node))
    ENCODER = staticmethod(kv_wrap(str, ChallengeItem.to_node))