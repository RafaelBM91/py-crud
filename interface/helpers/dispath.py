from functools import wraps
from adapter.sql.database import DataBase

def Dispath(method):
    @wraps(method)
    def fn(*args, **kargs):
        destruct = list(args)
        classdb = DataBase
        fnCall = getattr(classdb, method.__name__)
        if destruct.__len__() == 2:
            destruct.extend((None, False))
        if destruct.__len__() == 3:
            destruct.append(False)
        try:
            if destruct[3] == False:
                destruct[2] = fnCall(classdb, destruct[1])
            else:
                raise Exception()
        except Exception as e:
            destruct[2] = e.__str__()
            destruct[3] = True
        return method(*tuple(destruct), **kargs)
    return fn
