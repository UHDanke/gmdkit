# Imports
from dataclasses import dataclass
from typing import get_type_hints

# Package Imports
from gmdkit.models.serialization import DataclassDecoderMixin, dict_cast


@dataclass(slots=True)
class Particle(DataclassDecoderMixin):
    
    SEPARATOR = 'a'
    DICT_FORMAT = False
    
    max_particles: int = 0
    duration: float = 0
    lifetime: float = 0
    lifetime_rand: float = 0
    emission: int = 0
    angle: int = 0
    angle_rand: int = 0
    speed: int = 0
    speed_rand: int = 0
    posvar_x: int = 0
    posvar_y: int = 0
    gravity_x: int = 0
    gravity_y: int = 0
    accelrad: int = 0
    accelrad_rand: int = 0
    acceltan: int = 0
    acceltan_rand: int = 0
    startsize: int = 0
    startsize_rand: int = 0
    startspin: int = 0
    startspin_rand: int = 0
    startr: float = 0
    startr_rand: float = 0
    startg: float = 0
    startg_rand: float = 0
    startb: float = 0
    startb_rand: float = 0
    starta: float = 0
    starta_rand: float = 0
    endsize: int = 0
    endsize_rand: int = 0
    endspin: int = 0
    endspin_rand: int = 0
    endr: float = 0
    endr_rand: float = 0
    endg: float = 0
    endg_rand: float = 0
    endb: float = 0
    endb_rand: float = 0
    enda: float = 0
    enda_rand: float = 0
    fade_in: float = 0
    fade_in_rand: float = 0
    fade_out: float = 0
    fade_out_rand: float = 0
    startrad: int = 0
    startrad_rand: int = 0
    endrad: int = 0
    endrad_rand: int = 0
    rotsec: int = 0
    rotsec_rand: int = 0
    mode: int = 0
    mode_2: int = 0
    additive: bool = False
    start_spin_eq_end: bool = False
    start_rot_is_dir: bool = False
    dynamic_rotation: bool = False
    texture: int = 0
    uniform_obj_color: bool = False
    frictionp: float = 0
    frictionp_rand: float = 0
    respawn: float = 0
    respawn_rand: float = 0
    order_sensitive: bool = False
    start_size_eq_end: bool = False
    start_rad_eq_end: bool = False
    startrgb_var_sync: bool = False
    endrgb_var_sync: bool = False
    frictions: float = 0
    frictions_rand: float = 0
    frictionr: float = 0
    frictionr_rand: float = 0
    
    
Particle.DECODER = staticmethod(dict_cast(
    {
     key: (lambda x: bool(int(x))) if func is bool else func
     for key, func in get_type_hints(Particle).items()
     }
    ))