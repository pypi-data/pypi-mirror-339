#!/usr/bin/env python3


class ResFinderError(Exception):
    """ Root for all module exceptions in the resfinder application.
        Only used to enable "except" of all exceptions from resfinder.
        Never raised.
    """
    pass


class DatabaseError(ResFinderError):
    """ Raise when adding the same key to a dict twice."""
    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(DatabaseError, self).__init__(message, *args)


class DuplicateKeyError(ResFinderError):
    """ Raise when adding the same key to a dict twice."""
    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(DuplicateKeyError, self).__init__(message, *args)


class LockedObjectError(ResFinderError):
    """ Raise when attempting to alter a locked object."""
    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(LockedObjectError, self).__init__(message, *args)
