# Package Imports
from gmdkit.models.prop.particle import Particle
from gmdkit.models.interfaces.base import BaseObject, Field, register_id


class AnimatedMonsterObject(BaseObject):
    pass


class BaseAnimatedObject(BaseObject):
    animate_on_trigger: bool = Field(123)
    animate_active_only: bool = Field(214)


class AnimatedObject(BaseAnimatedObject):
    animation_speed: float = Field(107)
    use_speed: bool = Field(122)
    single_frame: int = Field(462)
    offset_anim: bool = Field(592)


class RandomAnimatedObject(AnimatedObject):
    randomize_start: bool = Field(106)


class DelayedAnimatedObject(RandomAnimatedObject):
    delayed_loop: bool = Field(126)


class SpecialAnimatedObject(RandomAnimatedObject):
    disable_shine: bool = Field(127)


class ExpandingAnimatedObject(BaseAnimatedObject):
    animation_speed: float = Field(107)


class ParticleObject(BaseObject):
    data: Particle = Field(145)
    use_obj_color: bool = Field(146)
    uniform_obj_color: bool = Field(147)
    quick_start: bool = Field(211)


class SpinningObject(BaseObject):
    rotation_speed: float = Field(97)
    disable_rotation: bool = Field(98)

# BaseAnimatedObject
register_id(1591, BaseAnimatedObject)  # Lava Animation 1
register_id(1593, BaseAnimatedObject)  # Lava Animation 2
 
# AnimatedMonsterObject
register_id(918, AnimatedMonsterObject)  # Large Beast Hazard
register_id(919, AnimatedMonsterObject)  # Animated Black Pit Hazard
register_id(1327, AnimatedMonsterObject)  # Small Monster Hazard
register_id(1328, AnimatedMonsterObject)  # Large Monster Hazard
register_id(1584, AnimatedMonsterObject)  # Bat Hazard
register_id(2012, AnimatedMonsterObject)  # Spiked Round Monster Hazard
 
# AnimatedObject
register_id(1050, AnimatedObject)  # Transparent Circle Wave Animation
register_id(1051, AnimatedObject)  # Transparent Sharp Wave Animation
register_id(1052, AnimatedObject)  # Transparent Inverse Circle Wave Animation
register_id(1053, AnimatedObject)  # Colored Stripes Small Square Animation
register_id(1054, AnimatedObject)  # Colored Stripes Slab Animation
register_id(1592, AnimatedObject)  # Colored Stripes Small Slab Animation
register_id(2605, AnimatedObject)  # Pixel Art 505
register_id(2694, AnimatedObject)  # Pixel Art 594
register_id(3001, AnimatedObject)  # Sharp Wave Animation
register_id(3002, AnimatedObject)  # Inverse Circle Wave Animation
register_id(4211, AnimatedObject)  # Pixel Art 1411
 
# AnimatedObject
register_id(2868, AnimatedObject)  # Small Explosion Animation
register_id(2870, AnimatedObject)  # Simple Explosion Animation
 
# RandomAnimatedObject
register_id(921, RandomAnimatedObject)  # Thin Fire Burst Animation
register_id(1516, RandomAnimatedObject)  # Waterfall Animation
register_id(1519, RandomAnimatedObject)  # Tiny Sparkle Animation
register_id(1618, RandomAnimatedObject)  # Double Ring Pulse Animation
register_id(1697, RandomAnimatedObject)  # Animated Glowing Electricity Straight
register_id(1851, RandomAnimatedObject)  # Small Splash Animation 1
register_id(1852, RandomAnimatedObject)  # Small Splash Animation 2
register_id(1854, RandomAnimatedObject)  # Drip Splash Animation
register_id(1855, RandomAnimatedObject)  # Drip Animation 2
register_id(1856, RandomAnimatedObject)  # Bubble Popping Animation
register_id(1860, RandomAnimatedObject)  # Large Glowing Electric Burst Animation
register_id(2020, RandomAnimatedObject)  # Action Lines Animation 1
register_id(2021, RandomAnimatedObject)  # Action Lines Animation 2
register_id(2022, RandomAnimatedObject)  # Slash Particle Animation 1
register_id(2024, RandomAnimatedObject)  # Shine Animation
register_id(2025, RandomAnimatedObject)  # Fan Particle Animation
register_id(2026, RandomAnimatedObject)  # Slash Particle Animation 2
register_id(2027, RandomAnimatedObject)  # Slash Particle Animation 3
register_id(2028, RandomAnimatedObject)  # Slash Particle Animation 4
register_id(2029, RandomAnimatedObject)  # Smoke Puff Animation 1
register_id(2030, RandomAnimatedObject)  # Shockwave Particle Animation 1
register_id(2031, RandomAnimatedObject)  # Shockwave Particle Animation 2
register_id(2033, RandomAnimatedObject)  # Smoke Particle Animation 1
register_id(2035, RandomAnimatedObject)  # Energy Burst Animation 1
register_id(2036, RandomAnimatedObject)  # Energy Burst Animation 2
register_id(2037, RandomAnimatedObject)  # Smoke Puff Animation 2
register_id(2038, RandomAnimatedObject)  # Energy Burst Animation 3
register_id(2039, RandomAnimatedObject)  # Smoke Puff Animation 3
register_id(2040, RandomAnimatedObject)  # Energy Burst Animation 4
register_id(2043, RandomAnimatedObject)  # Energy Burst Animation 5
register_id(2044, RandomAnimatedObject)  # Energy Burst Animation 6
register_id(2045, RandomAnimatedObject)  # Smoke Puff Animation 4
register_id(2048, RandomAnimatedObject)  # Energy Burst Animation 7
register_id(2049, RandomAnimatedObject)  # Energy Burst Animation 8
register_id(2050, RandomAnimatedObject)  # Energy Burst Animation 9
register_id(2051, RandomAnimatedObject)  # Splat Particle Animation 1
register_id(2052, RandomAnimatedObject)  # Splat Particle Animation 2
register_id(2053, RandomAnimatedObject)  # Splash Particle Animation
register_id(2054, RandomAnimatedObject)  # Fireball Particle Animation 3
register_id(2867, RandomAnimatedObject)  # Explosion Animation
register_id(2869, RandomAnimatedObject)  # Tall Explosion Animation
register_id(2871, RandomAnimatedObject)  # Tall Explosion 2 Animation
register_id(2872, RandomAnimatedObject)  # Explosive Burst Animation
register_id(2875, RandomAnimatedObject)  # Shooting Star Animation
register_id(2876, RandomAnimatedObject)  # Swoosh Animation
register_id(2877, RandomAnimatedObject)  # Center Explosion Animation
register_id(2878, RandomAnimatedObject)  # Slither Animation
register_id(2880, RandomAnimatedObject)  # Swoosh 2 Animation
register_id(2882, RandomAnimatedObject)  # Electric Burst Animation
register_id(2883, RandomAnimatedObject)  # Electric Burst 2 Animation
register_id(2885, RandomAnimatedObject)  # Electric Burst 3 Animation
register_id(2886, RandomAnimatedObject)  # Electric Burst 4 Animation
register_id(2887, RandomAnimatedObject)  # Electric Burst 5 Animation
 
# DelayedAnimatedObject
register_id(920, DelayedAnimatedObject)  # Large Fire Animation
register_id(923, DelayedAnimatedObject)  # Thin Fire 1 Animation
register_id(924, DelayedAnimatedObject)  # Thin Fire 2 Animation
register_id(1518, DelayedAnimatedObject)  # Waterfall Splash Animation
register_id(1583, DelayedAnimatedObject)  # Moving Fireball
register_id(1698, DelayedAnimatedObject)  # Animated Glowing Electricity Bent
register_id(1699, DelayedAnimatedObject)  # Animated Glowing Electricity End
register_id(1849, DelayedAnimatedObject)  # Splash Animation 1
register_id(1850, DelayedAnimatedObject)  # Splash Animation 2
register_id(1853, DelayedAnimatedObject)  # Drip Animation 1
register_id(1857, DelayedAnimatedObject)  # Large Animated Glowing Electricity
register_id(1858, DelayedAnimatedObject)  # Several Drips Animation
register_id(1936, DelayedAnimatedObject)  # Evaporating Blobs Animation 1
register_id(1937, DelayedAnimatedObject)  # Evaporating Blobs Animation 2
register_id(1938, DelayedAnimatedObject)  # Evaporating Blobs Animation 3
register_id(1939, DelayedAnimatedObject)  # Evaporating Blobs Animation 4
register_id(2023, DelayedAnimatedObject)  # Small Animated Fireball
register_id(2032, DelayedAnimatedObject)  # Animated Energy Ball
register_id(2034, DelayedAnimatedObject)  # Small Flame Animation
register_id(2041, DelayedAnimatedObject)  # Gradient Smoke Animation
register_id(2042, DelayedAnimatedObject)  # Angled Gradient Smoke Animation
register_id(2223, DelayedAnimatedObject)  # Pixel Art 123
register_id(2246, DelayedAnimatedObject)  # Pixel Art 146
register_id(2629, DelayedAnimatedObject)  # Large Animated Fire Pixel Art
register_id(2630, DelayedAnimatedObject)  # Tiny Animated Fire Pixel Art
register_id(2864, DelayedAnimatedObject)  # Wide Flame Animation
register_id(2865, DelayedAnimatedObject)  # Flame Animation
register_id(2873, DelayedAnimatedObject)  # Fireball Animation
register_id(2874, DelayedAnimatedObject)  # Small Fireball Animation
register_id(2879, DelayedAnimatedObject)  # Fireball 2 Animation
register_id(2881, DelayedAnimatedObject)  # Smoking Animation
register_id(2884, DelayedAnimatedObject)  # Electricity Animation
register_id(2888, DelayedAnimatedObject)  # Electricity 2 Animation
register_id(2889, DelayedAnimatedObject)  # Electricity 3 Animation
register_id(2890, DelayedAnimatedObject)  # Electricity Wobble Animation
register_id(2891, DelayedAnimatedObject)  # Electricity Stable Animation
register_id(2892, DelayedAnimatedObject)  # Electricity Circle Animation
register_id(2893, DelayedAnimatedObject)  # Electricity Square Animation
register_id(2894, DelayedAnimatedObject)  # Laser Wobble Animation
register_id(3119, DelayedAnimatedObject)  # Pixel Art 619
register_id(3120, DelayedAnimatedObject)  # Pixel Art 620
register_id(3121, DelayedAnimatedObject)  # Pixel Art 621
register_id(3219, DelayedAnimatedObject)  # Pixel Art 719
register_id(3303, DelayedAnimatedObject)  # Tiny Animated Fire Pixel Art
register_id(3304, DelayedAnimatedObject)  # Tiny Animated Fire Pixel Art
register_id(3482, DelayedAnimatedObject)  # Small Animated Fire Pixel Art
register_id(3483, DelayedAnimatedObject)  # Medium Animated Fire Pixel Art
register_id(3484, DelayedAnimatedObject)  # Large Animated Fire Pixel Art
register_id(3492, DelayedAnimatedObject)  # Pixel Art 992
register_id(3493, DelayedAnimatedObject)  # Pixel Art 993
register_id(4300, DelayedAnimatedObject)  # Pixel Art 1500
 
# SpecialAnimatedObject
register_id(2046, SpecialAnimatedObject)  # Fireball Particle Animation 1
register_id(2047, SpecialAnimatedObject)  # Fireball Particle Animation 2
register_id(2055, SpecialAnimatedObject)  # Explosion Animation
 
# ExpandingAnimatedObject
register_id(1839, ExpandingAnimatedObject)  # Large Hollow Expanding Circle Animation
register_id(1840, ExpandingAnimatedObject)  # Small Hollow Expanding Circle Animation
register_id(1841, ExpandingAnimatedObject)  # Large Expanding Circle Animation
register_id(1842, ExpandingAnimatedObject)  # Small Expanding Circle Animation
 
# SpinningObject
register_id(1582, SpinningObject)  # Rotating Fireball
register_id(1705, SpinningObject)  # Large Saw Blade
register_id(1706, SpinningObject)  # Medium Saw Blade
register_id(1707, SpinningObject)  # Small Saw Blade
register_id(1708, SpinningObject)  # Large Spike Blade
register_id(1709, SpinningObject)  # Medium Spike Blade
register_id(1710, SpinningObject)  # Small Spike Blade
register_id(1734, SpinningObject)  # Large Gear Blade
register_id(1735, SpinningObject)  # Medium Gear Blade
register_id(1736, SpinningObject)  # Small Gear Blade
register_id(186, SpinningObject)  # Large Outline Blade
register_id(187, SpinningObject)  # Medium Outline Blade
register_id(188, SpinningObject)  # Small Outline Blade
register_id(740, SpinningObject)  # Large Invisible Blade
register_id(741, SpinningObject)  # Medium Invisible Blade
register_id(742, SpinningObject)  # Small Invisible Blade
register_id(678, SpinningObject)  # Large Colored Gear
register_id(679, SpinningObject)  # Medium Colored Gear
register_id(680, SpinningObject)  # Small Colored Gear
register_id(1619, SpinningObject)  # Large Scythe Blade
register_id(1620, SpinningObject)  # Small Scythe Blade
register_id(1701, SpinningObject)  # Spiked Square Hazard
register_id(1702, SpinningObject)  # Spiked Circle Hazard
register_id(1703, SpinningObject)  # Triangle Hazard
register_id(183, SpinningObject)  # Large Blade
register_id(184, SpinningObject)  # Medium Blade
register_id(185, SpinningObject)  # Small Blade
register_id(85, SpinningObject)  # Large Decorative Gear
register_id(86, SpinningObject)  # Medium Decorative Gear
register_id(87, SpinningObject)  # Small Decorative Gear
register_id(97, SpinningObject)  # Very Small Decorative Gear
register_id(137, SpinningObject)  # Large Wheel
register_id(138, SpinningObject)  # Medium Wheel
register_id(139, SpinningObject)  # Small Wheel
register_id(154, SpinningObject)  # Large Spike Wheel
register_id(155, SpinningObject)  # Medium Spike Wheel
register_id(156, SpinningObject)  # Small Spike Wheel
register_id(180, SpinningObject)  # Large Cartwheel
register_id(181, SpinningObject)  # Medium Cartwheel
register_id(182, SpinningObject)  # Small Cartwheel
register_id(222, SpinningObject)  # Large Round Cloud
register_id(223, SpinningObject)  # Medium Round Cloud
register_id(224, SpinningObject)  # Small Round Cloud
register_id(375, SpinningObject)  # Large Rotating Arm
register_id(376, SpinningObject)  # Medium Rotating Arm
register_id(377, SpinningObject)  # Small Rotating Arm
register_id(378, SpinningObject)  # Very Small Rotating Arm
register_id(1521, SpinningObject)  # Large Jointless Arm
register_id(1522, SpinningObject)  # Medium Jointless Arm
register_id(1523, SpinningObject)  # Small Jointless Arm
register_id(1524, SpinningObject)  # Very Small Jointless Arm
register_id(1525, SpinningObject)  # Large Rotating Particle
register_id(1526, SpinningObject)  # Medium Rotating Particle
register_id(1527, SpinningObject)  # Small Rotating Particle
register_id(1528, SpinningObject)  # Very Small Rotating Particle
register_id(394, SpinningObject)  # Large Rotating Hexagon
register_id(395, SpinningObject)  # Medium Rotating Hexagon
register_id(396, SpinningObject)  # Small Rotating Hexagon
register_id(997, SpinningObject)  # Large Split Circle
register_id(998, SpinningObject)  # Medium Split Circle
register_id(999, SpinningObject)  # Small Split Circle
register_id(1000, SpinningObject)  # Very Small Split Circle
register_id(1019, SpinningObject)  # Large Rotating Shine
register_id(1020, SpinningObject)  # Medium Rotating Shine
register_id(1021, SpinningObject)  # Small Rotating Shine
register_id(1055, SpinningObject)  # Rotating Pulsing Rings with One Dot
register_id(1056, SpinningObject)  # Rotating Pulsing Rings with Two Dots
register_id(1057, SpinningObject)  # Rotating Pulsing Rings with Four Dots
register_id(1058, SpinningObject)  # Large Swirl
register_id(1059, SpinningObject)  # Medium Swirl
register_id(1060, SpinningObject)  # Small Swirl
register_id(1061, SpinningObject)  # Very Small Swirl
register_id(1752, SpinningObject)  # Triangle Swirl
register_id(1831, SpinningObject)  # Large Rotating Hollow Quarter Circle
register_id(1832, SpinningObject)  # Small Rotating Hollow Quarter Circle
register_id(1833, SpinningObject)  # Large Rotating Quarter Circle
register_id(1834, SpinningObject)  # Small Rotating Quarter Circle
 
# ParticleObject
register_id(2065, ParticleObject)  # Custom Particles