
"""Collections

Custom data structures used throughout the `pragmatics` framework.
"""

# Import statements
import functools

from .exceptions import IllegalMutationError


# Helper functions
def crystallize(data: dict) -> "ImmutableDict":
    """Converts a regular `dict` object to an `ImmutableDict`."""
    if isinstance(data, dict):
        return ImmutableDict((k, crystallize(v)) for k, v in data.items())
    elif isinstance(data, list):
        return tuple(crystallize(item) for item in data)
    else:
        return data


def crystalline(init_func):
    """Decorator for `post_init` to make all dictionaries immutable."""
    @functools.wraps(init_func)
    def wrapper(self, *args, **kwargs):
        init_func(self, *args, **kwargs)
        
        for name, value in self.__dict__.items():
            if isinstance(value, dict):
                object.__setattr__(self, name, crystallize(value))
    return wrapper


class ImmutableDict(dict):
    """A dictionary class that cannot be mutated after instantiation.
    
    This class overrides the mutative methods of `dict` to raise
    `IllegalMutationError` on attempts to modify its constituent data.
    """
    def __setitem__(self, key, value):
        raise IllegalMutationError("element dictionary", key)
    
    def __delitem__(self, key):
        raise IllegalMutationError("element dictionary", key)
    
    def update(self, *args, **kwargs):
        raise IllegalMutationError("element dictionary", "update()")
    
    def pop(self, *args, **kwargs):
        raise IllegalMutationError("element dictionary", "pop()")
    
    def popitem(self):
        raise IllegalMutationError("element dictionary", "popitem()")
    
    def clear(self):
        raise IllegalMutationError("element dictionary", "clear()")
    
    def setdefault(self, *args, **kwargs):
        raise IllegalMutationError("element dictionary", "setdefault()")

