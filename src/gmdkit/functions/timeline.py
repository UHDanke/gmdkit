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
TPS = 480
TICK_EPS = 1e-6

BoxSize = Union[dict[int, tuple[float, float]], Callable[[Object], Optional[tuple[float, float]]], None]


def speed_value(speed_type: int) -> float:
    return SPEED_VALUES.get(int(speed_type), SPEED.NORMAL)

def ticks_to_cover(dist: float, step: float) -> int:
    if dist <= 0:
        return 0
    return max(0, math.ceil(dist / step - TICK_EPS))

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
    by_group: dict[object, Object] = {}
    for o in objects:
        for g in _base(o).groups:
            by_group.setdefault(g, o)

    items: list[TimelineObject] = []
    for uid, o in enumerate(objects):
        if not counts_for_timeline(o):
            continue
        intf = _effect_intf(o)
        it = TimelineObject(o, uid, speed_kind(o), intf.get_positions(), int(intf.channel), int(intf.order))
        if it.kind == TELEPORT:
            tp = o.require_interface(TeleportSettings, None)
            target = getattr(tp, "target_id", 0) or 0
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
class TimelineToken:
    kind: str = ""
    index: int = 0
    tick: int = 0
    state: Optional[dict] = None
    max_order: dict = field(default_factory=dict)

    def save(self, kind: str, index: int, tick: int, state: dict, max_order: Optional[dict] = None):
        self.kind = kind
        self.index = index
        self.tick = tick
        self.state = dict(state)
        self.max_order = dict(max_order or {})


@dataclass
class Timeline:
    objects: list[TimelineObject] = field(default_factory=list)
    start_speed: int = 0
    platformer: bool = False
    ignore_timewarp: bool = False
    include_song: bool = False
    tps: int = TPS

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

    def _tick_step(self, st: dict) -> float:
        return st['speed'] * st['mod'] / self.tps

    @staticmethod
    def _direction(st: dict) -> int:
        return -1 if st['rev'] != st['vert'] else 1

    def _pass(self, it: TimelineObject, st: dict, n: int, step: float, dist: float, dx: float, dy: float):
        sign = self._direction(st)
        over = n * step - dist
        ox, oy = (0.0, sign * over) if st['vert'] else (sign * over, 0.0)
        old_vert = st['vert']
        jump = self._effect(it, st)
        self._advance(st, old_vert, dx, dy, jump)
        st['x'] += ox
        st['y'] += oy

    @staticmethod
    def _behind(st: dict, x: float, y: float) -> bool:
        if not st['vert']:
            return x > st['x'] if st['rev'] else x < st['x']
        return y < st['y'] if st['rev'] else y > st['y']

    def tick_for_pos(self, x: float, y: float = 0.0, channel: int = 0, order: int = 0,
                     token: Optional[TimelineToken] = None) -> int:
        if x <= 0:
            return 0
        if self.platformer:
            return ticks_to_cover(x, PLATFORMER_SPEED / self.tps)
        st = self._start()
        if not self.objects:
            return ticks_to_cover(x, self._tick_step(st))
        begin, tick = 0, 0
        max_order: dict[int, int] = {}
        if (token is not None and token.kind == "pos" and token.state is not None
                and not self._behind(token.state, x, y)):
            begin, tick = token.index, token.tick
            st, max_order = dict(token.state), dict(token.max_order)
        for i in range(begin, len(self.objects)):
            it = self.objects[i]
            if it.kind == SONG and not self.include_song:
                continue
            if token is not None:
                token.save("pos", i, tick, st, max_order)
            step = self._tick_step(st)
            prev = max_order.get(st['channel'], 0)
            if prev < it.order:
                max_order[st['channel']] = it.order
            px, py = it.position
            dist, dx, dy = self._step(st, px, py)
            n = ticks_to_cover(dist, step)
            if ((st['channel'] == channel or channel == -1)
                    and (order < 1 or max_order.get(st['channel'], 0) >= order or prev == order)):
                travel = self._direction(st) * n * step
                if not st['vert']:
                    a, q, b = st['x'], x, st['x'] + travel
                    end = px
                else:
                    a, q, b = st['y'], y, st['y'] + travel
                    end = py
                if min(a, b, end) <= q <= max(a, b, end):
                    return tick + ticks_to_cover(abs(a - q), step)
            tick += n
            self._pass(it, st, n, step, dist, dx, dy)
        if token is not None:
            token.save("pos", len(self.objects), tick, st, max_order)
        rest = (st['y'] - y) if st['vert'] else (st['x'] - x)
        return tick + ticks_to_cover(abs(rest), self._tick_step(st))

    def time_for_pos(self, x: float, y: float = 0.0, channel: int = 0, order: int = 0,
                     token: Optional[TimelineToken] = None) -> float:
        return self.tick_for_pos(x, y, channel, order, token) / self.tps

    def tick_for_obj(self, obj: Object, token: Optional[TimelineToken] = None) -> int:
        x, y = _base(obj).get_positions()
        intf = _effect_intf(obj)
        if intf is None:
            return self.tick_for_pos(x, y, token=token)
        return self.tick_for_pos(x, y, int(intf.channel), int(intf.order), token)

    def time_for_obj(self, obj: Object, token: Optional[TimelineToken] = None) -> float:
        return self.tick_for_obj(obj, token) / self.tps

    def pos_for_tick(self, tick: int, token: Optional[TimelineToken] = None) -> tuple[float, float]:
        if self.platformer or not self.objects:
            sp = PLATFORMER_SPEED if self.platformer else speed_value(self.start_speed)
            return (tick * sp / self.tps, 0.0)
        st = self._start()
        begin, elapsed = 0, 0
        if token is not None and token.kind == "tick" and token.state is not None and token.tick <= tick:
            begin, elapsed, st = token.index, token.tick, dict(token.state)

        def move(ticks):
            d = self._direction(st) * ticks * self._tick_step(st)
            if st['vert']:
                return (st['x'], st['y'] + d)
            return (st['x'] + d, st['y'])

        for i in range(begin, len(self.objects)):
            it = self.objects[i]
            if token is not None:
                token.save("tick", i, elapsed, st)
            step = self._tick_step(st)
            px, py = it.position
            if it.channel == st['channel']:
                dist, dx, dy = self._step(st, px, py)
            else:
                dist, dx, dy = 0.0, 0.0, 0.0
            n = ticks_to_cover(dist, step)
            if tick <= elapsed + n:
                return move(tick - elapsed)
            self._pass(it, st, n, step, dist, dx, dy)
            elapsed += n
        if token is not None:
            token.save("tick", len(self.objects), elapsed, st)
        return move(tick - elapsed)

    def pos_for_time(self, time: float, token: Optional[TimelineToken] = None) -> tuple[float, float]:
        return self.pos_for_tick(math.floor(time * self.tps + TICK_EPS), token)