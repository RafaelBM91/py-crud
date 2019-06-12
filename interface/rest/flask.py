import json
from flask import Flask, request

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

        @self.api.route('/register', methods=["POST"])
        def register():
            return self.template.register_user(request.form)

        @self.api.route('/profile', methods=["POST"])
        def profile():
            try:
                # result = self.template.profile("request.headers['Authorization']")
                print (self.template.profile('hola'))
                return ("bad", 401)
            except Exception as e:
                print (e)
                return ("Error", 401)
