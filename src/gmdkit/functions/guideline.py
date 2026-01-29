# Package Imports
from gmdkit.models.prop.guideline import GuidelineList, Guideline
from gmdkit.constants.game import guideline as guide_color


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
