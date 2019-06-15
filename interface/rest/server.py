from flask import (
    Flask,
    request
)
from flask_graphql import GraphQLView
from interface.rest.api import Api
from adapter.gql.schema import schema

def Server():
    app = Flask(__name__)
    api = Api()
    
    @app.route('/user/register', methods=['POST'])
    def user_register():
        return api.user_register(request.form)

    @app.route('/user/login', methods=['POST'])
    def user_login():
        return api.user_login(request.form)

    @app.route('/user/profile', methods=['POST'])
    def user_profile():
        return api.user_profile(request.headers.get('Authorization'))

    app.add_url_rule(
        '/graphql',
        view_func = GraphQLView.as_view(
            'graphql',
            schema = schema,
            graphiql = True,
            batch = True #for apollo and relay
        )
    )

    app.run(port=1212)
