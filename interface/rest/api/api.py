import json
from functools import wraps

from core.users.model import User
from interface.rest.flask import FlaskApi
from core.users.model import (
    User,
    Login
)
from adapter.sql.user import (
    user_register,
    user_login
)
from interface.secure.jwt import (
    AuthEncode,
    AuthDecode
)
from core.log.logger import Error

class Interface:
    api = None
    template = {}

    def __init__(self):
        self.api = FlaskApi(self)
        self.api.api.run(port = 9090)

    def user_register(self, user):
        try:
            new_user = User().load(user)
            if new_user.errors.__len__() > 0:
                return self.response({}, new_user.errors, 400)
            result = user_register(None, params = new_user.data)
            if result == None:
                return self.response({}, 'Error en la Data', 400)
            return self.response({ 'id': result }, {}, 200)
        except Exception as e:
            Error('api.py', e)
            return self.response({}, 'Error en la Data', 200)

    def user_login(self, user):
        try:
            login_user = Login().load(user)
            if login_user.errors.__len__() > 0:
                return self.response({}, login_user.errors, 400)
            result = user_login(None, params = login_user.data)
            print (AuthEncode(result).decode('utf-8'))
            return self.response({
                'token': AuthEncode(result).decode('utf-8')
            }, {}, 200)
        except Exception as e:
            Error('api.py', e)
            return self.response({}, 'Error en la Data', 200)

    def response(self, data, error, code):
        return json.dumps({
            'data' : data,
            'error': error
        }), code
