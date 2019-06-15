from sqlite3 import connect
from functools import wraps

def ConnectionDB(method):
    @wraps(method)
    def conn(*args, **kargs):
        destruct = list(args)
        destruct.append(connect('database.db'))
        return method(*tuple(destruct), **kargs)
    return conn
