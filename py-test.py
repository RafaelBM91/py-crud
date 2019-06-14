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
from jwt import (
    encode,
    decode
)
from datetime import (
    datetime,
    timedelta
)

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
        print (self)
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
            result = AuthEncode(result[0]).decode("utf-8")  if result != None else None
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result

    def user_profile(self, user_id):
        print ()
 
        # print ('shi', user_id)

        # try:
        #     self.user_login(user_id)
        # except Exception as e:
        #     print (self)

        return None

    # @ConnectionDB
    def user_by_id(self, values, cursor = None):
        print ('jijiji', values)
        # try:
        #     result = cursor.execute('''SELECT name, email FROM User 
        #             WHERE id='{}' LIMIT 1
        #         '''.format(
        #             values
        #         )
        #     ).fetchone()
        #     print (result)
        #     result = None
        # # AuthEncode(result[0]).decode("utf-8")  if result != None else None
        # except Exception as e:
        #     raise Exception(e)
        # finally:
        # cursor.close()
        return None

def Operations(method):
    @wraps(method)
    def fn(*args, **kargs):
        destruct = list(args)
        fnCall = None
        fnCall = getattr(DataBase, method.__name__)
        if destruct.__len__() == 2:
            destruct.extend((None, False))
        if destruct.__len__() == 3:
            destruct.append(False)
        try:
            if destruct[3] == False:
                destruct[2] = fnCall(None, destruct[1])
            else:
                raise Exception()
        except Exception as e:
            destruct[2] = e.__str__()
            destruct[3] = True
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
                
                return self.format({'token': result}, '[Ok]', '', 200)

    @AuthDecode
    @Operations
    def user_profile(self, values, result = None, errors = False):
        if errors:
            return self.format({}, '[Unauthorized]', '', 401)
        
        # print (result, errors)
        return self.format({}, '[Ok]', '', 200)

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

    @app.route('/user/profile', methods=['POST'])
    def user_profile():
        return mutation.user_profile(request.headers.get('Authorization'))

    app.run(port=1212)

def main():
    DataBase()
    FlastApi()

if __name__ == '__main__':
    main()
