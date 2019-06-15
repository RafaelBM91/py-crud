from marshmallow import (
    Schema,
    fields
)

class User(Schema):
    email     = fields.Str(required=True)
    name      = fields.Str(required=True)
    password  = fields.Str(required=True)

class UserLogin(Schema):
    email     = fields.Str(required=True)
    password  = fields.Str(required=True)
