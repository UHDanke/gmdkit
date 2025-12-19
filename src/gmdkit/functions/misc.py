# Imports
import math
from typing import Iterable

# Package Imports
from gmdkit.models.prop.guideline import GuidelineList, Guideline
from gmdkit.constants.game import guideline as guide_color


def next_free(
        values:Iterable[int],
        start:int=0,
        vmin:int=-math.inf,
        vmax:int=math.inf,
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
    result = []

    def range_search(start,stop,step):
        
        nonlocal result
        
        for i in range(start,stop+step,step):
            
            if len(result) > count: 
                break
            
            if i not in used: 
                result.add(i)
    
    if start >= 0:
        range_search(start, vmax, 1)
    
    if start < 0 or len(result) < count: 
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
