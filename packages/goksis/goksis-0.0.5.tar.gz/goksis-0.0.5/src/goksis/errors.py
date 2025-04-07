class BaseGooksisException(Exception):
    """Base class for exceptions that require logging."""


class Identity(BaseGooksisException):
    """Raises the same error as the parent"""


class NotFound(BaseGooksisException):
    """raised when a device not found"""


class CancelSelect(BaseGooksisException):
    """Raised when selection canceled"""


class DeviceNotConnected(BaseGooksisException):
    """Raised when device is not connected"""


class NotAvailable(BaseGooksisException):
    """Raised when an unavailable feature requested"""


class AlreadyIs(BaseGooksisException):
    """Raised when an action is already done"""


class WrongSelect(BaseGooksisException):
    """Raised when wrong string is provided"""
