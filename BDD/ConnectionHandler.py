from BDD.Database import Database

from BDD.BDD_PSQL.PsqlDatabase import PsqlDatabase

from Utils.Erreurs.BDD import BDDNonPriseEnCharge

handlers = {"psql": PsqlDatabase}


def initiate(systeme: str) -> Database:
    """
    Initialise la classe enfant de Database en fonction du type de base de donnée demandée et renvoie l'objet gérant
    La connection
    :param systeme: Type de la base de donnée
    :return:
    """
    if systeme.lower() not in handlers.keys():
        raise BDDNonPriseEnCharge

    return handlers.get(systeme.lower())()
