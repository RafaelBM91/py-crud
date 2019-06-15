from graphene import (
    ObjectType
)
from adapter.gql.mutation.post.create import PostCreate
from adapter.gql.mutation.comment.create import CommentCreate

class MutationC(ObjectType):
    post_create    = PostCreate.Field()
    comment_create = CommentCreate.Field()
