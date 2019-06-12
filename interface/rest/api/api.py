from core.users.model import User
from interface.rest.flask import FlaskApi
from core.users.model import User
from adapter.sql.user import register_user

from interface.secure.jwt import Authorization

class Interface:
    api = None
    template = {}

    def __init__(self):
        self.api = FlaskApi(self)
        self.api.api.run(port = 9090)

    def register_user(self, user = None):
        try:
            new_user = User().load(user)
            if new_user.errors.__len__() > 0:
                return ("Bad Request", 400)

            result = register_user(None, params = new_user.data)

            if result == None:
                return ("Error en la Data", 400)

            return ("Data Save: {}".format(result), 200)
        except Exception as e:
            print (e)
            return ("Bad Request", 400)

    @Authorization
    def profile(self, token):
        print ('****TOKEN*****', token)
        return ("ok", 200)
