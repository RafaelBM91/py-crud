from graphene import (
    ObjectType,
    String
)

class Person(ObjectType):
    id    = String()
    name  = String()
    email = String()

    def __init__(self, values):
        if values != None:
            self.id    = values[0]
            self.name  = values[1]
            self.email = values[2]
