import json
from flask import Flask, request
from functools import wraps

from core.log.logger import Error
from interface.integration.methods import ProfileDec

class FlaskApi:
    template = None

    def __init__(self, template):
        self.template = template
        self.api = Flask(__name__)
        self.__load_routes()

    def __load_routes(self):
        
        @self.api.route('/', methods=["GET"])
        def home():
            return "Ok.!", 200

        @self.api.route('/user/register', methods=["POST"])
        def user_register():
            return self.template.user_register(request.form)

        @self.api.route('/user/login', methods=["POST"])
        def user_login():
            return self.template.user_login(request.form)
        

