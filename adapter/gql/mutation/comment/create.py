from graphene import (
    ObjectType,
    InputObjectType,
    String,
    Mutation
)
from adapter.sql.database import DataBase

class CommentInput(InputObjectType):
    user_id = String(required = True)
    post_id = String(required = True)
    content = String(required = True)
    data    = String(required = True)

class CommentCreateResponse(ObjectType):
    id = String()

class CommentCreate(Mutation):
    class Arguments:
        comment = CommentInput(required = True)
    Output = CommentCreateResponse
    def mutate(self, info, comment):
        db = DataBase
        try:
            id = db.comment_creste(DataBase, comment)
        except Exception as e:
            print (e)
            return None
        return CommentCreateResponse(id)
