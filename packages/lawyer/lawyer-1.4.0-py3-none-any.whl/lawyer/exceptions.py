
class ParameterError(Exception):

        __strerror__ = "{} for an argument or group must be of type <class 'str'>."
        __interror__ = __strerror__.replace('str', 'int')
        __boolerror__ = __strerror__.replace('str', 'bool')
        __iterablerror__ = __strerror__.replace("<class 'str'>", 'iterable[str]')
        __capturetyperror__ = "capture type of an argument must be any one of these: {}."

class ArgumentError(Exception): pass
class InstanceError(Exception): pass
class ParseError(Exception): pass
class ExistsError(Exception): pass