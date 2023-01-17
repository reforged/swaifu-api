import psycopg2

from BDD.Database import Database
import BDD.BDD_PSQL.PsqlParsers as PsqlParsers

from Utils.Types import sql_json_format


class PsqlDatabase(Database):
    """
    Classe SqlDatabase héritant de Database et implémentant ses fonctions abstraites
    Offre query et execute comme interfaces communes et disponibles
    """
    sql_connection = None
    sql_cursor = None

    def __init__(self, database: str, url: str, user: str, password: str, port: str) -> None:
        """
        Initialise la connection à une base de données MySQL en fonction des paramètres fournis
        :param url:
        :param user:
        :param password:
        """
        self.sql_connection = psycopg2.connect(database=database, host=url, user=user, password=password, port=port)
        self.sql_cursor = self.sql_connection.cursor()

    def __del__(self) -> None:
        """
        Ferme la connection à la base de données lors de la destruction de la classe (Fin du programme)
        :return:
        """
        pass
        # del self.sql_cursor
        # self.sql_connection.close()
        # del self.sql_connection

    def su(self, query):
        self.sql_cursor.execute(query)
        return self.sql_cursor.fetchall()

    def query(self, request: sql_json_format) -> list:
        sql_request = PsqlParsers.jsonToPsqlQuery(request)
        self.sql_cursor.execute(sql_request)
        return self.sql_cursor.fetchall()

    def execute(self, request: sql_json_format) -> list:
        # TODO: Ajout de vérification au préalable
        sql_request = PsqlParsers.jsonToPsqlQuery(request)
        return self.sql_cursor.execute(sql_request)
