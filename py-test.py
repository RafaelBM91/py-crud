import json
from functools import wraps
from marshmallow import (
    Schema,
    fields,
    ValidationError
)
from flask import (
    Flask,
    request
)
from sqlite3 import connect
import uuid

class User(Schema):
    email     = fields.Str(required=True)
    name      = fields.Str(required=True)
    password  = fields.Str(required=True)

class UserLogin(Schema):
    email     = fields.Str(required=True)
    password  = fields.Str(required=True)

def ParseModel(Model):
    def decorator(method):
        @wraps(method)
        def parser(*args, **kargs):
            destruct = list(args)
            destruct[1] = Model().load(destruct[1])
            return method(*tuple(destruct), **kargs)
        return parser
    return decorator

def ConnectionDB(method):
    @wraps(method)
    def conn(*args, **kargs):
        destruct = list(args)
        destruct.append(connect('database.db'))
        return method(*tuple(destruct), **kargs)
    return conn

class DataBase:

    @ConnectionDB
    def __init__(self, cursor = None):
        cursor.execute('''CREATE TABLE IF NOT EXISTS User (
            id text  PRIMARY KEY,
            email text NOT NULL UNIQUE,
            name text NOT NULL,
            password text NOT NULL
        )''')
        cursor.commit()
        cursor.close()

    @ConnectionDB
    def user_register(self, values, cursor = None):
        if values.errors != {}:
            raise Exception(values.errors)
        try:
            id = uuid.uuid1().__str__()
            cursor.execute('''
                INSERT INTO User
                    (id, email, name, password)
                VALUES ('{}', '{}', '{}', '{}')'''.format(
                    id,
                    values.data['email'],
                    values.data['name'],
                    values.data['password']
                )
            )
            cursor.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return ({'id': id})

    @ConnectionDB
    def user_login(self, values, cursor = None):
        if values.errors != {}:
            raise Exception(values.errors)
        try:
            result = cursor.execute('''SELECT id FROM User 
                WHERE email='{}' AND password='{}' LIMIT 1
            '''.format(
                    values.data['email'],
                    values.data['password']
                )
            ).fetchone()
            result = result[0] if result != None else None
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result

def Operations(method):
    @wraps(method)
    def fn(*args, **kargs):
        destruct = list(args)
        fnCall = None
        fnCall = getattr(DataBase, method.__name__)
        try:
            destruct.append(
                fnCall(None, destruct[1])
            )
        except Exception as e:
            destruct.extend((e.__str__(), True))
        return method(*tuple(destruct), **kargs)
    return fn

class Mutation:
    
    @ParseModel(User)
    @Operations
    def user_register(self, values, result = None, errors = False):
        if errors:
            return self.format({}, '[Error]', result, 400)
        else:
            return self.format(result, '[Ok]', '', 200)

    @ParseModel(UserLogin)
    @Operations
    def user_login(self, values, result = None, errors = False):
        if result == None:
            return self.format({}, '[Access Denied]', {}, 401)
        else: 
            if errors:
                return self.format({}, '[Error]', result, 401)
            else:
                
                return self.format({'id': result}, '[Ok]', '', 200)

    def format(self, data, msg, error, code):
        return json.dumps({
            'data' : data,
            'msg'  : msg,
            'error': error
        }), code

def FlastApi():
    app = Flask(__name__)
    mutation = Mutation()
    
    @app.route('/user/register', methods=['POST'])
    def user_register():
        return mutation.user_register(request.form)

    @app.route('/user/login', methods=['POST'])
    def user_login():
        return mutation.user_login(request.form)

    app.run(port=1212)

def main():
    DataBase()
    FlastApi()

if __name__ == '__main__':
    main()
