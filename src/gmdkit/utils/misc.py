# Imports
from typing import Iterable, Literal


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


def split_digit_list(value:int, leading_digit:Literal[1,2,3,4,5,6,7,8,9]=1):
    
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    s = str(value)
    
    if not s.startswith(leading_digit):
        raise ValueError("Value must have {leading_digit} as a leading digit")
    
    return [int(d) for d in s[1:]]
    

def join_digit_list(digit_list, leading_digit:Literal[1,2,3,4,5,6,7,8,9]=1):
    return int(
        leading_digit +
        "".join(str(max(0, min(int(d), 9))) for d in digit_list)
        )
        
    