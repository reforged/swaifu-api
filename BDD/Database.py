from abc import ABC, abstractmethod


class Database(ABC):
    """
    Classe abstraite afin d'offrir une interface commune à tous les types de systèmes de gestion de données
    Notamment base de donnée MySQL ou un système de fichier
    """
    @abstractmethod
    def query(self, request) -> list:
        pass

    @abstractmethod
    def execute(self, request) -> list:
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def lastVal(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

