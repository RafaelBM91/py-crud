from jwt import (
    encode,
    decode
)
from functools import wraps

def Authorization(method):
    @wraps(method)
    def function(*args, **kargs):
        print ('args')
    return function
