from adapter.sql.connector import ConnectionDB
from adapter.auth.authorization import AuthEncode
from interface.helpers.hash import crypt
import uuid

class DataBase:
    @ConnectionDB
    def __init__(self, cursor = None):
        cursor.execute('''CREATE TABLE IF NOT EXISTS User (
            id text  PRIMARY KEY,
            email text NOT NULL UNIQUE,
            name text NOT NULL,
            password text NOT NULL
        )''')
        cursor.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Post (
            id text  PRIMARY KEY,
            user_id text NOT NULL,
            title text NOT NULL,
            content text NOT NULL,
            data text NOT NULL
        )''')
        cursor.commit()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Comment (
            id text  PRIMARY KEY,
            user_id text NOT NULL,
            post_id text NOT NULL,
            content text NOT NULL,
            data text NOT NULL
        )''')
        cursor.commit()   
        cursor.close()

    @ConnectionDB
    def user_register(self, values, cursor = None):
        if values.errors != {}:
            raise Exception(values.errors)
        try:
            id = uuid.uuid1().__str__()
            cursor.execute('''
                INSERT INTO User
                    (id, email, name, password)
                VALUES ('{}', '{}', '{}', '{}')'''.format(
                    id,
                    values.data['email'],
                    values.data['name'],
                    crypt(values.data['password'])
                )
            )
            cursor.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return ({'id': id})

    @ConnectionDB
    def user_login(self, values, cursor = None):
        if values.errors != {}:
            raise Exception(values.errors)
        try:
            result = cursor.execute('''SELECT id FROM User 
                WHERE email='{}' AND password='{}' LIMIT 1
            '''.format(
                    values.data['email'],
                    crypt(values.data['password'])
                )
            ).fetchone()
            result = AuthEncode(result[0]).decode("utf-8")  if result != None else None
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result

    def user_profile(self, user_id):
        return self.user_by_id(self, user_id)

    @ConnectionDB
    def user_by_id(self, values, cursor = None):
        try:
            result = cursor.execute('''
                SELECT id, name, email FROM User WHERE id='{}' LIMIT 1
            '''.format(values)
            ).fetchone()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result

    @ConnectionDB
    def post_creste(self, values, cursor = None):
        id = uuid.uuid1().__str__()
        try:
            cursor.execute('''
                INSERT INTO Post
                    (id, user_id, title, content, data)
                VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(
                    id,
                    values['user_id'],
                    values['title'],
                    values['content'],
                    values['data']
                )
            )
            cursor.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return id

    @ConnectionDB
    def post_by_user_id(self, values, cursor = None):
        try:
            result = cursor.execute('''
                SELECT * FROM Post WHERE user_id = '{}'
            '''.format(
                values
            )).fetchall()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result

    @ConnectionDB
    def comment_creste(self, values, cursor = None):
        id = uuid.uuid1().__str__()
        try:
            cursor.execute('''
                INSERT INTO Comment
                    (id, user_id, post_id, content, data)
                VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(
                    id,
                    values['user_id'],
                    values['post_id'],
                    values['content'],
                    values['data']
                )
            )
            cursor.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return id

    @ConnectionDB
    def comment_by_post_id(self, values, cursor = None):
        try:
            result = cursor.execute('''
                SELECT * FROM Comment WHERE post_id = '{}'
            '''.format(
                values
            )).fetchall()
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
        return result


