class DahuaRequestError(Exception):
    """Exception raised for request errors."""


class DahuaMethodNotSupported(Exception):
    """Methods that a function parent does not support"""


def code_to_error(code: int):
    """
    ERROR_CODE_NOT_SET = 268959743,
    INTERFACE_NOT_FOUND = 268632064,
    METHOD_NOT_FOUND = 268894210,
    REQUEST_INVALID = 268894209,
    REQUEST_INVALID_PARAM = 268894211,
    SESSION_INVALID = 28763750,

    USER_NOT_VALID = 268632070,
    PASSWORD_NOT_VALID = 268632071,
    IN_BLACK_LIST = 268632073,
    HAS_BEEN_USED = 268632074,
    HAS_BEEN_LOCKED = 268632081,

    BUSY = 268632075,
    """
    # TODO create exceptions for each and map
