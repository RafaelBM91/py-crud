from graphene import (
    ObjectType,
    String,
    Field,
    List
)
from adapter.gql.query.user.model import Person
from adapter.gql.query.comment.model import Comment

class Post(ObjectType):
    id       = String()
    user     = Field(Person)
    title    = String()
    content  = String()
    data     = String()
    comment  = List(Comment)
    
    def __init__(self, post, person, comment):
        if post != None:
            self.id       = post[0]
            self.user     = person
            self.title    = post[2]
            self.content  = post[3]
            self.data     = post[4]
            self.comment  = comment
