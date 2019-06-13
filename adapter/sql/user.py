from sqlite3 import connect
from functools import wraps
import uuid

def ConnectDB(method):
    @wraps(method)
    def function(*args, **kargs):
        cursor = connect('database.db')
        return method(cursor, **kargs)
    return function

@ConnectDB
def user_register(cursor, params):
    try:
        id = uuid.uuid1().__str__()
        cursor.execute('''
            INSERT INTO User
                (id, email, name, password)
            VALUES ('{}', '{}', '{}', '{}')'''.format(
                id,
                params['email'],
                params['name'],
                params['password']
            )
        )
        cursor.commit()
        return id
    except Exception as e:
        print ('[Error ~> sql.users]: ', e)
        return None
    finally:
        cursor.close()

@ConnectDB
def user_login(cursor, params):
    try:
        result = cursor.execute('''
            SELECT id FROM User WHERE email='{}' AND password='{}' LIMIT 1
        '''.format(
                params['email'],
                params['password']
            )
        ).fetchone()
        return result[0] if result != None else None
    except Exception as e:
        print ('[Error ~> sql.users]: ', e)
        return None
    finally:
        cursor.close()
