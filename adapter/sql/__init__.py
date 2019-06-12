from sqlite3 import connect

cursor = connect('database.db')

cursor.execute(''' CREATE TABLE IF NOT EXISTS User (
    id text  PRIMARY KEY,
    email text NOT NULL UNIQUE,
    name text NOT NULL,
    password text NOT NULL
) ''')

cursor.commit()

cursor.close()
