# Imports
import inspect
from typing import Self, Any
from collections.abc import Iterator, Iterable, Callable


def filter_kwargs(*functions:Callable, **kwargs) -> list[tuple[Callable,dict[str,Any]]]:
    """
    Filters keyword arguments to only those present on the given functions.

    Parameters
    ----------
    *functions : Callable
        One or more functions to retrieve the parameters from.
        
    **kwargs : dict[str,Any]
        The keyword arguments to filter.

    Returns
    -------
    func_kwargs : list[tuple[Callable,dict[str,any]]]
        A list containing functions and matching keyword arguments.

    """
    if not kwargs: return [(f, {}) for f in functions]
    
    new_kwargs = []
    
    for function in functions:
        sig = inspect.signature(function)
        
        new_kwargs.append({k: v for k, v in kwargs.items() if k in sig.parameters})
    
    return list(zip(functions, new_kwargs))


class ListClass(list):
    
    def __init__(self, *args):
        super().__init__(*args)

    def __add__(self, other) -> Self:
        return self.__class__(super().__add__(other))


    def __radd__(self, other) -> Self:
        return self.__class__(other + list(self))


    def __mul__(self, n) -> Self:
        return self.__class__(super().__mul__(n))


    def __rmul__(self, n) -> Self:
        return self.__class__(super().__rmul__(n))


    def __getitem__(self, item) -> Self:
        result = super().__getitem__(item)
        return self.__class__(result) if isinstance(item, slice) else result

    
    def __repr__(self):
        return f"{self.__class__}({list(self)})"
        
        
    def copy(self) -> Self:
        return self.__class__(self)
    
    
    def where(self, *conditions:Callable, **kwargs:Any) -> Self:
        """
        Filters a list where an item matches at least one condition.

        Parameters
        ----------
        *conditions : Callable
            One or more functions that take in an object and return TRUE or FALSE.
            
        **kwargs : Any
            Optional keyword arguments to pass to the called functions.

        Returns
        -------
        Self
            A new class instance containing filtered objects.
        """
        result = self.__class__()
        
        f_kw = filter_kwargs(*conditions, **kwargs)

        for item in self:
            for condition, nkwargs in f_kw:
                if condition(item, **nkwargs):

                    result.append(item)
        
        return result
    
    
    def apply(self, *functions:Callable, **kwargs) -> Self:
        """
        Applies a series of functions in place on each list member.

        Parameters
        ----------
        *functions : Callable
            One or more functions that will be applied on each list member sequentially.

        **kwargs : Any
            Optional keyword arguments to pass to the called functions.
            
        Returns
        -------
        Self
            The class instance, allows method chaining.
            
        Example
        -------
        new_list = ListClass(1,2,3)
        
        new_list.apply(lambda x: x*2)
        
        print(new_list)  # Output: [2, 4, 6]

        """        
        f_kw = filter_kwargs(*conditions, **kwargs)
            
        for i, item in enumerate(self):
            for function, nkwargs in f_kw:
                if (val:=function(item, **nkwargs)) is not None:
                    self[i] = val
        
        return self
    
    
    def exclude(self, *conditions:Callable[..., bool], **kwargs: Any) -> Self:
        """
        Returns all items that meet at least one condition and removes them from the list.

        Parameters
        ----------
        *conditions : Callable[..., bool]
            One or more conditions that take in an object and return either TRUE or FALSE.

        **kwargs : Any
            Optional keyword arguments to pass to the called functions.
            
        Returns
        -------
        Self
            A new class instance containing the filtered objects.
        """
        ex = self.__class__()
        
        keep = []

        f_kw = filter_kwargs(*conditions, **kwargs)

        for item in self:
            for condition, nkwargs in f_kw:
                if condition(item,**nkwargs):
                    ex.append(item)
                    break
            else:
                keep.append(item)
    
        self[:] = keep
        return ex
    
    
    def values(self, *functions:Callable[..., Iterable[Any]], **kwargs:Any) -> list:
        """
        Applies one or more functions to each item and collects all resulting values in a list.

        Parameters
        ----------
        *functions : Callable
            One or more functions that take in an object and returns a list of values.
            
        **kwargs : Any
            Optional keyword arguments to pass to the called functions.

        Returns
        -------
        list
            A list containing the collected values.
        """
        result = list()
        f_kw = filter_kwargs(*functions, **kwargs)
        print(f_kw)
        for item in self:
            for function, nkwargs in f_kw:
                result.extend(function(item,**nkwargs) or [])
                
        return result
    
    
    def unique_values(self, *functions:Callable[..., set[Any]], **kwargs:Any) -> set:
        """
        Applies one or more functions to each item and collects all unique values in a set.

        Parameters
        ----------
        *functions : Callable[..., set[Any]]
            One or more functions that take in an object and returns a set of values.
            
        **kwargs : Any
            Optional keyword arguments to pass to the called functions.

        Returns
        -------
        set
            A set containing the unique collected values.

        """
        result = set()
    
        f_kw = filter_kwargs(*functions, **kwargs)
        
        for item in self:
            for function, nkwargs in f_kw:
                result.update(function(item,**nkwargs) or [])
                
        return result
    
    
    def shared_values(self, *functions:Callable[..., set[Any]], **kwargs:Any) -> set:
        """
        Applies one or more functions to each item and collects values shared by all items in a set.

        Parameters
        ----------
        *functions : Callable[..., set[Any]]
            One or more functions that take in an object and returns a set of values.
            
        **kwargs : Any
            Optional keyword arguments to pass to the called functions.

        Returns
        -------
        set
            A set containing the shared collected values.

        """
        result = None
        
        f_kw = filter_kwargs(*functions, **kwargs)
        
        for item in self:
            for function, nkwargs in f_kw:
                val = set(function(item,**nkwargs) or [])
                
                if result is None:
                    result = val
                
                else:
                    result &= val
                
                if not result:
                    return set()
        
        return result
    
        
class DictClass(dict):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    @classmethod
    def fromkeys(cls, iterable, value=None):
        return cls({k: value for k in iterable})


    def __repr__(self):
        return f"{self.__class__}({dict(self)})"


    def copy(self):
        return self.__class__(self)


    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        return self.__class__(dict(self, **other))


    def __ror__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        return self.__class__(dict(other, **self))
    
    
    def pluck(self, *keys:str, ignore_missing:bool=False) -> list:
        """
        Retrieves the values of the specified keys from the object.

        Parameters
        ----------
        *keys : str
            One or more keys to retrieve the values of.
        
        ignore_missing: bool
            Whether missing keys should be skipped. Defaults to False.
            
        Returns
        -------
        list
            Returns a list containing the values of the specified keys.

        """
        result = list()
        
        if ignore_missing:
            for k in set(keys) & self.keys():
                result.append(self.get(k))
        else:
            for k in keys:
                result.append(self.get(k))          
        
        return result

        
class StrClass(str):
    
    def __new__(cls, value):
        return super().__new__(cls, value)
   
    
    def _wrap(self, result):
        return self.__class__(result) if isinstance(result, str) else result

    def __add__(self, other):
        return self._wrap(super().__add__(other))


    def __radd__(self, other):
        return self._wrap(other + super())


    def __getitem__(self, key):
        result = super().__getitem__(key)
        return self._wrap(result)


    def replace(self, old, new, count=-1):
        return self._wrap(super().replace(old, new, count))


    def upper(self):
        return self._wrap(super().upper())


    def lower(self):
        return self._wrap(super().lower())


    def capitalize(self):
        return self._wrap(super().capitalize())


    def title(self):
        return self._wrap(super().title())


    def strip(self, chars=None):
        return self._wrap(super().strip(chars))


    def lstrip(self, chars=None):
        return self._wrap(super().lstrip(chars))


    def rstrip(self, chars=None):
        return self._wrap(super().rstrip(chars))


    def join(self, iterable):
        return self._wrap(super().join(iterable))