# Imports
import copy
import math
from array import array
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Self, Sequence

# Package Imports
from gmdkit.models.font import BMFont
from gmdkit.models.object import Object, ObjectList
from gmdkit.models import interfaces
from gmdkit.utils.enums import EnumClass
from gmdkit.utils.typing import PathString, ANY, NEWLINE


TEXT_OBJECT_ID = 914
MAX_TEXT_BYTES = 400
DEFAULT_TEXT = "A"
NO_PREVIOUS_GLYPH = 0xFFFF


class TextureQuality(EnumClass):
    LOW = 1
    MEDIUM = 2
    HIGH = 4


class TextAlign(EnumClass):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    JUSTIFY = 3


class VerticalAlign(EnumClass):
    TOP = 0
    CENTER = 1
    BOTTOM = 2


class TextCase(EnumClass):
    NONE = 0
    UPPER = 1
    LOWER = 2


FONT_SUFFIXES = {
    TextureQuality.LOW: "",
    TextureQuality.MEDIUM: "-hd",
    TextureQuality.HIGH: "-uhd",
    }


def font_file_name(font_id:int) -> str:
    if font_id <= 0:
        return "bigFont"
    return f"gjFont{min(font_id, 59):02d}"


@dataclass
class GameFont:
    fonts: dict[TextureQuality, BMFont] = field(default_factory=dict)

    @classmethod
    def from_directory(cls, path:PathString, name:str|int) -> Self:
        if isinstance(name, int):
            name = font_file_name(name)

        new = cls()
        for quality, suffix in FONT_SUFFIXES.items():
            file = Path(path) / f"{name}{suffix}.fnt"
            if file.is_file():
                new.fonts[quality] = BMFont.from_file(file)

        if not new.fonts:
            raise FileNotFoundError(f"no font files named '{name}' found in '{path}'")

        return new

    @classmethod
    def from_files(
            cls,
            low:Optional[PathString]=None,
            medium:Optional[PathString]=None,
            high:Optional[PathString]=None
            ) -> Self:
        new = cls()
        for quality, path in zip(TextureQuality, (low, medium, high)):
            if path is not None:
                new.fonts[quality] = BMFont.from_file(path)
        return new

    def get(self, quality:TextureQuality=TextureQuality.HIGH) -> BMFont:
        font = self.fonts.get(TextureQuality(quality))
        if font is None:
            raise KeyError(f"font is missing the {TextureQuality(quality).name} quality file")
        return font


def render_text(text:str) -> str:
    if "\0" in text:
        return ""

    try:
        data = text.encode("utf-8")
    except UnicodeEncodeError:
        return ""

    if len(data) > MAX_TEXT_BYTES:
        end = MAX_TEXT_BYTES
        while end > 0 and data[end] & 0xC0 == 0x80:
            end -= 1
        data = data[:end]

    text = data.decode("utf-8")

    if text in ("", " "):
        return DEFAULT_TEXT

    return text


def utf16_units(text:str) -> array:
    return array("H", text.encode("utf-16-le"))


@dataclass(slots=True)
class LabelGlyph:
    index: int
    char: int
    glyph: int
    line: int
    x: float
    y: float
    width: float
    height: float


@dataclass(slots=True)
class LabelLayout:
    text: str
    glyphs: list[LabelGlyph]
    width: float
    height: float
    lines: int

    @property
    def anchor(self) -> tuple[float, float]:
        return self.width / 2, self.height / 2

    def glyph_at(self, index:int) -> Optional[LabelGlyph]:
        for glyph in self.glyphs:
            if glyph.index == index:
                return glyph
        return None


def layout_label(
        text:str,
        font:BMFont,
        kerning:int=0,
        scale_factor:int=TextureQuality.HIGH
        ) -> LabelLayout:

    units = utf16_units(text)
    count = len(units)
    line_height = font.common.line_height
    lines = 1 + sum(1 for u in units[:count - 1] if u == 10) if count else 1

    glyphs = []
    line = 0
    line_x = 0
    line_y = (lines - 1) * line_height
    longest = 0
    previous = NO_PREVIOUS_GLYPH
    last = None

    for index, unit in enumerate(units):

        if unit == 10:
            line_x = 0
            line_y -= line_height
            line += 1
            continue

        glyph = unit
        char = font.get_char(glyph)

        if char is None:
            if 0x61 <= unit <= 0x7A and font.get_char(unit - 0x20) is not None:
                glyph = unit - 0x20
                char = font.get_char(glyph)
            else:
                continue

        amount = font.get_kerning(previous, glyph) + kerning

        x = line_x + char.x_offset + char.width * 0.5 + amount
        y = line_y + line_height - char.y_offset - char.height * 0.5

        glyphs.append(LabelGlyph(
            index=index,
            char=unit,
            glyph=glyph,
            line=line,
            x=x / scale_factor,
            y=y / scale_factor,
            width=char.width / scale_factor,
            height=char.height / scale_factor,
            ))

        line_x += char.x_advance + amount
        longest = max(longest, line_x)
        previous = glyph
        last = char

    width = longest
    if last is not None and last.x_advance < last.width:
        width = last.width + longest - last.x_advance

    if not count:
        width = 0
        lines = 0

    return LabelLayout(
        text=text,
        glyphs=glyphs,
        width=width / scale_factor,
        height=lines * line_height / scale_factor,
        lines=lines,
        )


Matrix = tuple[float, float, float, float]


def multiply_matrix(first:Matrix, second:Matrix) -> Matrix:
    a1, b1, c1, d1 = first
    a2, b2, c2, d2 = second
    return (
        a1 * a2 + c1 * b2,
        b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2,
        b1 * c2 + d1 * d2,
        )


def apply_matrix(matrix:Matrix, x:float, y:float) -> tuple[float, float]:
    a, b, c, d = matrix
    return a * x + c * y, b * x + d * y


def same_matrix(first:Matrix, second:Matrix, tolerance:float=1e-9) -> bool:
    return all(abs(p - q) <= tolerance for p, q in zip(first, second))


@dataclass(slots=True, frozen=True)
class ObjectTransform:
    scale_x: float = 1.0
    scale_y: float = 1.0
    skew_x: float = 0.0
    skew_y: float = 0.0
    flip_x: bool = False
    flip_y: bool = False

    @classmethod
    def rotated(cls, angle:float, scale_x:float=1.0, scale_y:float=1.0, flip_x:bool=False, flip_y:bool=False) -> Self:
        return cls(scale_x=scale_x, scale_y=scale_y, skew_x=angle, skew_y=angle, flip_x=flip_x, flip_y=flip_y)

    @classmethod
    def from_matrix(cls, matrix:Matrix) -> Self:
        a, b, c, d = matrix
        return cls(
            scale_x=math.hypot(a, b),
            scale_y=math.hypot(c, d),
            skew_x=math.degrees(math.atan2(c, d)),
            skew_y=math.degrees(math.atan2(-b, a)),
            )

    @classmethod
    def from_object(cls, obj:Object) -> Self:
        custom_x = obj.get(128) or 0
        custom_y = obj.get(129) or 0

        if custom_x or custom_y:
            scale_x = custom_x or 1.0
            scale_y = custom_y or 1.0
        else:
            scale_x = scale_y = obj.get(32) or 1.0

        rotation = obj.get(6) or 0.0
        skew_x = obj.get(131) or 0.0
        skew_y = obj.get(132) or 0.0

        if skew_x == skew_y:
            skew_x = skew_y = rotation

        return cls(
            scale_x=float(scale_x),
            scale_y=float(scale_y),
            skew_x=float(skew_x),
            skew_y=float(skew_y),
            flip_x=bool(obj.get(4)),
            flip_y=bool(obj.get(5)),
            )

    def to_object(self, obj:Object):
        obj.pop(32, None)

        for key, value in ((128, self.scale_x), (129, self.scale_y)):
            if value != 1:
                obj[key] = value
            else:
                obj.pop(key, None)

        for key, value in ((4, self.flip_x), (5, self.flip_y)):
            if value:
                obj[key] = True
            else:
                obj.pop(key, None)

        if self.skew_x == self.skew_y:
            obj.pop(131, None)
            obj.pop(132, None)
            if self.skew_x:
                obj[6] = self.skew_x
            else:
                obj.pop(6, None)
        else:
            obj.pop(6, None)
            obj[131] = self.skew_x
            obj[132] = self.skew_y

    @property
    def matrix(self) -> Matrix:
        sx = -self.scale_x if self.flip_x else self.scale_x
        sy = -self.scale_y if self.flip_y else self.scale_y
        rx = math.radians(self.skew_x)
        ry = math.radians(self.skew_y)
        return (
            math.cos(ry) * sx,
            -math.sin(ry) * sx,
            math.sin(rx) * sy,
            math.cos(rx) * sy,
            )

    def apply(self, x:float, y:float) -> tuple[float, float]:
        return apply_matrix(self.matrix, x, y)


@dataclass(slots=True)
class PlacedGlyph:
    index: int
    char: str
    x: float
    y: float
    width: float
    height: float
    matrix: Matrix
    page: int
    texture: tuple[int, int, int, int]


def text_object_glyphs(
        obj:Object,
        font:GameFont,
        quality:TextureQuality=TextureQuality.HIGH
        ) -> list[PlacedGlyph]:

    view = obj.require_interface(interfaces.Text)
    bm_font = font.get(quality)
    layout = layout_label(render_text(view.data), bm_font, view.kerning, int(quality))
    matrix = ObjectTransform.from_object(obj).matrix
    ax, ay = layout.anchor

    result = []
    for glyph in layout.glyphs:
        dx, dy = apply_matrix(matrix, glyph.x - ax, glyph.y - ay)
        char = bm_font.get_char(glyph.glyph)
        result.append(PlacedGlyph(
            index=glyph.index,
            char=chr(glyph.glyph),
            x=view.x + dx,
            y=view.y + dy,
            width=glyph.width,
            height=glyph.height,
            matrix=matrix,
            page=char.page,
            texture=(char.x, char.y, char.width, char.height),
            ))
    return result


@dataclass(slots=True)
class TextCell:
    text: str
    x: Optional[float] = None
    y: Optional[float] = None
    transform: Optional[ObjectTransform] = None

    @property
    def visible(self) -> bool:
        return self.x is not None

    @property
    def units(self) -> int:
        return len(self.text.encode("utf-16-le")) // 2


@dataclass(slots=True)
class TextPlacement:
    text: str
    kerning: int
    x: float
    y: float
    transform: ObjectTransform


def label_cells(layout:LabelLayout, transform:ObjectTransform) -> list[list[TextCell]]:
    glyphs = {glyph.index: glyph for glyph in layout.glyphs}
    ax, ay = layout.anchor
    lines = [[]]
    index = 0

    for char in layout.text:
        if char == "\n":
            lines.append([])
            index += 1
            continue

        cell = TextCell(char)
        glyph = glyphs.get(index)

        if glyph is not None and not char.isspace():
            cell.x, cell.y = transform.apply(glyph.x - ax, glyph.y - ay)
            cell.transform = transform

        lines[-1].append(cell)
        index += cell.units

    return lines


def place_text(
        lines:Sequence[Sequence[TextCell]],
        font:BMFont,
        kerning:int=0,
        scale_factor:int=TextureQuality.HIGH,
        tolerance:float=1e-4
        ) -> Optional[TextPlacement]:

    text = "\n".join("".join(cell.text for cell in line) for line in lines)

    if render_text(text) != text:
        return None

    layout = layout_label(text, font, kerning, scale_factor)
    glyphs = {glyph.index: glyph for glyph in layout.glyphs}
    ax, ay = layout.anchor
    transform = None
    matrix = None
    offset = None
    index = 0

    for line in lines:
        for cell in line:
            if cell.visible:
                glyph = glyphs.get(index)
                if glyph is None:
                    return None

                if transform is None:
                    transform = cell.transform
                    matrix = transform.matrix
                elif cell.transform is not transform and not same_matrix(matrix, cell.transform.matrix):
                    return None

                dx, dy = apply_matrix(matrix, glyph.x - ax, glyph.y - ay)
                ox = cell.x - dx
                oy = cell.y - dy

                if offset is None:
                    offset = (ox, oy)
                elif abs(ox - offset[0]) > tolerance or abs(oy - offset[1]) > tolerance:
                    return None

            index += cell.units
        index += 1

    if offset is None:
        return None

    return TextPlacement(text, kerning, offset[0], offset[1], transform)


def strip_cells(cells:Sequence[TextCell], leading:bool=True) -> list[TextCell]:
    visible = [i for i, cell in enumerate(cells) if cell.visible]
    if not visible:
        return []
    start = visible[0] if leading else 0
    return list(cells[start:visible[-1] + 1])


def split_separators(split:str|object|None) -> Optional[set[str]]:
    if split is None:
        return set()
    if split is NEWLINE:
        return {"\n"}
    if split is ANY:
        return None
    if isinstance(split, str):
        return set(split)
    raise TypeError(f"split must be a string, NEWLINE, ANY or None, got {split!r}")


def has_separator(lines:Sequence[Sequence[TextCell]], separators:set[str]) -> bool:
    if "\n" in separators and len(lines) > 1:
        return True
    return any(cell.text in separators for line in lines for cell in line)


def split_cells(cells:Sequence[TextCell], separators:Optional[set[str]]) -> list[list[TextCell]]:
    if separators is None:
        return [[cell] for cell in cells if cell.visible]

    parts = [[]]
    for cell in cells:
        if cell.text in separators:
            parts.append([cell])
            parts.append([])
        else:
            parts[-1].append(cell)

    return [strip_cells(part) for part in parts if any(cell.visible for cell in part)]


def fit_cells(
        cells:Sequence[TextCell],
        font:BMFont,
        kerning:int,
        scale_factor:int,
        tolerance:float
        ) -> list[TextPlacement]:

    visible = [i for i, cell in enumerate(cells) if cell.visible]
    result = []
    start = 0

    while start < len(visible):
        first = visible[start]
        best = place_text([cells[first:first + 1]], font, kerning, scale_factor, tolerance)
        end = start

        while best is not None and end + 1 < len(visible):
            candidate = place_text([cells[first:visible[end + 1] + 1]], font, kerning, scale_factor, tolerance)
            if candidate is None:
                break
            best = candidate
            end += 1

        if best is not None:
            result.append(best)
        start = end + 1

    return result


def fit_text(
        lines:Sequence[Sequence[TextCell]],
        font:BMFont,
        kerning:int=0,
        scale_factor:int=TextureQuality.HIGH,
        split:str|object|None=None,
        tolerance:float=1e-4
        ) -> list[TextPlacement]:

    separators = split_separators(split)
    result = []
    count = len(lines)
    i = 0

    while i < count:
        line = strip_cells(lines[i])

        if not line:
            i += 1
            continue

        best = None
        if separators is not None and not has_separator([line], separators):
            best = place_text([line], font, kerning, scale_factor, tolerance)

        if best is None:
            for part in split_cells(line, separators):
                result.extend(fit_cells(part, font, kerning, scale_factor, tolerance))
            i += 1
            continue

        end = i + 1
        j = i + 1
        while j < count:
            block = [strip_cells(lines[k], leading=False) for k in range(i, j + 1)]
            if has_separator(block, separators):
                break
            if not block[-1]:
                j += 1
                continue
            candidate = place_text(block, font, kerning, scale_factor, tolerance)
            if candidate is None:
                break
            best = candidate
            j += 1
            end = j

        result.append(best)
        i = end

    return result


def placement_objects(
        placements:Sequence[TextPlacement],
        template:Object,
        origin_x:float,
        origin_y:float
        ) -> ObjectList:

    result = ObjectList()

    for placement in placements:
        obj = copy.deepcopy(template)
        placement.transform.to_object(obj)
        view = obj.require_interface(interfaces.Text)
        view.data = placement.text

        if placement.kerning:
            view.kerning = placement.kerning
        else:
            obj.pop(488, None)

        view.x = origin_x + placement.x
        view.y = origin_y + placement.y
        result.append(obj)

    return result


def split_text_object(
        obj:Object,
        font:GameFont,
        quality:TextureQuality=TextureQuality.HIGH,
        split:str|object|None=ANY,
        portable:bool=True,
        tolerance:float=1e-4
        ) -> ObjectList:

    view = obj.require_interface(interfaces.Text)
    scale_factor = int(quality)
    bm_font = font.get(quality)
    layout = layout_label(render_text(view.data), bm_font, view.kerning, scale_factor)
    lines = label_cells(layout, ObjectTransform.from_object(obj))
    kerning = 0 if portable else view.kerning
    placements = fit_text(lines, bm_font, kerning, scale_factor, split, tolerance)

    return placement_objects(placements, obj, view.x, view.y)


@dataclass(slots=True, frozen=True)
class Padding:
    left: float = 0.0
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0

    @classmethod
    def all(cls, value:float) -> Self:
        return cls(value, value, value, value)

    @classmethod
    def symmetric(cls, horizontal:float=0.0, vertical:float=0.0) -> Self:
        return cls(horizontal, vertical, horizontal, vertical)


def rotation_matrix(angle:float) -> Matrix:
    radians = math.radians(angle)
    return (math.cos(radians), -math.sin(radians), math.sin(radians), math.cos(radians))


IDENTITY_MATRIX = (1.0, 0.0, 0.0, 1.0)


@dataclass(slots=True, frozen=True)
class EllipsePath:
    radius_x: float
    radius_y: float
    angle: float = 90.0
    clockwise: bool = True
    samples: int = 4096
    table: tuple = field(default=(), init=False, repr=False, compare=False)

    def __post_init__(self):
        step = 2 * math.pi / self.samples
        lengths = [0.0]
        for i in range(self.samples):
            t = i * step
            lengths.append(lengths[-1] + step / 6 * (
                self.speed(t) + 4 * self.speed(t + step / 2) + self.speed(t + step)))
        object.__setattr__(self, "table", tuple(lengths))

    def speed(self, t:float) -> float:
        return math.hypot(self.radius_x * math.sin(t), self.radius_y * math.cos(t))

    @classmethod
    def circle(cls, radius:float, angle:float=90.0, clockwise:bool=True) -> Self:
        return cls(radius, radius, angle, clockwise)

    @property
    def circumference(self) -> float:
        return self.table[-1]

    def length_at(self, t:float) -> float:
        turns, rest = divmod(t, 2 * math.pi)
        position = rest / (2 * math.pi) * self.samples
        i = min(int(position), self.samples - 1)
        fraction = position - i
        return turns * self.circumference + self.table[i] + (self.table[i + 1] - self.table[i]) * fraction

    def angle_at(self, length:float) -> float:
        turns, rest = divmod(length, self.circumference)
        low, high = 0, self.samples
        while high - low > 1:
            middle = (low + high) // 2
            if self.table[middle] <= rest:
                low = middle
            else:
                high = middle
        span = self.table[low + 1] - self.table[low]
        fraction = (rest - self.table[low]) / span if span else 0.0
        return 2 * math.pi * (turns + (low + fraction) / self.samples)

    def point(self, t:float) -> tuple[float, float]:
        return self.radius_x * math.cos(t), self.radius_y * math.sin(t)

    def place(self, x:float, y:float) -> tuple[float, float, Matrix]:
        direction = -1.0 if self.clockwise else 1.0
        start = self.length_at(math.radians(self.angle))
        t = self.angle_at(start + direction * x)
        px, py = self.point(t)
        tx, ty = -self.radius_x * math.sin(t) * direction, self.radius_y * math.cos(t) * direction
        size = math.hypot(tx, ty) or 1.0
        tx, ty = tx / size, ty / size
        nx, ny = -ty, tx
        return px + nx * y, py + ny * y, (tx, ty, nx, ny)

    def outline(self, samples:int=128) -> list[tuple[float, float]]:
        return [self.point(2 * math.pi * i / samples) for i in range(samples)]


@dataclass(slots=True)
class TextLine:
    text: str
    first: bool
    last: bool


@dataclass(slots=True)
class LineLayout:
    cells: list[TextCell]
    width: float


@dataclass
class TextBlock:
    text: str
    font: GameFont
    x: float = 0.0
    y: float = 0.0
    anchor: tuple[float, float] = (0.5, 0.5)
    world_anchor: Optional[tuple[float, float]] = None
    align: TextAlign = TextAlign.LEFT
    vertical_align: VerticalAlign = VerticalAlign.TOP
    width: Optional[float] = None
    height: Optional[float] = None
    padding: Padding = field(default_factory=Padding)
    line_height: Optional[float] = None
    line_spacing: float = 0.0
    paragraph_spacing: float = 0.0
    line_offset: tuple[float, float] = (0.0, 0.0)
    indent: float = 0.0
    letter_spacing: float = 0.0
    word_spacing: float = 0.0
    tab_size: int = 4
    case: TextCase = TextCase.NONE
    break_words: bool = False
    transform: ObjectTransform = field(default_factory=ObjectTransform)
    glyph_rotation: float = 0.0
    path: Optional[EllipsePath] = None
    quality: TextureQuality = TextureQuality.HIGH
    portable: bool = True
    split: str|object|None = None
    template: Optional[Object] = None
    tolerance: float = 1e-4

    @property
    def bm_font(self) -> BMFont:
        return self.font.get(self.quality)

    @property
    def font_line_height(self) -> float:
        return self.bm_font.common.line_height / int(self.quality)

    @property
    def row_height(self) -> float:
        return self.font_line_height if self.line_height is None else self.line_height

    @property
    def kerning(self) -> int:
        amount = self.letter_spacing * int(self.quality)
        kerning = round(amount)
        if abs(amount - kerning) > 1e-6 or (self.portable and kerning):
            return 0
        return kerning

    @property
    def source_text(self) -> str:
        text = self.text.replace("\r\n", "\n").replace("\t", " " * self.tab_size)
        match self.case:
            case TextCase.UPPER:
                return text.upper()
            case TextCase.LOWER:
                return text.lower()
        return text

    def layout_line(self, text:str, extra_space:float=0.0) -> LineLayout:
        layout = layout_label(text, self.bm_font, 0, int(self.quality))
        glyphs = {glyph.index: glyph for glyph in layout.glyphs}
        space = self.word_spacing + extra_space
        cells = []
        index = 0
        order = 0
        spaces = 0

        for char in text:
            cell = TextCell(char)
            glyph = glyphs.get(index)

            if glyph is not None:
                if not char.isspace():
                    cell.x = glyph.x + self.letter_spacing * order + space * spaces
                    cell.y = glyph.y
                order += 1

            if char == " ":
                spaces += 1

            cells.append(cell)
            index += cell.units

        width = layout.width + self.letter_spacing * max(order - 1, 0) + space * spaces
        return LineLayout(cells, width)

    def line_width(self, text:str) -> float:
        return self.layout_line(text).width

    def split_word(self, word:str, width:float) -> list[str]:
        parts = []
        current = ""
        for char in word:
            if current and self.line_width(current + char) > width:
                parts.append(current)
                current = char
            else:
                current += char
        parts.append(current)
        return parts

    def wrap(self) -> list[TextLine]:
        result = []

        for paragraph in self.source_text.split("\n"):
            if self.width is None:
                result.append(TextLine(paragraph.rstrip(), True, True))
                continue

            lines = []
            current = None
            for word in paragraph.split(" "):
                available = self.width - (self.indent if not lines else 0.0)
                candidate = word if current is None else f"{current} {word}"

                if current is not None and self.line_width(candidate.rstrip()) > available:
                    lines.append(current.rstrip())
                    current = word
                else:
                    current = candidate

                available = self.width - (self.indent if not lines else 0.0)
                if self.break_words and current and self.line_width(current) > available:
                    parts = self.split_word(current, available)
                    lines.extend(parts[:-1])
                    current = parts[-1]

            lines.append((current or "").rstrip())
            for i, text in enumerate(lines):
                result.append(TextLine(text, i == 0, i == len(lines) - 1))

        return result

    def content_height(self, lines:Sequence[TextLine]) -> float:
        if not lines:
            return 0.0
        height = len(lines) * self.row_height + (len(lines) - 1) * self.line_spacing
        height += self.paragraph_spacing * sum(1 for line in lines[:-1] if line.last)
        return height

    def content_size(self) -> tuple[float, float]:
        lines = self.wrap()
        width = self.width
        if width is None:
            width = max(
                (self.line_width(line.text) + (self.indent if line.first else 0.0) for line in lines),
                default=0.0,
                )
        height = self.height
        if height is None:
            height = self.content_height(lines)
        return width, height

    @property
    def origin(self) -> tuple[float, float]:
        if self.world_anchor is None:
            return self.x, self.y
        return self.world_anchor

    def box(self) -> tuple[float, float, float, float]:
        width, height = self.content_size()
        padding = self.padding
        box_width = width + padding.left + padding.right
        box_height = height + padding.top + padding.bottom
        return (
            -self.anchor[0] * box_width,
            -self.anchor[1] * box_height,
            box_width,
            box_height,
            )

    def layout(self) -> list[list[TextCell]]:
        lines = self.wrap()
        width, height = self.content_size()
        left, bottom, box_width, box_height = self.box()
        padding = self.padding
        content_left = left + padding.left
        content_top = bottom + box_height - padding.top
        row_height = self.row_height
        natural = self.content_height(lines)

        match self.vertical_align:
            case VerticalAlign.CENTER:
                content_top -= (height - natural) / 2
            case VerticalAlign.BOTTOM:
                content_top -= height - natural

        result = []
        top = content_top

        for i, line in enumerate(lines):
            indent = self.indent if line.first else 0.0
            layout = self.layout_line(line.text)
            available = width - indent
            offset = indent

            match self.align:
                case TextAlign.CENTER:
                    offset += (available - layout.width) / 2
                case TextAlign.RIGHT:
                    offset += available - layout.width
                case TextAlign.JUSTIFY:
                    spaces = line.text.count(" ")
                    if not line.last and spaces:
                        layout = self.layout_line(line.text, (available - layout.width) / spaces)

            line_x = content_left + offset + self.line_offset[0] * i
            line_y = top - row_height + (row_height - self.font_line_height) / 2 + self.line_offset[1] * i

            for cell in layout.cells:
                if cell.visible:
                    cell.x += line_x
                    cell.y += line_y

            result.append(layout.cells)
            top -= row_height + self.line_spacing + (self.paragraph_spacing if line.last else 0.0)

        return result

    def place(self, x:float, y:float) -> tuple[float, float, Matrix]:
        if self.path is None:
            matrix = IDENTITY_MATRIX
        else:
            x, y, matrix = self.path.place(x, y)
        origin_x, origin_y = self.origin
        return self.x - origin_x + x, self.y - origin_y + y, matrix

    def map_point(self, x:float, y:float) -> tuple[float, float]:
        px, py, _ = self.place(x, y)
        return self.transform.apply(px, py)

    def cells(self) -> list[list[TextCell]]:
        result = []
        transform = self.transform
        base = transform.matrix

        for line in self.layout():
            for cell in line:
                if not cell.visible:
                    continue

                px, py, matrix = self.place(cell.x, cell.y)
                if self.glyph_rotation:
                    matrix = multiply_matrix(matrix, rotation_matrix(self.glyph_rotation))

                cell.x, cell.y = transform.apply(px, py)

                if matrix is IDENTITY_MATRIX:
                    cell.transform = transform
                else:
                    cell.transform = ObjectTransform.from_matrix(multiply_matrix(base, matrix))

            result.append(line)

        return result

    def path_outline(self, samples:int=128) -> list[tuple[float, float]]:
        if self.path is None:
            return []
        origin_x, origin_y = self.origin
        offset_x, offset_y = self.x - origin_x, self.y - origin_y
        points = []
        for x, y in self.path.outline(samples):
            px, py = self.transform.apply(offset_x + x, offset_y + y)
            points.append((origin_x + px, origin_y + py))
        return points

    def outline(self, samples:int=16) -> list[tuple[float, float]]:
        left, bottom, width, height = self.box()
        origin_x, origin_y = self.origin
        corners = ((left, bottom), (left + width, bottom), (left + width, bottom + height), (left, bottom + height))
        points = []
        for (x0, y0), (x1, y1) in zip(corners, corners[1:] + corners[:1]):
            for step in range(samples):
                t = step / samples
                px, py = self.map_point(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
                points.append((origin_x + px, origin_y + py))
        return points

    def placements(self) -> list[TextPlacement]:
        return fit_text(
            self.cells(),
            self.bm_font,
            self.kerning,
            int(self.quality),
            self.split,
            self.tolerance,
            )

    def to_objects(self) -> ObjectList:
        template = self.template
        if template is None:
            template = Object.from_editor(TEXT_OBJECT_ID)
        return placement_objects(self.placements(), template, *self.origin)