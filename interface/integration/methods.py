from functools import wraps
from interface.secure.jwt import AuthDecode

def ProfileDec(method):
    @wraps(method)
    def function(*args, **kargs):
        print (args)
        return method(*args, **kargs)
    return function
