from graphene import (
    ObjectType,
    InputObjectType,
    String,
    Mutation
)
from adapter.sql.database import DataBase

class PostInput(InputObjectType):
    user_id = String(required = True)
    title   = String(required = True)
    content = String(required = True)
    data    = String(required = True)

class PostCreateResponse(ObjectType):
    id = String()

class PostCreate(Mutation):
    class Arguments:
        post = PostInput(required = True)
    Output = PostCreateResponse
    def mutate(self, info, post):
        db = DataBase
        try:
            id = db.post_creste(DataBase, post)
        except Exception as e:
            print (e)
            return None
        return PostCreateResponse(id)