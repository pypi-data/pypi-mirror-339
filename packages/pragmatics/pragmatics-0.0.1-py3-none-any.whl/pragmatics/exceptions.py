
"""Exceptions

Provides access to the `pragmatics` framework's error handling system.
"""


class PragmaticsError(Exception):
    """Base exception class for all errors in the `pragmatics` framework."""
    pass


class IllegalMutationError(PragmaticsError):
    """Exception raised on attempts to modify immutable data.

    This error is raised when code attempts to directly modify values
    in frozen data structures, such as the `pragmatics` framework's
    `Elements` class.
    """
    
    def __init__(self, object_type, attribute=None, message=None):
        self.object_type = object_type
        self.attribute = attribute
        
        if message is None:
            if attribute:
                self.message = f"Cannot modify '{attribute}' in immutable {object_type}. " \
                              f"Create a copy instead."
            else:
                self.message = f"Cannot modify immutable {object_type}. Create a copy instead."
        else:
            self.message = message
            
        super().__init__(self.message)
