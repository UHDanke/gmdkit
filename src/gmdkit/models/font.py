# Imports
import re
from dataclasses import dataclass, field
from typing import Any, Optional, Self

# Package Imports
from gmdkit.serialization.mixins import FilePathMixin


ATTRIBUTE_PATTERN = re.compile(r'(\w+)=("(?:.*?)"(?=\s|$)|\S*)')


def parse_attributes(line:str) -> dict[str, str]:
    return {k: v for k, v in ATTRIBUTE_PATTERN.findall(line)}


def decode_value(value:str, kind:type) -> Any:
    if kind is str:
        if len(value) >= 2 and value[0] == value[-1] == '"':
            return value[1:-1]
        return value
    if kind is bool:
        return value not in ("", "0")
    if kind is tuple:
        return tuple(int(x) for x in value.split(",")) if value else ()
    return kind(value)


def encode_value(value:Any, kind:type) -> str:
    if kind is str:
        return f'"{value}"'
    if kind is bool:
        return "1" if value else "0"
    if kind is tuple:
        return ",".join(str(x) for x in value)
    return str(value)


@dataclass(slots=True)
class FontRecord:
    KEYS = ()
    extra: dict[str, str] = field(default_factory=dict, kw_only=True)
    raw: dict[str, str] = field(default_factory=dict, kw_only=True, repr=False, compare=False)

    @classmethod
    def from_attributes(cls, attributes:dict[str, str]) -> Self:
        values = {}
        raw = {}
        extra = dict(attributes)
        for key, name, kind in cls.KEYS:
            if key in extra:
                text = extra.pop(key)
                values[name] = decode_value(text, kind)
                if encode_value(values[name], kind) != text:
                    raw[key] = text
        return cls(**values, extra=extra, raw=raw)

    def to_attributes(self) -> list[tuple[str, str]]:
        result = []
        for key, name, kind in self.KEYS:
            value = getattr(self, name)
            if value is None:
                continue
            text = self.raw.get(key)
            if text is None or decode_value(text, kind) != value:
                text = encode_value(value, kind)
            result.append((key, text))
        result.extend(self.extra.items())
        return result


@dataclass(slots=True)
class FontInfo(FontRecord):
    KEYS = (
        ("face", "face", str),
        ("size", "size", int),
        ("bold", "bold", bool),
        ("italic", "italic", bool),
        ("charset", "charset", str),
        ("unicode", "unicode", bool),
        ("stretchH", "stretch_h", int),
        ("smooth", "smooth", bool),
        ("aa", "aa", int),
        ("padding", "padding", tuple),
        ("spacing", "spacing", tuple),
        ("outline", "outline", int),
        )

    face: str = ""
    size: int = 0
    bold: bool = False
    italic: bool = False
    charset: str = ""
    unicode: bool = False
    stretch_h: int = 100
    smooth: bool = True
    aa: int = 1
    padding: tuple[int, int, int, int] = (0, 0, 0, 0)
    spacing: tuple[int, int] = (0, 0)
    outline: Optional[int] = None


@dataclass(slots=True)
class FontCommon(FontRecord):
    KEYS = (
        ("lineHeight", "line_height", int),
        ("base", "base", int),
        ("scaleW", "scale_w", int),
        ("scaleH", "scale_h", int),
        ("pages", "pages", int),
        ("packed", "packed", bool),
        ("alphaChnl", "alpha_channel", int),
        ("redChnl", "red_channel", int),
        ("greenChnl", "green_channel", int),
        ("blueChnl", "blue_channel", int),
        )

    line_height: int = 0
    base: int = 0
    scale_w: int = 0
    scale_h: int = 0
    pages: int = 1
    packed: bool = False
    alpha_channel: Optional[int] = None
    red_channel: Optional[int] = None
    green_channel: Optional[int] = None
    blue_channel: Optional[int] = None


@dataclass(slots=True)
class FontPage(FontRecord):
    KEYS = (
        ("id", "id", int),
        ("file", "file", str),
        )

    id: int = 0
    file: str = ""


@dataclass(slots=True)
class FontChar(FontRecord):
    KEYS = (
        ("id", "id", int),
        ("x", "x", int),
        ("y", "y", int),
        ("width", "width", int),
        ("height", "height", int),
        ("xoffset", "x_offset", int),
        ("yoffset", "y_offset", int),
        ("xadvance", "x_advance", int),
        ("page", "page", int),
        ("chnl", "channel", int),
        ("letter", "letter", str),
        )
    WIDTHS = {
        "id": 7, "x": 6, "y": 6, "width": 6, "height": 6,
        "xoffset": 6, "yoffset": 6, "xadvance": 6,
        }

    id: int = 0
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    x_offset: int = 0
    y_offset: int = 0
    x_advance: int = 0
    page: int = 0
    channel: int = 0
    letter: Optional[str] = None


@dataclass(slots=True)
class FontKerning(FontRecord):
    KEYS = (
        ("first", "first", int),
        ("second", "second", int),
        ("amount", "amount", int),
        )

    first: int = 0
    second: int = 0
    amount: int = 0


@dataclass
class BMFont(FilePathMixin):
    EXTENSION = "fnt"

    info: FontInfo = field(default_factory=FontInfo)
    common: FontCommon = field(default_factory=FontCommon)
    pages: dict[int, FontPage] = field(default_factory=dict)
    chars: dict[int, FontChar] = field(default_factory=dict)
    kernings: dict[tuple[int, int], FontKerning] = field(default_factory=dict)
    path: Optional[str] = field(default=None, repr=False, compare=False)

    def _name_fallback_(self):
        return self.info.face or None

    @classmethod
    def from_string(cls, string:str) -> Self:
        new = cls()

        for line in string.splitlines():
            tag, _, rest = line.strip().partition(" ")
            attributes = parse_attributes(rest)

            match tag:
                case "info":
                    new.info = FontInfo.from_attributes(attributes)
                case "common":
                    new.common = FontCommon.from_attributes(attributes)
                case "page":
                    page = FontPage.from_attributes(attributes)
                    new.pages[page.id] = page
                case "char":
                    char = FontChar.from_attributes(attributes)
                    new.chars[char.id] = char
                case "kerning":
                    kerning = FontKerning.from_attributes(attributes)
                    new.kernings[(kerning.first, kerning.second)] = kerning
                case "chars" | "kernings" | "":
                    continue
                case _:
                    raise ValueError(f"unknown font block '{tag}'")

        return new

    def to_string(self) -> str:
        lines = [
            format_line("info", self.info.to_attributes()),
            format_line("common", self.common.to_attributes()),
            ]
        lines.extend(format_line("page", p.to_attributes()) for p in self.pages.values())
        lines.append(f"chars count={len(self.chars)}")
        lines.extend(
            format_line("char", c.to_attributes(), widths=FontChar.WIDTHS)
            for c in self.chars.values()
            )
        if self.kernings:
            lines.append(f"kernings count={len(self.kernings)}")
            lines.extend(format_line("kerning", k.to_attributes()) for k in self.kernings.values())
        return "\n".join(lines) + "\n"

    def get_char(self, char_id:int) -> Optional[FontChar]:
        return self.chars.get(char_id)

    def get_kerning(self, first:int, second:int) -> int:
        kerning = self.kernings.get((first, second))
        return 0 if kerning is None else kerning.amount

    def set_kerning(self, first:int, second:int, amount:int):
        if amount:
            self.kernings[(first, second)] = FontKerning(first=first, second=second, amount=amount)
        else:
            self.kernings.pop((first, second), None)


def format_line(tag:str, attributes:list[tuple[str, str]], widths:Optional[dict[str, int]]=None) -> str:
    widths = widths or {}
    parts = []
    for key, value in attributes:
        width = widths.get(key)
        parts.append(f"{key}={value:<{width}}" if width else f"{key}={value} ")
    return (tag + " " + "".join(parts)).rstrip()