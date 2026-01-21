# Imports
from typing import Iterable

# Package Imports
from gmdkit.models.prop.guideline import GuidelineList, Guideline
from gmdkit.constants.game import guideline as guide_color


def next_free(
        values:Iterable[int],
        start:int|None=None,
        vmin:int=-2**31,
        vmax:int=2**31-1,
        count:int=1
        ) -> list[int]:
    """
    Returns the next unused integer from a list, within the given limits.
    Negative numbers are returned counting down from -1.

    Parameters
    ----------
    values : Iterable[int]
        Currently used values.
        
    start : int, optional
        The current next free value, used to speed up iterative searches over large lists. Defaults to 0.
    
    vmin : int, optional
        The minimum value that can be returned. Defaults to -inf.
    
    vmax : int, optional
        The maximum value that can be returned. Defaults to inf.
    
    count : int, optional
        The number of values to return. Defaults to 1.
        
    Returns
    -------
    new_ids : list[int]
        A list of ids returned.
    """
    used = set(values)
    used.add(0)
    result = []

    def range_search(start: int, stop: int, step: int):
        nonlocal result
        i = start
        while (i < stop if step > 0 else i > stop):
            if len(result) >= count:
                break
            if i not in used:
                result.append(i)
            i += step


    if vmin > vmax: return result
    if start is None:
        start = 0 if vmin <= 0 else vmin
    else:
        if start < vmin:
            start = vmin
        elif start > vmax:
            start = -1 if vmin < 0 else vmax
        
    if start is not None and start <= vmax:
        range_search(start, vmax, 1)

    if len(result) < count and start is not None and start >= vmin:
        range_search(start, vmin, -1)
    
    return result


def bpm_guideline(bpm, bpb=1, beat_start=0, start=0, end=60, bar_color=guide_color.YELLOW, beat_color=guide_color.ORANGE):
    result = GuidelineList()
    interval = 60.0 / (bpm * bpb)
    time = start
    
    if beat_start < start:
        i = int((start - beat_start) // interval)
    else:
        i = 0

    time = beat_start + i * interval
    
    while time <= end:
       if i % bpb == 0:
           color = bar_color
       else:
           color = beat_color

       result.append(Guideline(time=time,color = color))
       time += interval
       i += 1
       
    return result
