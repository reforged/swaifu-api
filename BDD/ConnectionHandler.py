from BDD.Database import Database
from BDD.BDD_PSQL.PsqlDatabase import PsqlDatabase

handlers = {"fichier": None, "psql": PsqlDatabase}


def initiate(systeme: str, params: dict[str, str]) -> Database:
    if systeme.lower() not in handlers.keys():
        return
        # Raise Error

    return handlers.get(systeme.lower())(params["database"], params["url"], params["user"], params["password"], params["port"])
