from adapter.mongodb.connect import connection

@connection
def find_one_user(client, options):
    return client.python.users.find_one(options)

@connection
def insert_one_user(client, options):
    return client.python.users.insert_one(options)
