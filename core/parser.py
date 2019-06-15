from functools import wraps

def ParseModel(Model):
    def decorator(method):
        @wraps(method)
        def parser(*args, **kargs):
            destruct = list(args)
            destruct[1] = Model().load(destruct[1])
            return method(*tuple(destruct), **kargs)
        return parser
    return decorator
