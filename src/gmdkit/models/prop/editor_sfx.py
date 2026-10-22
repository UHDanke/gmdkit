# Imports
from typing import Any

# Package Imports
from gmdkit.utils.types import ListClass, DictClass
from gmdkit.utils import enums
from gmdkit.serialization.mixins import (
    ArrayDecoderMixin, DataclassDecoderMixin, DelimiterMixin, DictDecoderMixin
    )
from gmdkit.serialization.functions import dataclass_decoder, field_decoder
from gmdkit.serialization.classes import FieldMetaclass, DictField
from gmdkit.serialization.type_cast import to_bool, from_bool, from_float, serialize
from gmdkit.models.custom_sfx import CustomSFXMappingList


class EditorSFXSound(DictDecoderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    SEPARATOR = ","
    KEY_DECODER = int
    KEY_ENCODER = str
    DEFAULT_DECODER = None
    DEFAULT_ENCODER = staticmethod(serialize)

    sfx_id: int = DictField(key=1, decoder=int, default=0)                                          
    volume: float = DictField(key=2, decoder=float, encoder=from_float, default=1.0)                
    speed: int = DictField(key=3, decoder=int, default=0)                                           
    pitch: int = DictField(key=4, decoder=int, default=0)                                           
    start: int = DictField(key=5, decoder=int, default=0)                                           
    end: int = DictField(key=6, decoder=int, default=0)                                             
    fade_in: int = DictField(key=7, decoder=int, default=0)                                        
    fade_out: int = DictField(key=8, decoder=int, default=0)                                       
    min_interval: float = DictField(key=9, decoder=float, encoder=from_float, default=0.0)         
    speed_rand: int = DictField(key=10, decoder=int, default=0)                                    
    pitch_rand: int = DictField(key=11, decoder=int, default=0)                                    
    volume_rand: float = DictField(key=12, decoder=float, encoder=from_float, default=0.0)        
    pitch_steps: bool = DictField(key=13, decoder=to_bool, encoder=from_bool, default=False)      
    fft: bool = DictField(key=14, decoder=to_bool, encoder=from_bool, default=False)              
    custom_library_id: int = DictField(key=15, decoder=int, default=0)                            
    use_reverb: bool = DictField(key=16, decoder=to_bool, encoder=from_bool, default=False)       


class EditorSFXSoundList(ArrayDecoderMixin, ListClass[EditorSFXSound]):

    __slots__ = ()

    SEPARATOR = ":"
    DECODER = EditorSFXSound.from_string
    ENCODER = EditorSFXSound.to_string


class EditorSFXBinding(DictDecoderMixin, DictClass[int, Any], metaclass=FieldMetaclass):
    SEPARATOR = ","
    KEY_DECODER = int
    KEY_ENCODER = str
    DEFAULT_DECODER = None
    DEFAULT_ENCODER = staticmethod(serialize)

    action: enums.EditorSFXAction = DictField(
        key=1, decoder=enums.EditorSFXAction.from_string, default=enums.EditorSFXAction.PLACE_ANY
        )
    play_mode: enums.EditorSFXPlayMode = DictField(
        key=2, decoder=enums.EditorSFXPlayMode.from_string, default=enums.EditorSFXPlayMode.RANDOM
        )
    min_interval: float = DictField(key=3, decoder=float, encoder=from_float, default=0.0)
    

@dataclass_decoder(slots=True, from_array=True, separator=";")
class EditorSFXSoundBinding(DataclassDecoderMixin):
    binding: EditorSFXBinding = field_decoder(decoder=EditorSFXBinding.from_string,encoder=EditorSFXBinding.to_string,default_factory=EditorSFXBinding)
    sounds: EditorSFXSoundList = field_decoder(
        decoder=EditorSFXSoundList.from_string,
        encoder=EditorSFXSoundList.to_string,
        default_factory=EditorSFXSoundList,
        )

class EditorSFXSoundBindingList(DelimiterMixin, ArrayDecoderMixin, ListClass[EditorSFXBinding]):
    __slots__ = ()

    SEPARATOR = ";"
    END_DELIMITER = ";"
    GROUP_SIZE = 2
    DECODER = EditorSFXSoundBinding.from_tokens
    ENCODER = EditorSFXSoundBinding.to_tokens

    def get_action(self, action: int):
        for b in self:
            if b.binding.action == action:
                return b
        return None


@dataclass_decoder(slots=True, from_array=True, separator="M|")
class EditorSFXBindingMapping(DataclassDecoderMixin):

    bindings: EditorSFXSoundBindingList = field_decoder(
        default_factory=EditorSFXSoundBindingList,
        decoder=EditorSFXSoundBindingList.from_string, encoder=EditorSFXSoundBindingList.to_string
        )
    mappings: CustomSFXMappingList = field_decoder(
        default_factory=CustomSFXMappingList,
        decoder=CustomSFXMappingList.from_string, encoder=CustomSFXMappingList.to_string,
        optional=True
        )


@dataclass_decoder(slots=True, from_array=True, separator=";",max_split=1)
class EditorSFXString(DataclassDecoderMixin):

    version: int = 1
    sfx_data: EditorSFXBindingMapping = field_decoder(
        default_factory=EditorSFXBindingMapping, 
        decoder=EditorSFXBindingMapping.from_string, 
        encoder=EditorSFXBindingMapping.to_string
        )