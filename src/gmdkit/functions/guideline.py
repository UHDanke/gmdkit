# Imports
from typing import Optional

# Package Imports
from gmdkit.models.prop.guideline import GuidelineList, Guideline
from gmdkit.constants.game import guideline as guide_color


def bpm_guideline(
        guideline:Optional[GuidelineList]=None,
        bpm:float=60.0, 
        bpb:int=1, 
        start:float=0.0, 
        trim_start:float=0.0,
        trim_end:float=100.0, 
        bar_color:float=guide_color.YELLOW, 
        beat_color:float=guide_color.ORANGE
        ) -> GuidelineList:
    """
    Adds BPM lines to a guideline object.

    Parameters
    ----------
    guideline : Optional[GuidelineList], optional
        The guideline to modify, creates a new guideline if left as None.
    bpm : float, optional
        Bars per minute, defaults to 60.
    bpb : int, optional
        Beats per bar, defaults to 1.
    start : float, optional
        The start point of the beat, defaults to 0.
    trim_start : float, optional
        Trims beats before this time, defaults to 0.
    trim_end : float, optional
        Trims beats after this time, defaults to 60.
    bar_color : float, optional
        The color used for bar lines, defaults to guide_color.YELLOW.
    beat_color : float, optional
        The color used for the beat lines, defaults to guide_color.ORANGE.

    Returns
    -------
    GuidelineList

    """
    
    guideline = GuidelineList() if guideline is None else guideline
    interval = 60.0 / (bpm * bpb)
    time = trim_start
    
    if start < trim_start:
        i = int((trim_start - start) // interval)
    else:
        i = 0

    time = start + i * interval
    
    while time <= trim_end:
       if i % bpb == 0:
           color = bar_color
       else:
           color = beat_color

       guideline.append(Guideline(time=time,color = color))
       time += interval
       i += 1
       
    return guideline
