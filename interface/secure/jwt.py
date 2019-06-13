from jwt import (
    encode,
    decode
)
from datetime import (
    datetime,
    timedelta
)
from functools import wraps

def AuthDecode(method):
    @wraps(method)
    def function(*args, **kargs):
        largs = list(args)
        token = largs[1]
        try:
            result = decode(token)
        except Exception as e:
            result = None
        largs[1] = result
        nargs = tuple(largs)
        return method(*nargs, **kargs)
    return function

def AuthEncode(user_id):
    exp = (datetime.utcnow() + timedelta(seconds=60))
    result = encode({ 'id': user_id, 'exp': exp.__str__() }, 'secrect', algorithm='HS256')
    return result
