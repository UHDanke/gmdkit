# Package Imports
from gmdkit.utils import enums
from gmdkit.serialization.classes import BaseInterface
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class VolumeInterface(BaseInterface):
    group_id_1: int = Field(51)
    group_id_2: int = Field(71)
    player_1: bool = Field(138)
    player_2: bool = Field(200)
    vol_near: float = Field(421)
    vol_med: float = Field(422)
    vol_far: float = Field(423)
    dist_1: int = Field(424)
    dist_2: int = Field(425)
    dist_3: int = Field(426)
    camera: bool = Field(428)
    direction: enums.VolumeDirection = Field(458)
    
    @property
    def dist_near(self):
        return self.dist_1
    
    @dist_near.setter
    def dist_near(self, value:float):
        d1 = self.dist_1
        d2 = self.dist_2
        
        if value != d1:
            self.dist_1 = value
            self.dist_2 = d2 + d1 - value

    @property
    def dist_med(self):
        return self.dist_1 + self.dist_2
    
    @dist_med.setter
    def dist_med(self, value:float):
        d1 = self.dist_1
        d2 = self.dist_2
        d3 = self.dist_3
        
        if value != d2:
            self.dist_2 = value - d1
            self.dist_3 = d3 + d2 - value
        
    @property
    def dist_far(self):
        return self.dist_1 + self.dist_2 + self.dist_3
    
    @dist_far.setter
    def dist_far(self, value:float):
        self.dist_3 = value - self.dist_1 - self.dist_2


class BPMTrigger(TriggerObject):
    duration: float = Field(10)
    bpm: int = Field(498)
    speed: enums.Speed = Field(499)
    disable: bool = Field(500)
    bpb: int = Field(501)


class SFXTrigger(VolumeInterface,TriggerObject):
    sfx_id: int = Field(392)
    speed: int = Field(404)
    pitch: int = Field(405)
    volume: float = Field(406)
    use_reverb: bool = Field(407)
    start: int = Field(408)
    fade_in: int = Field(409)
    end: int = Field(410)
    fade_out: int = Field(411)
    fft: bool = Field(412)
    loop: bool = Field(413)
    is_unique: bool = Field(415)
    unique_id: int = Field(416)
    override: bool = Field(420)
    pre_load: bool = Field(433)
    min_int: float = Field(434)
    sfx_group: int = Field(455)
    ignore_volume: bool = Field(489)
    sfx_duration: float = Field(490)
    reverb: enums.ReverbPreset = Field(502)
    override_reverb: bool = Field(503)
    speed_rand: int = Field(596)
    pitch_rand: int = Field(597)
    volume_rand: float = Field(598)
    pitch_steps: bool = Field(599)


class EditSFXTrigger(VolumeInterface,TriggerObject):
    duration: float = Field(10)
    sfx_id: int = Field(392)
    speed: int = Field(404)
    volume: float = Field(406)
    stop_loop: bool = Field(414)
    unique_id: int = Field(416)
    stop: bool = Field(417)
    change_volume: bool = Field(418)
    change_speed: bool = Field(419)
    sfx_group: int = Field(455)
    group_id: int = Field(457)


class SongTrigger(TriggerObject):
    song_id: int = Field(392)
    prep: bool = Field(399)
    load_prep: bool = Field(400)
    speed: int = Field(404)
    volume: float = Field(406)
    start: int = Field(408)
    fade_in: int = Field(409)
    end: int = Field(410)
    fade_out: int = Field(411)
    loop: bool = Field(413)
    song_channel: int = Field(432)
    dont_reset: bool = Field(595)


class EditSongTrigger(VolumeInterface,TriggerObject):
    duration: float = Field(10)
    speed: int = Field(404)
    volume: float = Field(406)
    stop_loop: bool = Field(414)
    stop: bool = Field(417)
    change_volume: bool = Field(418)
    change_speed: bool = Field(419)
    song_channel: int = Field(432)


# BPMTrigger
register_id(3642, BPMTrigger)  # BPM Trigger

# SFXTrigger
register_id(3602, SFXTrigger)  # SFX Trigger
register_id(3603, EditSFXTrigger)  # Edit SFX Trigger

# SongTrigger
register_id(1934, SongTrigger)  # Song Trigger
register_id(3605, EditSongTrigger)  # Edit Song Trigger
