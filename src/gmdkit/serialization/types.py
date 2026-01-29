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
        if not conditions:
            return self.__class__()
        
        if len(conditions) == 1 and not kwargs:
            condition = conditions[0]
            return self.__class__(item for item in self if condition(item))
        
        funcs = filter_kwargs(*conditions, **kwargs) if kwargs else conditions
        
        return self.__class__(
            item for item in self 
            if any(condition(item) for condition in funcs)
        )
    
    
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
        if not functions:
            return self
        
        if len(functions) == 1 and not kwargs:
            func = functions[0]
            for i in range(len(self)):
                new = func(self[i])
                if new is not None:
                    self[i] = new
            return self
        
        funcs = filter_kwargs(*functions, **kwargs) if kwargs else functions
        
        for i in range(len(self)):
            val = self[i]
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
        if not conditions:
            return self.__class__()
        
        excluded = self.__class__()
        kept = []
        
        funcs = filter_kwargs(*conditions, **kwargs) if kwargs else conditions
        
        excluded_append = excluded.append
        kept_append = kept.append
        
        for item in self:
            if any(condition(item) for condition in funcs):
                excluded_append(item)
            else:
                kept_append(item)
        
        self[:] = kept
        return excluded

    
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
        if not functions:
            return []
        
        if len(functions) == 1 and not kwargs:
            func = functions[0]
            result = []
            extend = result.extend
            for item in self:
                vals = func(item)
                if vals:
                    extend(vals)
            return result
        
        funcs = filter_kwargs(*functions, **kwargs) if kwargs else functions
        
        result = []
        extend = result.extend
        
        for item in self:
            for function in funcs:
                vals = function(item)
                if vals:
                    extend(vals)
                
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
        if not functions:
            return set()
        
        result = set()
        
        funcs = filter_kwargs(*functions, **kwargs) if kwargs else functions
        
        update = result.update
        
        for item in self:
            for function in funcs:
                vals = function(item)
                if vals:
                    update(vals)
                
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
        if not functions or not self:
            return set()
        
        funcs = filter_kwargs(*functions, **kwargs) if kwargs else functions
        
        result = None
        
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
        
        return result if result is not None else set()

        
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
        if len(keys) == 1:
            key = keys[0]
            if ignore_missing and key not in self:
                return []
            return [self.get(key)]
        
        if ignore_missing:
            if len(keys) > 3:
                valid_keys = set(keys) & self.keys()
                return [self[k] for k in keys if k in valid_keys]
            else:
                return [self[k] for k in keys if k in self]
        else:
            return [self.get(k) for k in keys]


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
        if not keys:
            return []
        
        if len(keys) == 1:
            key = keys[0]
            if ignore_missing:
                return [self.pop(key)] if key in self else []
            return [self.pop(key, None)]
        
        if ignore_missing:
            if len(keys) > 3:
                valid_keys = set(keys) & self.keys()
                return [self.pop(k) for k in keys if k in valid_keys]
            else:
                return [self.pop(k) for k in keys if k in self]
        else:
            return [self.pop(k, None) for k in keys]


class EnumClass(IntEnum):
    
    @classmethod
    def _missing_(cls, value):
        return int(value)