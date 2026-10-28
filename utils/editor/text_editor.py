# Imports
import argparse
import importlib.util
import json
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse


REQUIRED_LIBRARIES = {
    "numpy": "pip install numpy",
    "zstandard": "pip install zstandard",
    "websocket": "pip install websocket-client",
    "gmdkit": "pip install -e <path to the gmdkit repository>",
    }

REQUIRED_MODULES = {
    "gmdkit.models.font": "font.py",
    "gmdkit.extensions.text": "text.py",
    "gmdkit.extensions.live_editor": "live_editor.py",
    }


def check_libraries() -> list[str]:
    problems = []

    for name, install in REQUIRED_LIBRARIES.items():
        if importlib.util.find_spec(name) is None:
            problems.append(f"missing library '{name}', install it with: {install}")

    if problems:
        return problems

    for name, file in REQUIRED_MODULES.items():
        try:
            found = importlib.util.find_spec(name) is not None
        except ImportError as error:
            problems.append(f"could not import '{name}': {error}")
            continue
        if not found:
            problems.append(f"gmdkit is missing '{name}' ({file}), update gmdkit")

    return problems


PROBLEMS = check_libraries()

if PROBLEMS:
    print("text editor cannot start:")
    for problem in PROBLEMS:
        print(f"  - {problem}")
    if __name__ == "__main__":
        sys.exit(1)
    raise ImportError("; ".join(PROBLEMS))


# Package Imports
from gmdkit.models import interfaces
from gmdkit.models.object import ObjectList
from gmdkit.extensions import live_editor
from gmdkit.extensions.text import (
    ANY, NEWLINE, EllipsePath, GameFont, ObjectTransform, Padding,
    TextAlign, TextBlock, TextCase, TextureQuality, VerticalAlign,
    font_file_name, text_object_glyphs,
    )


FONT_PATTERN = re.compile(r"^(bigFont|gjFont(\d{2}))(-hd|-uhd)?\.fnt$")
CONFIG_PATH = Path.home() / ".gmdkit" / "text_editor.json"
RESOURCE_CANDIDATES = (
    r"C:\Program Files (x86)\Steam\steamapps\common\Geometry Dash\Resources",
    r"C:\Program Files\Steam\steamapps\common\Geometry Dash\Resources",
    "~/Library/Application Support/Steam/steamapps/common/Geometry Dash/Geometry Dash.app/Contents/Resources",
    "~/.steam/steam/steamapps/common/Geometry Dash/Resources",
    "~/.local/share/Steam/steamapps/common/Geometry Dash/Resources",
    )


class FontLibrary:

    def __init__(self, path:str|Path):
        self.path = Path(path).expanduser()
        self.fonts: dict[int, GameFont] = {}

        if not self.path.is_dir():
            raise FileNotFoundError(f"folder not found: {self.path}")
        if not self.available():
            raise FileNotFoundError(f"no font files (bigFont / gjFontXX .fnt) found in {self.path}")

    def available(self) -> list[int]:
        ids = set()
        for file in self.path.glob("*.fnt"):
            match = FONT_PATTERN.match(file.name)
            if match:
                ids.add(int(match.group(2)) if match.group(2) else 0)
        return sorted(ids)

    def get(self, font_id:int) -> GameFont:
        font = self.fonts.get(font_id)
        if font is None:
            font = self.fonts[font_id] = GameFont.from_directory(self.path, font_file_name(font_id))
        return font

    def page_path(self, font_id:int, quality:int, page:int) -> Optional[Path]:
        bm_font = self.get(font_id).get(quality)
        info = bm_font.pages.get(page)
        if info is None:
            return None
        path = self.path / info.file
        return path if path.is_file() else None


class EditorConfig:

    def __init__(self, path:Path=CONFIG_PATH):
        self.path = path
        self.resources = ""
        self.live_url = live_editor.WEBSOCKET_URL
        self.library: Optional[FontLibrary] = None
        self.error = ""

    def load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}

        self.live_url = data.get("live_url") or live_editor.WEBSOCKET_URL
        resources = data.get("resources") or ""

        if not resources:
            for candidate in RESOURCE_CANDIDATES:
                if Path(candidate).expanduser().is_dir():
                    resources = candidate
                    break

        self.set_resources(resources)

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps({"resources": self.resources, "live_url": self.live_url}, indent=2),
                encoding="utf-8",
                )
        except OSError as error:
            self.error = f"could not save settings: {error}"

    def set_resources(self, resources:str):
        self.resources = resources.strip().strip('"')
        self.library = None
        self.error = ""

        if not self.resources:
            self.error = "set the game's Resources folder"
            return

        try:
            self.library = FontLibrary(self.resources)
        except FileNotFoundError as error:
            self.error = str(error)

    def to_dict(self) -> dict[str, Any]:
        return {
            "resources": self.resources,
            "live_url": self.live_url,
            "fonts": self.library.available() if self.library else [],
            "error": self.error,
            "config_file": str(self.path),
            }

    def require_library(self) -> FontLibrary:
        if self.library is None:
            raise ValueError(self.error or "set the game's Resources folder")
        return self.library


def number(settings:dict, key:str, default:float=0.0) -> float:
    value = settings.get(key, default)
    if value in (None, ""):
        return default
    return float(value)


def optional_number(settings:dict, key:str) -> Optional[float]:
    value = settings.get(key)
    if value in (None, ""):
        return None
    return float(value)


def split_from_settings(settings:dict) -> str|object|None:
    match settings.get("split", "none"):
        case "any":
            return ANY
        case "newline":
            return NEWLINE
        case "chars":
            return settings.get("split_chars") or None
    return None


def path_from_settings(settings:dict) -> Optional[EllipsePath]:
    match settings.get("path", "none"):
        case "circle":
            radius = number(settings, "path_radius_x", 300)
            if not radius:
                return None
            return EllipsePath.circle(radius, number(settings, "path_angle", 90), not settings.get("path_reverse"))
        case "ellipse":
            radius_x = number(settings, "path_radius_x", 300)
            radius_y = number(settings, "path_radius_y", 200)
            if not radius_x or not radius_y:
                return None
            return EllipsePath(radius_x, radius_y, number(settings, "path_angle", 90), not settings.get("path_reverse"))
    return None


def block_from_settings(settings:dict, library:FontLibrary) -> TextBlock:
    rotation = number(settings, "rotation")
    return TextBlock(
        text=settings.get("text", ""),
        font=library.get(int(settings.get("font", 1))),
        x=number(settings, "x"),
        y=number(settings, "y"),
        anchor=(number(settings, "anchor_x", 0.5), number(settings, "anchor_y", 0.5)),
        world_anchor=(
            (number(settings, "world_anchor_x"), number(settings, "world_anchor_y"))
            if settings.get("world_anchor") else None
            ),
        align=TextAlign[settings.get("align", "LEFT")],
        vertical_align=VerticalAlign[settings.get("vertical_align", "TOP")],
        width=optional_number(settings, "width"),
        height=optional_number(settings, "height"),
        padding=Padding(
            number(settings, "padding_left"),
            number(settings, "padding_top"),
            number(settings, "padding_right"),
            number(settings, "padding_bottom"),
            ),
        line_height=optional_number(settings, "line_height"),
        line_spacing=number(settings, "line_spacing"),
        paragraph_spacing=number(settings, "paragraph_spacing"),
        line_offset=(number(settings, "line_offset_x"), number(settings, "line_offset_y")),
        indent=number(settings, "indent"),
        letter_spacing=number(settings, "letter_spacing"),
        word_spacing=number(settings, "word_spacing"),
        tab_size=int(number(settings, "tab_size", 4)),
        case=TextCase[settings.get("case", "NONE")],
        break_words=bool(settings.get("break_words")),
        transform=ObjectTransform(
            scale_x=number(settings, "scale_x", 1.0),
            scale_y=number(settings, "scale_y", 1.0),
            skew_x=rotation + number(settings, "skew_x"),
            skew_y=rotation + number(settings, "skew_y"),
            flip_x=bool(settings.get("flip_x")),
            flip_y=bool(settings.get("flip_y")),
            ),
        glyph_rotation=number(settings, "glyph_rotation"),
        path=path_from_settings(settings),
        quality=TextureQuality(int(settings.get("quality", 4))),
        portable=bool(settings.get("portable", True)),
        split=split_from_settings(settings),
        )


def build_objects(settings:dict, library:FontLibrary) -> tuple[TextBlock, ObjectList]:
    block = block_from_settings(settings, library)
    objects = block.to_objects()
    group = int(number(settings, "group"))
    if group:
        for obj in objects:
            obj.require_interface(interfaces.BaseObject).groups.append(group)
    return block, objects


def preview(settings:dict, library:FontLibrary) -> dict[str, Any]:
    block, objects = build_objects(settings, library)
    quality = block.quality
    bm_font = block.bm_font
    font_id = int(settings.get("font", 1))

    glyphs = []
    texts = []
    for obj in objects:
        texts.append(obj.require_interface(interfaces.Text).data)
        for glyph in text_object_glyphs(obj, block.font, quality):
            if glyph.char.isspace():
                continue
            glyphs.append({
                "char": glyph.char,
                "x": glyph.x,
                "y": glyph.y,
                "width": glyph.width,
                "height": glyph.height,
                "matrix": glyph.matrix,
                "page": glyph.page,
                "texture": glyph.texture,
                })

    origin_x, origin_y = block.origin
    anchor_x, anchor_y = block.map_point(0.0, 0.0)

    return {
        "glyphs": glyphs,
        "outline": block.outline(),
        "path": block.path_outline(),
        "anchor": [origin_x + anchor_x, origin_y + anchor_y],
        "origin": [origin_x, origin_y],
        "objects": len(objects),
        "texts": texts,
        "bytes": max((len(t.encode("utf-8")) for t in texts), default=0),
        "page_size": [bm_font.common.scale_w, bm_font.common.scale_h],
        "page_url": f"/page?font={font_id}&quality={int(quality)}&page=",
        "kerning": block.kerning,
        }


def send(settings:dict, library:FontLibrary, url:str) -> dict[str, Any]:
    _, objects = build_objects(settings, library)
    group = int(number(settings, "group"))
    if not group:
        raise ValueError("set a group id so the previous text can be replaced")

    with live_editor.LiveEditor(url) as editor:
        editor.remove_objects(group)
        editor.add_objects(objects)

    return {"sent": len(objects)}


class TextEditorHandler(BaseHTTPRequestHandler):
    config: EditorConfig

    def log_message(self, format, *args):
        pass

    def reply(self, status:int, body:bytes, content_type:str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def reply_json(self, status:int, data:Any):
        self.reply(status, json.dumps(data).encode("utf-8"), "application/json")

    def do_GET(self):
        url = urlparse(self.path)

        if url.path == "/":
            self.reply(200, EDITOR_PAGE.encode("utf-8"), "text/html; charset=utf-8")

        elif url.path == "/config":
            self.reply_json(200, self.config.to_dict())

        elif url.path == "/page":
            query = parse_qs(url.query)
            try:
                path = self.config.require_library().page_path(
                    int(query["font"][0]), int(query["quality"][0]), int(query["page"][0]))
            except (KeyError, ValueError, FileNotFoundError):
                path = None
            if path is None:
                self.reply(404, b"", "text/plain")
            else:
                self.reply(200, path.read_bytes(), "image/png")

        else:
            self.reply(404, b"", "text/plain")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        config = self.config
        try:
            settings = json.loads(self.rfile.read(length) or b"{}")
            match self.path:
                case "/config":
                    if "live_url" in settings:
                        config.live_url = settings["live_url"].strip() or live_editor.WEBSOCKET_URL
                    if "resources" in settings:
                        config.set_resources(settings["resources"])
                    config.save()
                    self.reply_json(200, config.to_dict())
                case "/preview":
                    self.reply_json(200, preview(settings, config.require_library()))
                case "/send":
                    self.reply_json(200, send(settings, config.require_library(), config.live_url))
                case "/export":
                    self.reply_json(200, {"string": build_objects(settings, config.require_library())[1].to_string()})
                case _:
                    self.reply_json(404, {"error": "unknown endpoint"})
        except Exception as error:
            self.reply_json(400, {"error": f"{type(error).__name__}: {error}"})


def create_server(config:EditorConfig, host:str="127.0.0.1", port:int=8765) -> ThreadingHTTPServer:
    handler = type("Handler", (TextEditorHandler,), {"config": config})
    return ThreadingHTTPServer((host, port), handler)


def main(argv:Optional[list[str]]=None):
    parser = argparse.ArgumentParser(description="Interactive text block editor for Geometry Dash text objects.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)

    config = EditorConfig()
    config.load()

    server = create_server(config, args.host, args.port)
    url = f"http://{args.host}:{server.server_address[1]}/"
    print(f"text editor running at {url}")
    print(f"settings are saved to {config.path}")
    if config.error:
        print(f"warning: {config.error}, set the folder in the editor page")

    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, (url,)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


EDITOR_PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>gmdkit text editor</title>
<style>
:root { --bg:#16181d; --panel:#1f232b; --line:#323844; --text:#e6e8ee; --muted:#8b93a3; --accent:#6aa8ff; --warn:#ff9b6a; --ok:#7dffa8; }
* { box-sizing:border-box; }
body { margin:0; height:100vh; display:flex; background:var(--bg); color:var(--text); font:13px/1.4 system-ui, sans-serif; }
aside { width:350px; flex:none; overflow-y:auto; background:var(--panel); border-right:1px solid var(--line); padding:12px 14px 40px; }
main { flex:1; position:relative; overflow:hidden; }
h1 { font-size:15px; margin:0 0 10px; }
details { border-top:1px solid var(--line); padding:6px 0; }
summary { cursor:pointer; color:var(--muted); font-weight:600; text-transform:uppercase; font-size:11px; letter-spacing:.06em; padding:4px 0; }
label { display:grid; grid-template-columns:110px 1fr; align-items:center; gap:8px; margin:5px 0; color:var(--muted); }
label.check { grid-template-columns:auto 1fr; }
label.wide { grid-template-columns:1fr; gap:3px; }
input, select, textarea, button { font:inherit; color:var(--text); background:#14171c; border:1px solid var(--line); border-radius:5px; padding:4px 6px; min-width:0; }
input[type=range] { padding:0; }
textarea { width:100%; height:110px; resize:vertical; font-family:ui-monospace, monospace; }
.row { display:flex; gap:6px; }
.row > * { flex:1; }
button { cursor:pointer; background:#2a3140; padding:6px 10px; }
button.primary { background:var(--accent); color:#0b1424; border-color:var(--accent); font-weight:600; }
.note { color:var(--muted); font-size:12px; margin:4px 0; word-break:break-all; }
.error { color:var(--warn); }
#status { margin-top:8px; color:var(--muted); white-space:pre-wrap; min-height:3em; }
#stats { position:absolute; left:10px; bottom:8px; color:var(--muted); pointer-events:none; }
#hint { position:absolute; right:10px; bottom:8px; color:var(--muted); pointer-events:none; }
#empty { position:absolute; inset:0; display:none; align-items:center; justify-content:center; color:var(--muted); font-size:15px; padding:20px; text-align:center; }
svg { width:100%; height:100%; display:block; cursor:grab; }
svg.dragging { cursor:grabbing; }
.grid { stroke:#232833; stroke-width:1; vector-effect:non-scaling-stroke; }
.axis { stroke:#3a4252; stroke-width:1; vector-effect:non-scaling-stroke; }
.outline { fill:rgba(106,168,255,.06); stroke:var(--accent); stroke-dasharray:4 3; stroke-width:1; vector-effect:non-scaling-stroke; }
.path { fill:none; stroke:#c792ff; stroke-dasharray:2 4; stroke-width:1; vector-effect:non-scaling-stroke; }
.anchor { fill:var(--warn); }
.pivot { stroke:var(--ok); stroke-width:2; vector-effect:non-scaling-stroke; }
.box { fill:rgba(255,255,255,.08); stroke:#9aa3b5; stroke-width:1; vector-effect:non-scaling-stroke; }
.boxtext { fill:#cfd5e2; font-family:sans-serif; font-weight:bold; }
</style>
</head>
<body>
<aside>
  <h1>Text block</h1>

  <details id="setup" open><summary>Setup</summary>
    <label class="wide">Game Resources folder <input id="cfg_resources" type="text" placeholder="...\Geometry Dash\Resources"></label>
    <label class="wide">WSLiveEditor url <input id="cfg_live_url" type="text"></label>
    <button id="cfg_apply">Apply</button>
    <div id="cfg_note" class="note"></div>
  </details>

  <textarea id="text">Geometry Dash
text block editor</textarea>
  <label>Font <select id="font"></select></label>
  <label>Quality <select id="quality"><option value="4">High (uhd)</option><option value="2">Medium (hd)</option><option value="1">Low</option></select></label>
  <label>Case <select id="case"><option>NONE</option><option>UPPER</option><option>LOWER</option></select></label>

  <details open><summary>Position</summary>
    <label>X <input id="x" type="number" value="0" step="1"></label>
    <label>Y <input id="y" type="number" value="0" step="1"></label>
    <label>Anchor X <input id="anchor_x" type="range" min="0" max="1" step="0.05" value="0.5"></label>
    <label>Anchor Y <input id="anchor_y" type="range" min="0" max="1" step="0.05" value="0.5"></label>
    <label class="check"><input id="world_anchor" type="checkbox"> World anchor (pivot)</label>
    <label>Pivot X <input id="world_anchor_x" type="number" value="0" step="1"></label>
    <label>Pivot Y <input id="world_anchor_y" type="number" value="0" step="1"></label>
  </details>

  <details open><summary>Layout</summary>
    <label>Align <select id="align"><option>LEFT</option><option>CENTER</option><option>RIGHT</option><option>JUSTIFY</option></select></label>
    <label>Vertical <select id="vertical_align"><option>TOP</option><option>CENTER</option><option>BOTTOM</option></select></label>
    <label>Width <input id="width" type="number" placeholder="auto" step="10"></label>
    <label>Height <input id="height" type="number" placeholder="auto" step="10"></label>
    <label class="check"><input id="break_words" type="checkbox"> Break long words</label>
    <label>Indent <input id="indent" type="number" value="0" step="1"></label>
    <label>Tab size <input id="tab_size" type="number" value="4" min="0" step="1"></label>
  </details>

  <details><summary>Padding</summary>
    <label>Left <input id="padding_left" type="number" value="0" step="1"></label>
    <label>Top <input id="padding_top" type="number" value="0" step="1"></label>
    <label>Right <input id="padding_right" type="number" value="0" step="1"></label>
    <label>Bottom <input id="padding_bottom" type="number" value="0" step="1"></label>
  </details>

  <details open><summary>Spacing</summary>
    <label>Letter <input id="letter_spacing" type="number" value="0" step="0.25"></label>
    <label>Word <input id="word_spacing" type="number" value="0" step="1"></label>
    <label>Line height <input id="line_height" type="number" placeholder="font" step="1"></label>
    <label>Line spacing <input id="line_spacing" type="number" value="0" step="1"></label>
    <label>Paragraph <input id="paragraph_spacing" type="number" value="0" step="1"></label>
    <label>Line offset X <input id="line_offset_x" type="number" value="0" step="1"></label>
    <label>Line offset Y <input id="line_offset_y" type="number" value="0" step="1"></label>
  </details>

  <details open><summary>Transform</summary>
    <label>Scale X <input id="scale_x" type="number" value="1" step="0.05"></label>
    <label>Scale Y <input id="scale_y" type="number" value="1" step="0.05"></label>
    <label>Rotation <input id="rotation" type="range" min="-180" max="180" step="1" value="0"></label>
    <label>Skew X <input id="skew_x" type="range" min="-80" max="80" step="1" value="0"></label>
    <label>Skew Y <input id="skew_y" type="range" min="-80" max="80" step="1" value="0"></label>
    <div class="row"><label class="check"><input id="flip_x" type="checkbox"> Flip X</label><label class="check"><input id="flip_y" type="checkbox"> Flip Y</label></div>
    <label>Glyph rotation <input id="glyph_rotation" type="range" min="-180" max="180" step="1" value="0"></label>
  </details>

  <details><summary>Path</summary>
    <label>Shape <select id="path"><option value="none">None</option><option value="circle">Circle</option><option value="ellipse">Ellipse</option></select></label>
    <label>Radius X <input id="path_radius_x" type="number" value="300" step="10"></label>
    <label>Radius Y <input id="path_radius_y" type="number" value="200" step="10"></label>
    <label>Start angle <input id="path_angle" type="range" min="-180" max="180" step="1" value="90"></label>
    <label class="check"><input id="path_reverse" type="checkbox"> Counterclockwise (text inside)</label>
    <div class="note">With a path, X / Y is the centre of the circle or ellipse and the anchor sits on it at the start angle.</div>
  </details>

  <details open><summary>Objects</summary>
    <label>Split <select id="split"><option value="none">Fewest objects</option><option value="newline">At newlines</option><option value="chars">At characters</option><option value="any">Every glyph</option></select></label>
    <label>Split chars <input id="split_chars" type="text" value=" "></label>
    <label class="check"><input id="portable" type="checkbox" checked> Portable (no kerning)</label>
    <label>Group ID <input id="group" type="number" value="9999" min="0" step="1"></label>
    <label class="check"><input id="live" type="checkbox"> Send to editor on change</label>
    <div class="row"><button class="primary" id="send">Send to editor</button><button id="export">Copy objects</button></div>
    <div id="status"></div>
  </details>
</aside>
<main>
  <svg id="view"><g id="world"></g></svg>
  <div id="empty"></div>
  <div id="stats"></div>
  <div id="hint">wheel: zoom · drag: pan · double click: fit</div>
</main>
<script>
const $ = id => document.getElementById(id);
const svg = $("view"), world = $("world");
const NS = "http://www.w3.org/2000/svg";
const STORAGE_KEY = "gmdkit-text-editor";
let view = { x: 0, y: 0, scale: 1 }, last = null, timer = null, pageCache = {}, fitted = false, ready = false;

function fields() {
  return [...document.querySelectorAll("aside [id]")].filter(el =>
    ["INPUT", "SELECT", "TEXTAREA"].includes(el.tagName) && !el.id.startsWith("cfg_"));
}

function settings() {
  const out = {};
  for (const el of fields()) out[el.id] = el.type === "checkbox" ? el.checked : el.value;
  return out;
}

function remember() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(settings())); } catch (e) {}
}

function restore() {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch (e) {}
  if (!saved) return;
  for (const el of fields()) {
    if (!(el.id in saved) || el.id === "font" || el.id === "live") continue;
    if (el.type === "checkbox") el.checked = saved[el.id]; else el.value = saved[el.id];
  }
  return saved.font;
}

function status(message, error) {
  $("status").textContent = message || "";
  $("status").className = error ? "error" : "";
}

async function post(path, body) {
  const response = await fetch(path, { method: "POST", body: JSON.stringify(body) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || response.statusText);
  return data;
}

function showConfig(config, savedFont) {
  $("cfg_resources").value = config.resources;
  $("cfg_live_url").value = config.live_url;
  $("cfg_note").innerHTML = "";
  const note = document.createElement("div");
  note.textContent = config.error ? config.error : `${config.fonts.length} fonts found · saved to ${config.config_file}`;
  if (config.error) note.className = "error";
  $("cfg_note").appendChild(note);

  const select = $("font"), current = savedFont ?? select.value;
  select.innerHTML = "";
  for (const id of config.fonts) {
    const option = document.createElement("option");
    option.value = id;
    option.textContent = id === 0 ? "0 - bigFont" : `${id} - gjFont${String(id).padStart(2, "0")}`;
    select.appendChild(option);
  }
  if (config.fonts.map(String).includes(String(current))) select.value = current;
  else if (config.fonts.includes(1)) select.value = "1";

  ready = config.fonts.length > 0;
  $("setup").open = !ready || $("setup").open;
  $("empty").style.display = ready ? "none" : "flex";
  $("empty").textContent = ready ? "" : "Set the game's Resources folder in Setup to load the fonts.";
  pageCache = {};
}

function applyView() {
  const r = svg.getBoundingClientRect();
  world.setAttribute("transform", `translate(${r.width / 2 + view.x} ${r.height / 2 + view.y}) scale(${view.scale})`);
}

function el(name, attrs, parent) {
  const node = document.createElementNS(NS, name);
  for (const k in attrs) node.setAttribute(k, attrs[k]);
  (parent || world).appendChild(node);
  return node;
}

function drawGrid(bounds) {
  const g = el("g", {});
  const step = 30;
  const [x0, y0, x1, y1] = bounds.map(v => Math.round(v / step) * step);
  for (let x = x0 - step * 10; x <= x1 + step * 10; x += step)
    el("line", { x1: x, y1: -(y1 + step * 10), x2: x, y2: -(y0 - step * 10), class: x === 0 ? "axis" : "grid" }, g);
  for (let y = y0 - step * 10; y <= y1 + step * 10; y += step)
    el("line", { x1: x0 - step * 10, y1: -y, x2: x1 + step * 10, y2: -y, class: y === 0 ? "axis" : "grid" }, g);
}

function pageAvailable(url) {
  if (!(url in pageCache)) {
    pageCache[url] = new Promise(resolve => { const img = new Image(); img.onload = () => resolve(true); img.onerror = () => resolve(false); img.src = url; });
  }
  return pageCache[url];
}

function extent(data) {
  const points = data.outline.concat(data.path, data.glyphs.map(g => [g.x, g.y]), [data.origin, data.anchor]);
  return [Math.min(...points.map(p => p[0])), Math.min(...points.map(p => p[1])), Math.max(...points.map(p => p[0])), Math.max(...points.map(p => p[1]))];
}

async function draw(data) {
  last = data;
  world.innerHTML = "";
  drawGrid(extent(data));
  el("polygon", { points: data.outline.map(p => `${p[0]},${-p[1]}`).join(" "), class: "outline" });
  if (data.path.length) el("polygon", { points: data.path.map(p => `${p[0]},${-p[1]}`).join(" "), class: "path" });

  const pages = {};
  for (const g of data.glyphs) if (!(g.page in pages)) pages[g.page] = await pageAvailable(data.page_url + g.page);

  const defs = el("defs", {});
  let clipId = 0;
  for (const g of data.glyphs) {
    const [a, b, c, d] = g.matrix;
    const group = el("g", { transform: `matrix(${a} ${-b} ${-c} ${d} ${g.x} ${-g.y})` });
    const [tx, ty, tw, th] = g.texture;
    if (pages[g.page] && tw && th) {
      const id = `clip${clipId++}`;
      const clip = el("clipPath", { id: id }, defs);
      el("rect", { x: tx, y: ty, width: tw, height: th }, clip);
      el("image", {
        href: data.page_url + g.page, width: data.page_size[0], height: data.page_size[1],
        transform: `translate(${-g.width / 2} ${-g.height / 2}) scale(${g.width / tw} ${g.height / th}) translate(${-tx} ${-ty})`,
        "clip-path": `url(#${id})`,
      }, group);
    } else {
      el("rect", { x: -g.width / 2, y: -g.height / 2, width: g.width, height: g.height, class: "box" }, group);
      const t = el("text", { x: 0, y: g.height * 0.3, "text-anchor": "middle", class: "boxtext", "font-size": g.height * 0.8 }, group);
      t.textContent = g.char;
    }
  }
  el("circle", { cx: data.anchor[0], cy: -data.anchor[1], r: 3 / view.scale, class: "anchor" });
  if ($("world_anchor").checked || data.path.length) {
    const s = 6 / view.scale, [px, py] = data.origin;
    el("path", { d: `M${px - s} ${-py}H${px + s}M${px} ${-py - s}V${-py + s}`, class: "pivot" });
  }

  if (!fitted) { fit(); fitted = true; }
  $("stats").textContent = `${data.objects} object${data.objects === 1 ? "" : "s"} · ${data.glyphs.length} glyphs · largest ${data.bytes}/400 bytes · kerning ${data.kerning} · quality ${$("quality").value}`;
}

function fit() {
  if (!last) return;
  const [x0, y0, x1, y1] = extent(last);
  const r = svg.getBoundingClientRect();
  const w = x1 - x0 || 100, h = y1 - y0 || 100;
  view.scale = Math.min(r.width / w, r.height / h) * 0.8;
  view.x = -((x0 + x1) / 2) * view.scale;
  view.y = ((y0 + y1) / 2) * view.scale;
  applyView();
}

async function refresh() {
  remember();
  if (!ready) return;
  try {
    const data = await post("/preview", settings());
    await draw(data);
    status("");
    if ($("live").checked) await sendToEditor(true);
  } catch (error) { status(error.message, true); }
}

async function sendToEditor(quiet) {
  try {
    const result = await post("/send", settings());
    status(`sent ${result.sent} objects to the editor`);
  } catch (error) { status(error.message, true); if (quiet) $("live").checked = false; }
}

function schedule() { clearTimeout(timer); timer = setTimeout(refresh, 120); }

for (const node of fields()) node.addEventListener("input", schedule);
$("cfg_apply").onclick = async () => {
  try {
    const config = await post("/config", { resources: $("cfg_resources").value, live_url: $("cfg_live_url").value });
    showConfig(config);
    fitted = false;
    refresh();
  } catch (error) { $("cfg_note").textContent = error.message; $("cfg_note").className = "note error"; }
};
$("send").onclick = () => sendToEditor(false);
$("export").onclick = async () => {
  try {
    const result = await post("/export", settings());
    await navigator.clipboard.writeText(result.string);
    status("object string copied to clipboard");
  } catch (error) { status(error.message, true); }
};

svg.addEventListener("wheel", event => {
  event.preventDefault();
  const r = svg.getBoundingClientRect();
  const mx = event.clientX - r.left - r.width / 2, my = event.clientY - r.top - r.height / 2;
  const factor = Math.exp(-event.deltaY * 0.0015);
  view.x = mx - (mx - view.x) * factor;
  view.y = my - (my - view.y) * factor;
  view.scale *= factor;
  applyView();
}, { passive: false });
let drag = null;
svg.addEventListener("pointerdown", e => { drag = { x: e.clientX - view.x, y: e.clientY - view.y }; svg.classList.add("dragging"); svg.setPointerCapture(e.pointerId); });
svg.addEventListener("pointermove", e => { if (drag) { view.x = e.clientX - drag.x; view.y = e.clientY - drag.y; applyView(); } });
svg.addEventListener("pointerup", () => { drag = null; svg.classList.remove("dragging"); });
svg.addEventListener("dblclick", fit);
window.addEventListener("resize", applyView);

const savedFont = restore();
fetch("/config").then(r => r.json()).then(config => { showConfig(config, savedFont); refresh(); });
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()