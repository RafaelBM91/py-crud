from interface.rest.server import Server
from adapter.sql.database import DataBase

def App():
    DataBase()
    Server()

if __name__ == "__main__":
    App()
