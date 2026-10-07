# Package Imports
from gmdkit.utils import enums
from gmdkit.models.interfaces.base import TriggerObject, Field, register_id


class ShaderTrigger(TriggerObject):
    
    def fix_color(self) -> None:        
        super().fix_color()
        self.color_1 = enums.ColorID.WHITE


class ShaderOptions(ShaderTrigger):
    ignore_player_particles: bool = Field(188)
    disable_all: bool = Field(192)
    layer_min: enums.GradientLayer = Field(196)
    layer_max: enums.GradientLayer = Field(197)


class BulgeShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    bulge: float = Field(176)
    radius: float = Field(180)
    target: bool = Field(188)
    player_2: bool = Field(200)
    screen_offset_x: float = Field(290)
    screen_offset_y: float = Field(291)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class ChromaticShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target_x: float = Field(180)
    use_x: bool = Field(188)
    target_y: float = Field(189)
    use_y: bool = Field(190)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class ChromaticGlitchShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    speed: float = Field(175)
    strength: float = Field(176)
    line_thickness: float = Field(179)
    rgb_offset: float = Field(180)
    segment_height: float = Field(189)
    line_strength: float = Field(191)
    disable: bool = Field(192)
    relative_pos: bool = Field(194)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class EditColorShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    cb: float = Field(175)
    cr: float = Field(176)
    br: float = Field(179)
    bg: float = Field(180)
    bb: float = Field(189)
    cg: float = Field(191)
    disable_preview: bool = Field(531)


class GlitchShader(ShaderTrigger):
    duration: float = Field(10)
    speed: float = Field(175)
    strength: float = Field(176)
    slice_height: float = Field(179)
    max_col_x_offset: float = Field(181)
    max_col_y_offset: float = Field(182)
    max_slice_x_offset: float = Field(191)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class GrayScaleShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    tint_channel: int = Field(51)
    ease_rate: float = Field(85)
    target: float = Field(176)
    use_lum: bool = Field(188)
    use_tint: bool = Field(190)
    disable_preview: bool = Field(531)


class HueShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    degrees: float = Field(176)
    disable_preview: bool = Field(531)


class InvertColorShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target: float = Field(176)
    red: float = Field(179)
    green: float = Field(180)
    edit_rgb: bool = Field(188)
    blue: float = Field(189)
    tween_rgb: bool = Field(190)
    clamp_rgb: bool = Field(194)
    disable_preview: bool = Field(531)


class LensCircleShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    tint_channel: int = Field(71)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    strength: float = Field(176)
    size: float = Field(179)
    fade: float = Field(181)
    player_2: bool = Field(200)
    screen_offset_x: float = Field(290)
    screen_offset_y: float = Field(291)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class MotionBlurShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ref_channel: int = Field(71)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    intensity: float = Field(176)
    target_x: float = Field(180)
    fade: float = Field(181)
    use_x: bool = Field(188)
    target_y: float = Field(189)
    use_y: bool = Field(190)
    follow_ease: float = Field(191)
    dual_dir: bool = Field(194)
    player_2: bool = Field(200)
    center: bool = Field(201)
    relative: bool = Field(514)
    empty_only: bool = Field(515)
    disable_preview: bool = Field(531)


class PinchShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    modifier: float = Field(179)
    target_x: float = Field(180)
    target: bool = Field(188)
    use_x: bool = Field(190)
    use_y: bool = Field(194)
    player_2: bool = Field(200)
    screen_offset_x: float = Field(290)
    screen_offset_y: float = Field(291)
    radius: float = Field(512)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class PixelateShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target_x: float = Field(180)
    use_x: bool = Field(188)
    target_y: float = Field(189)
    use_y: bool = Field(190)
    snap_grid: bool = Field(194)
    relative: bool = Field(514)
    hard_edges: bool = Field(515)
    disable_preview: bool = Field(531)


class RadialBlurShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ref_channel: int = Field(71)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    intensity: float = Field(176)
    size: float = Field(179)
    fade: float = Field(181)
    target: bool = Field(188)
    player_2: bool = Field(200)
    screen_offset_x: float = Field(290)
    screen_offset_y: float = Field(291)
    empty_only: bool = Field(515)
    disable_preview: bool = Field(531)


class SepiaShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target: float = Field(176)
    disable_preview: bool = Field(531)


class ShockLineShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    speed: float = Field(175)
    strength: float = Field(176)
    time_offset: float = Field(177)
    wave_width: float = Field(179)
    thickness: float = Field(180)
    fade_in: float = Field(181)
    fade_out: float = Field(182)
    invert: bool = Field(184)
    flip: bool = Field(185)
    rotate: bool = Field(186)
    dual: bool = Field(187)
    target: bool = Field(188)
    follow: bool = Field(190)
    player_2: bool = Field(200)
    screen_offset: float = Field(290)
    max_size: float = Field(512)
    animate: bool = Field(513)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class ShockwaveShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    center_id: int = Field(51)
    ease_rate: float = Field(85)
    player_1: bool = Field(138)
    speed: float = Field(175)
    strength: float = Field(176)
    time_offset: float = Field(177)
    wave_width: float = Field(179)
    thickness: float = Field(180)
    fade_in: float = Field(181)
    fade_out: float = Field(182)
    inner: float = Field(183)
    invert: bool = Field(184)
    target: bool = Field(188)
    follow: bool = Field(190)
    outer: float = Field(191)
    player_2: bool = Field(200)
    screen_offset_x: float = Field(290)
    screen_offset_y: float = Field(291)
    max_size: float = Field(512)
    animate: bool = Field(513)
    relative: bool = Field(514)
    disable_preview: bool = Field(531)


class SplitScreenShader(ShaderTrigger):
    duration: float = Field(10)
    easing: enums.Easing = Field(30)
    ease_rate: float = Field(85)
    target_x: float = Field(180)
    use_x: bool = Field(188)
    target_y: float = Field(189)
    use_y: bool = Field(190)
    disable_preview: bool = Field(531)


# BulgeShader
register_id(2916, BulgeShader)  # Bulge Shader Trigger

# ChromaticGlitchShader
register_id(2911, ChromaticGlitchShader)  # Chromatic Glitch Shader Trigger

# ChromaticShader
register_id(2910, ChromaticShader)  # Chromatic Aberration Shader Trigger

# EditColorShader
register_id(2923, EditColorShader)  # Edit Color Shader Trigger

# GlitchShader
register_id(2909, GlitchShader)  # Glitch Shader Trigger

# GrayScaleShader
register_id(2919, GrayScaleShader)  # Grayscale Shader Trigger

# HueShader
register_id(2922, HueShader)  # Hue Shader Trigger

# InvertColorShader
register_id(2921, InvertColorShader)  # Invert Color Trigger

# LensCircleShader
register_id(2913, LensCircleShader)  # Lens Circle Shader Trigger

# MotionBlurShader
register_id(2915, MotionBlurShader)  # Motion Blur Shader Trigger

# PinchShader
register_id(2917, PinchShader)  # Pinch Shader Trigger

# PixelateShader
register_id(2912, PixelateShader)  # Pixelate Shader Trigger

# RadialBlurShader
register_id(2914, RadialBlurShader)  # Radial Blur Shader Trigger

# SepiaShader
register_id(2920, SepiaShader)  # Sepia Shader Trigger

# ShaderOptions
register_id(2904, ShaderOptions)  # Shader Trigger

# ShockLineShader
register_id(2907, ShockLineShader)  # Shock Line Shader Trigger

# ShockwaveShader
register_id(2905, ShockwaveShader)  # Shock Wave Shader Trigger

# SplitScreenShader
register_id(2924, SplitScreenShader)  # Split Screen Shader Trigger
