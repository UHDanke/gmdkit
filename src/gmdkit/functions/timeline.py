# Imports
import math
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Union

# Package Imports
from gmdkit.models.level import Level
from gmdkit.models.object import Object
from gmdkit.models import interfaces
from gmdkit.models.interfaces.teleport import TeleportSettings
from gmdkit.utils.functions import transform_corners, bounds
from gmdkit.constants.game import speed as SPEED



SPEED_VALUES = {1: SPEED.SLOW, 2: SPEED.FAST, 3: SPEED.VERY_FAST, 4: SPEED.SUPER_FAST}
PLATFORMER_SPEED = SPEED.SPAWN_ORDER
TRIGGER_OFFSET = 15.0
REVERSE, TIMEWARP, SONG, ROTATE, TELEPORT = -1, -2, -3, -4, -5
SPEED_PORTALS = {200: 1, 201: 0, 202: 2, 203: 3, 1334: 4}
SPECIAL = {1917: REVERSE, 1935: TIMEWARP, 1934: SONG, 2900: ROTATE, 2902: TELEPORT, 3022: TELEPORT, 3027: TELEPORT}
SPEED_OBJECTS = set(SPEED_PORTALS) | set(SPECIAL)
EDGE_ALWAYS = {200, 201, 202, 203, 1334, 2902}
EDGE_NEVER = {36, 84, 141, 1022, 1330, 1333, 1594, 1704, 1751, 3027}
CAN_REVERSE = {35, 36, 67, 84, 140, 141, 1022, 1330, 1332, 1333, 3004, 3005, 3027}
REVERSE_KEY = 117

BoxSize = Union[dict[int, tuple[float, float]], Callable[[Object], Optional[tuple[float, float]]], None]


def speed_value(speed_type: int) -> float:
    return SPEED_VALUES.get(int(speed_type), SPEED.NORMAL)

def _base(obj: Object) -> interfaces.BaseObject:
    return obj.require_interface(interfaces.BaseObject)


def _effect_intf(obj: Object) -> Optional[interfaces.EffectObject]:
    return obj.require_interface(interfaces.EffectObject, None)


def is_reversed(obj: Object) -> bool:
    if int(_base(obj).obj_id) not in CAN_REVERSE:
        return False
    intf = obj.require_interface((interfaces.OrbObject, interfaces.PadObject), None)
    if intf is not None:
        return bool(intf.reverse)
    return bool(obj.get(REVERSE_KEY, False))


def object_direction(obj: Object) -> int:
    intf = _base(obj)
    fx, fy = bool(intf.flip_x), bool(intf.flip_y)
    rot = intf.rotation
    if rot == 0 and (intf.skew_x or intf.skew_y):
        rot = intf.skew_x
    r = int(rot) % 360 if rot >= 0 else -(-int(rot) % 360)
    a0, a180 = r == 0, abs(r) == 180
    r90, r270 = r in (90, -270), r in (-90, 270)
    none, only_y, only_x, both = (not fx and not fy), (not fx and fy), (fx and not fy), (fx and fy)

    if a0 and none:
        slope = 0
    elif both:
        slope = 0 if a180 else 3 if a0 else 4 if r270 else 5 if r90 else 0
    elif a0 and only_y:
        slope = 1
    elif only_x and a180:
        slope = 1
    elif only_x and a0:
        slope = 2
    elif a180 and only_y:
        slope = 2
    elif none:
        slope = 3 if a180 else 4 if r90 else 5 if r270 else 0
    elif r90 and only_x:
        slope = 6
    elif only_y:
        slope = 6 if r270 else 7 if r90 else 0
    else:
        slope = 7 if (r270 and only_x) else 0
    return {2: 3, 3: 3, 4: 2, 5: 1, 6: 1, 7: 2}.get(slope, 4)

@dataclass
class TimelineObject:
    obj: Object
    uid: int
    kind: int
    position: tuple[float, float]
    channel: int = 0
    order: int = 0
    teleport_target: Optional[tuple[float, float]] = None

    @property
    def obj_id(self) -> int:
        return int(_base(self.obj).obj_id)

    @property
    def arrow(self) -> Optional[interfaces.GameplayArrow]:
        return self.obj.require_interface(interfaces.GameplayArrow, None)


def speed_kind(obj: Object) -> int:
    oid = int(_base(obj).obj_id)
    if oid == 1917:
        return REVERSE
    kind = SPEED_PORTALS.get(oid, SPECIAL.get(oid, 0))
    return REVERSE if is_reversed(obj) else kind


def counts_for_timeline(obj: Object) -> bool:
    intf = _effect_intf(obj)
    if intf is None or not intf.editor_preview:
        return False
    oid = int(intf.obj_id)
    if oid in SPEED_OBJECTS:
        return True
    if not is_reversed(obj):
        return False
    return oid in CAN_REVERSE


def _rect(obj: Object, box_size: BoxSize) -> tuple[float, float, float, float]:
    intf = _base(obj)
    size = box_size(obj) if callable(box_size) else (box_size or {}).get(int(intf.obj_id))
    if size is None:
        rect = intf.hitbox_rect
        if rect is not None:
            return rect
        x, y = intf.get_positions()
        return x, y, 0.0, 0.0
    scale_x, scale_y, rotation, _ = intf.node_transform
    center = intf.hitbox_center or intf.get_positions()
    angle = -math.radians(rotation)
    cos, sin = math.cos(angle), math.sin(angle)
    corners = transform_corners(abs(scale_x) * size[0] / 2, abs(scale_y) * size[1] / 2, center, (cos, sin, -sin, cos))
    return bounds(corners)


def _switches_channel(it: TimelineObject) -> Optional[int]:
    arrow = it.arrow
    if arrow is not None and arrow.change_channel:
        return int(arrow.target_channel)
    return None


def _sort_channels(items: list[TimelineObject]) -> list[TimelineObject]:
    dirs: dict[int, int] = {}
    for it in items:
        target = _switches_channel(it)
        if target is not None:
            dirs.setdefault(target, object_direction(it.obj))
    channels: dict[int, list[TimelineObject]] = {}
    for it in items:
        channels.setdefault(it.channel, []).append(it)

    def key(it: TimelineObject):
        d = dirs.get(it.channel, 4)
        x, y = it.position
        v = {1: it.order + y, 2: it.order - y, 3: it.order - x}.get(d, it.order + x)
        return (it.order, int(v), it.uid)

    for lst in channels.values():
        lst.sort(key=key)

    out: list[TimelineObject] = []
    current = channels.get(0)
    while current:
        it = current.pop(0)
        out.append(it)
        target = _switches_channel(it)
        if target is not None:
            current = channels.get(target)
    for lst in channels.values():
        out += lst
        lst.clear()
    return out


def collect_timeline_objects(
        objects: Iterable[Object],
        *,
        box_size: BoxSize = None,
        teleport_target: Optional[Callable[[Object, int], Optional[tuple[float, float]]]] = None,
        ) -> list[TimelineObject]:
    objects = list(objects)
    by_group: dict[int, Object] = {}
    for o in objects:
        for g in _base(o).groups:
            by_group.setdefault(int(g), o)

    items: list[TimelineObject] = []
    for uid, o in enumerate(objects):
        if not counts_for_timeline(o):
            continue
        intf = _effect_intf(o)
        it = TimelineObject(o, uid, speed_kind(o), intf.get_positions(), int(intf.channel), int(intf.order))
        if it.kind == TELEPORT:
            tp = o.require_interface(TeleportSettings, None)
            target = int(getattr(tp, 'target_id', 0) or 0)
            dest = teleport_target(o, target) if teleport_target else None
            if dest is None:
                t = by_group.get(target)
                dest = _base(t).get_positions() if t is not None else it.position
            it.teleport_target = dest
        items.append(it)

    items = _sort_channels(items)

    vertical = reversed_ = False
    for it in items:
        oid = it.obj_id
        intf = _effect_intf(it.obj)
        trig = it.obj.require_interface(interfaces.TriggerObject, None)
        touch = bool(trig.touch_trigger) if trig is not None else False
        edge = oid not in EDGE_NEVER and (oid in EDGE_ALWAYS or touch)
        if edge and not intf.center_effect:
            rx, ry, w, h = _rect(it.obj, box_size)
            x, y = rx + w / 2, ry + h / 2
            if not vertical:
                x = rx + w + TRIGGER_OFFSET if reversed_ else rx - TRIGGER_OFFSET
            else:
                y = ry - TRIGGER_OFFSET if reversed_ else ry + h + TRIGGER_OFFSET
            it.position = (x, y)
        if it.kind == ROTATE:
            arrow = it.arrow
            if not arrow.channel_only:
                vertical = int(arrow.dir_y_neg) in (3, 4)
                reversed_ = int(arrow.dir_x_pos) in (1, 3)
        elif it.kind == REVERSE:
            reversed_ = not reversed_

    return _sort_channels(items)


@dataclass
class Timeline:
    objects: list[TimelineObject] = field(default_factory=list)
    start_speed: int = 0
    platformer: bool = False
    ignore_timewarp: bool = False
    include_song: bool = False

    @classmethod
    def from_objects(cls, objects: Iterable[Object], start_speed: int = 0, platformer: bool = False, **kw):
        coll = {k: kw.pop(k) for k in ('box_size', 'teleport_target') if k in kw}
        return cls(collect_timeline_objects(objects, **coll), int(start_speed), platformer, **kw)

    @classmethod
    def from_level(cls, lvl: Level, **kw):
        settings = lvl.start.require_interface(interfaces.LevelSettings)
        return cls.from_objects(lvl.objects, int(settings.speed), bool(settings.platformer_mode), **kw)

    def _effect(self, it: TimelineObject, st: dict):
        k = it.kind
        jump = (0.0, 0.0)
        if k >= 0:
            st['speed'] = speed_value(k)
        elif k == TIMEWARP:
            if not self.ignore_timewarp:
                st['mod'] = float(it.obj.require_interface(interfaces.TimewarpTrigger).time_mod)
        elif k == REVERSE:
            st['rev'] = not st['rev']
        elif k == ROTATE:
            arrow = it.arrow
            if not arrow.channel_only:
                st['vert'] = int(arrow.dir_y_neg) in (3, 4)
                st['rev'] = int(arrow.dir_x_pos) in (1, 3)
            if arrow.change_channel:
                st['channel'] = int(arrow.target_channel)
        elif k == TELEPORT:
            tp = it.obj.require_interface(TeleportSettings, None)
            tx, ty = it.teleport_target or it.position
            jx, jy = tx - it.position[0], ty - it.position[1]
            if tp is not None:
                jx = 0.0 if tp.ignore_x else jx
                jy = 0.0 if tp.ignore_y else jy
            jump = (jx, jy)
        return jump

    @staticmethod
    def _step(st: dict, px: float, py: float) -> tuple[float, float, float]:
        dx = (px if px > 0 else 0.0) - st['x']
        dy = (py if py > 0 else 0.0) - st['y']
        if not st['vert']:
            ok = dx < 0 if st['rev'] else dx > 0
            if not ok:
                dx = 0.0
            return abs(dx), dx, dy
        ok = dy > 0 if st['rev'] else dy < 0
        if not ok:
            dy = 0.0
        return abs(dy), dx, dy

    @staticmethod
    def _advance(st: dict, old_vert: bool, dx: float, dy: float, jump):
        if not old_vert or not st['vert']:
            st['x'] += dx
        if old_vert or st['vert']:
            st['y'] += dy
        st['x'] += jump[0]
        st['y'] += jump[1]

    def _start(self) -> dict:
        return dict(x=0.0, y=0.0, vert=False, rev=False, mod=1.0, speed=speed_value(self.start_speed), channel=0)

    def time_for_pos(self, x: float, y: float = 0.0, channel: int = 0, order: int = 0) -> float:
        if x <= 0:
            return 0.0
        if self.platformer:
            return x / PLATFORMER_SPEED
        st = self._start()
        if not self.objects:
            return x / st['speed']
        t = 0.0
        max_order: dict[int, int] = {}
        for it in self.objects:
            if it.kind == SONG and not self.include_song:
                continue
            seg_speed = st['speed'] * st['mod']
            prev = max_order.get(st['channel'], 0)
            if prev < it.order:
                max_order[st['channel']] = it.order
            px, py = it.position
            dist, dx, dy = self._step(st, px, py)
            if ((st['channel'] == channel or channel == -1)
                    and (order < 1 or max_order.get(st['channel'], 0) >= order or prev == order)):
                if not st['vert']:
                    if min(st['x'], px) <= x <= max(st['x'], px):
                        return t + abs(st['x'] - x) / seg_speed
                elif min(st['y'], py) <= y <= max(st['y'], py):
                    return t + abs(st['y'] - y) / seg_speed
            t += dist / seg_speed
            old_vert = st['vert']
            jump = self._effect(it, st)
            self._advance(st, old_vert, dx, dy, jump)
        rest = (st['y'] - y) if st['vert'] else (st['x'] - x)
        return t + abs(rest) / (st['speed'] * st['mod'])

    def pos_for_time(self, time: float) -> tuple[float, float]:
        if self.platformer or not self.objects:
            sp = PLATFORMER_SPEED if self.platformer else speed_value(self.start_speed)
            return (time * sp, 0.0)
        st = self._start()
        elapsed = 0.0

        def move(remaining):
            d = remaining * st['speed'] * st['mod']
            if st['rev'] != st['vert']:
                d = -d
            if st['vert']:
                st['y'] += d
            else:
                st['x'] += d
            return (st['x'], st['y'])

        for it in self.objects:
            px, py = it.position
            if it.channel == st['channel']:
                dist, dx, dy = self._step(st, px, py)
            else:
                dist, dx, dy = 0.0, 0.0, 0.0
            end = elapsed + dist / (st['speed'] * st['mod'])
            if time <= end:
                return move(time - elapsed)
            old_vert = st['vert']
            jump = self._effect(it, st)
            self._advance(st, old_vert, dx, dy, jump)
            elapsed = end
        return move(time - elapsed)