from abc import ABC, abstractmethod
from Utils.Types import sql_json_format


class Database(ABC):
    """
    Classe abstraite afin d'offrir une interface commune à tous les types de systèmes de gestion de données
    Notamment base de donnée MySQL ou un système de fichier
    """
    @abstractmethod
    def query(self, request: sql_json_format) -> list:
        pass

    @abstractmethod
    def execute(self, request: sql_json_format) -> list:
        pass

    @abstractmethod
    def su(self, query):
        pass
