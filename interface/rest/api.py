import json
from core.parser import ParseModel
from core.models import (
    User,
    UserLogin
)
from interface.helpers.dispath import Dispath
from adapter.auth.authorization import AuthDecode

class Api:
    @ParseModel(User)
    @Dispath
    def user_register(self, values, result = None, errors = False):
        if errors:
            return self.format({}, '[Error]', result, 400)
        else:
            return self.format(result, '[Ok]', '', 200)

    @ParseModel(UserLogin)
    @Dispath
    def user_login(self, values, result = None, errors = False):
        if result == None:
            return self.format({}, '[Access Denied]', {}, 401)
        else: 
            if errors:
                return self.format({}, '[Error]', result, 401)
            else:
                
                return self.format({'token': result}, '[Ok]', '', 200)

    @AuthDecode
    @Dispath
    def user_profile(self, values, result = None, errors = False):
        if errors:
            return self.format({}, '[Unauthorized]', '', 401)
        return self.format({
            'name' : result[1],
            'email': result[2]
        }, '[Ok]', '', 200)

    def format(self, data, msg, error, code):
        return json.dumps({
            'data' : data,
            'msg'  : msg,
            'error': error
        }), code
