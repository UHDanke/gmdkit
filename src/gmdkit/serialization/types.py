# Package Imports
from gmdkit.serialization.functions import filter_kwargs

# Imports
from typing import Self, Any
from collections.abc import Iterable, Callable
from enum import IntEnum


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
        return f"{self.__class__.__name__}({super().__repr__()})"
        
        
    def copy(self) -> Self:
        return self.__class__(self)
    
    @classmethod
    def wrap(cls, *args:Any):
        return cls(args)
        
    
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
        
        funcs = filter_kwargs(*conditions, **kwargs)

        for item in self:
            for condition in funcs:
                if condition(item):
                    result.append(item)
                    break
        
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
        funcs = filter_kwargs(*functions, **kwargs)
            
        for i, item in enumerate(self):
            val = item
            for function in funcs:
                new = function(val)
                if new is not None:
                    val = new
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

        funcs = filter_kwargs(*conditions, **kwargs)

        for item in self:
            for condition in funcs:
                if condition(item):
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
        funcs = filter_kwargs(*functions, **kwargs)
        for item in self:
            for function in funcs:
                vals = function(item) 
                if vals:
                    result.extend(vals)
                
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
    
        funcs = filter_kwargs(*functions, **kwargs)
        
        for item in self:
            for function in funcs:
                vals = function(item) 
                if vals:
                    result.update(vals)
                
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
        
        funcs = filter_kwargs(*functions, **kwargs)
        
        for item in self:
            for function in funcs:
                vals = function(item)
                val = vals if isinstance(vals, set) else set(vals or ())
                
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
    def fromkeys(cls, iterable, value: Any = None):
        return cls(dict.fromkeys(iterable, value))


    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


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
        key_set = set(keys)
        
        if ignore_missing:
            for k in key_set & self.keys():
                result.append(self.get(k))
        else:
            for k in keys:
                result.append(self.get(k))          
        
        return result


    def discard(self, *keys:str, ignore_missing:bool=False) -> list:
        """
        Discards the specified keys from the object and returns their values.

        Parameters
        ----------
        *keys : str
            One or more keys to discard and retrieve the values of.
        
        ignore_missing: bool
            Whether missing keys should be skipped. Defaults to False.
            
        Returns
        -------
        list
            Returns a list containing the values of the discarded keys.

        """
        result = list()
        
        if ignore_missing:
            for k in set(keys) & self.keys():
                result.append(self.pop(k))
        else:
            for k in keys:
                result.append(self.pop(k,None))          
        
        return result


class EnumClass(IntEnum):
    UNKNOWN = -1 
    
    @classmethod
    def _missing_(cls, value):
        obj = cls.UNKNOWN
        obj._value_ = value
        return obj