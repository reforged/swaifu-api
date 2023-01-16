import BDD.Database as Database
from sql import SQL


class SqlDatabase(Database):
    sql_connection = None

    def __init__(self, url, user, password):
        pass

    def query(self, request):
        pass

    def execute(self, request):
        pass
