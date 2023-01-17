import BDD.Database as Database
import BDD.BDD_SQL.SqlParsers as SqlParsers
import mysql.connector as connector


class SqlDatabase(Database):
    """
    Classe SqlDatabase héritant de Database et implémentant ses fonctions abstraites
    Offre query et execute comme interfaces communes et disponibles
    """
    sql_connection = None
    sql_cursor = None

    def __init__(self, url: str, user: str, password: str) -> None:
        """
        Initialise la connection à une base de données MySQL en fonction des paramètres fournis
        :param url:
        :param user:
        :param password:
        """
        sql_connection = connector.connect(host=url, user=user, password=password)
        sql_cursor = sql_connection.cursor()

    def __del__(self) -> None:
        """
        Ferme la connection à la base de données lors de la destruction de la classe (Fin du programme)
        :return:
        """
        del self.sql_cursor
        self.sql_connection.close()
        del self.sql_connection

    def query(self, request: str) -> list:
        sql_request = SqlParsers.jsonToSql(request)
        return self.sql_cursor.execute(sql_request)

    def execute(self, request: str) -> list:
        # TODO: Ajout de vérification au préalable
        sql_request = SqlParsers.jsonToSql(request)
        return self.sql_cursor.execute(sql_request)
