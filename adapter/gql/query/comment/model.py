from graphene import (
    ObjectType,
    String,
    Field
)
from adapter.gql.query.user.model import Person

class Comment(ObjectType):
    id       = String()
    user     = Field(Person)
    content  = String()
    data     = String()

    def __init__(self, comment, person):
        if comment != None:
            self.id       = comment[0]
            self.user     = person
            self.content  = comment[3]
            self.data     = comment[4]
