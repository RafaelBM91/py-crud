from marshmallow import (
    Schema,
    fields,
    pre_load,
    post_load,
    ValidationError
)

class User(Schema):
    email    = fields.Str(required=True)
    name     = fields.Str(required=True)
    password = fields.Str(required=True)

    @pre_load
    def make_pre(self, data):
        return data

    @post_load
    def make_post(self, data):
        return data

class Login(Schema):
    email    = fields.Str(required=True)
    password = fields.Str(required=True)

    @pre_load
    def make_pre(self, data):
        return data

    @post_load
    def make_post(self, data):
        return data
