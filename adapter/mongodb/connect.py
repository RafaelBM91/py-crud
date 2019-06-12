from functools import wraps

from pymongo import (
    MongoClient,
    TEXT
)

def prepare_database(database, collection):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database]
    try:
        collection = db.create_collection(collection)
        collection.create_index([('dni', TEXT)], unique = True)
    except Exception as ex:
        print (ex)

def connection(method):
    @wraps(method)
    def wrap_method(*args, **kwargs):
        client = MongoClient('mongodb://localhost:27017/')
        aux_args = list(args)
        aux_args[0] = client
        new_args = tuple(aux_args)
        return method(*new_args, **kwargs)
    return wrap_method
