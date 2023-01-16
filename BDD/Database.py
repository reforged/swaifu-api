from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def query(self, request):
        pass

    @abstractmethod
    def execute(self, request):
        pass
