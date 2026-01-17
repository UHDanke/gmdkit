# Imports
from contextvars import ContextVar
from contextlib import contextmanager


float_precision = ContextVar("float_precision", default=None) 
string_fallback = ContextVar("string_fallback", default=True)
discard_default = ContextVar("discard_default", default=False)


@contextmanager
def casting_options(
        float_precision:int=None,
        string_fallback:bool=False,
        discard_default:bool=False
        ):
    tokens = []
    tokens.append(float_precision.set(float_precision))
    tokens.append(string_fallback.set(string_fallback))
    tokens.append(discard_default.set(discard_default))
    
    try:
        yield
    finally:
        for var, token in tokens.items():
            var.reset(token)