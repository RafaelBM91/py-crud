from graphene import (
    ObjectType,
    String,
    List,
    Field
)
from adapter.sql.database import DataBase
from functools import wraps
from adapter.gql.query.user.model import Person
from adapter.gql.query.post.model import Post
from adapter.gql.query.comment.model import Comment

def FindUserById(id):
    db     = DataBase
    result = db.user_by_id(db, id)
    return Person(result) if result != None else None

def FindCommentByPostId(id):
    db     = DataBase
    result = db.comment_by_post_id(db, id)
    return result

class Query(ObjectType):
    person_by_id  = Field(Person, id = String(required = True))
    posts_by_user = List(Post, user_id = String(required = True))

    def resolve_person_by_id(self, info, id):
        return FindUserById(id)

    def resolve_posts_by_user(self, info, user_id):
        db = DataBase
        result = db.post_by_user_id(db, user_id)
        post_list = list()
        for post in result:
            person = FindUserById(post[1])
            list_comment = list()
            try:
                comments = FindCommentByPostId(post[0])
                for comment in comments:
                    person_comment = FindUserById(comment[1])
                    list_comment.append(Comment(comment, person_comment))
                print (list_comment)
            except Exception as e:
                print (e)
            post_list.append(Post(post, person, list_comment))
        return post_list
