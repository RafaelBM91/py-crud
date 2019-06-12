# models

from marshmallow import (
    Schema,
    fields,
    ValidationError
)

class User(Schema):
    dni      = fields.Str(required=True)
    email    = fields.Str(required=True)
    name     = fields.Str(required=True)
    password = fields.Str(required=True)

# api

import json
from flask import Flask, request

class Api:
    template = None

    def __init__(self, template):
        self.template = template
        self.api = Flask(__name__)
        self.__load_routes()

    def __load_routes(self):
        
        @self.api.route('/', methods=["GET"])
        def home():
            return "Ok.!", 200

        @self.api.route('/register', methods=["POST"])
        def register():
            return self.template.register_user(request.form)

# database

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

@connection
def find_one_user(client, options):
    return client.python.users.find_one(options)

@connection
def insert_one_user(client, options):
    return client.python.users.insert_one(options)

# interface

##declare module { models }

class Interface:
    api = None
    template = {}

    def __init__(self):
        self.api = Api(self)
        self.api.api.run(port = 9090)

    def register_user(self, user = None):
        try:
            new_user = User().load(user)
            if new_user.errors.__len__() > 0:
                return ("Bad Request", 400)
            return ("Ok.!", 200)
        except ValidationError as er:
            print (er)
            return ("Bad Request", 400)

# app

class App:

    def start_app(self):
        prepare_database('python', 'users')
        print (find_one_user(None, { 'name': 'rafael' }))

        try:
            print (insert_one_user(None, { 'dni': '001577503', 'password': '123456', 'email': 'ts@ts.ts', 'name': 'rafael' }))
        except Exception as e:
            print (e)

        self.interface = Interface()

# main
if __name__ == "__main__":
    App().start_app()
