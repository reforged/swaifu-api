from BDD.Database import Database
from BDD.BDD_PSQL.PsqlDatabase import PsqlDatabase
from Erreurs.BDD import BDDNonPriseEnCharge

handlers = {"fichier": None, "psql": PsqlDatabase}


def initiate(systeme: str, params: dict[str, str]) -> Database:
    if systeme.lower() not in handlers.keys():
        raise BDDNonPriseEnCharge

    return handlers.get(systeme.lower())(params["database"], params["url"], params["user"], params["password"], params["port"])
