from jwt import (
    encode,
    decode
)
from datetime import (
    datetime,
    timedelta
)
from functools import wraps

def AuthEncode(user_id):
    exp = (datetime.utcnow() + timedelta(minutes=60))
    token = encode({ 'id': user_id, 'exp': exp }, 'secrect', algorithm='HS256')
    return token

def AuthDecode(method):
    @wraps(method)
    def decode_fn(*args, **kargs):
        destruct = list(args)
        try:
            token = destruct[1].encode()
            decoded = decode(token, 'secrect', algorithms=['HS256'])
            destruct[1] = decoded['id']
        except Exception as e:
            print (e)
            destruct.extend((None, True))
        return method(*tuple(destruct), **kargs)
    return decode_fn