import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler


def etiquettes(database: Database.Database) -> list[dict]:
    """
    Gère la route .../etiquettes - Méthode GET

    Permet à un utilisateur d'obtenir toutes les étiquettes.

    :param database: Objet base de données
    :return:
    """

    return EtiquetteHandler.getAllEtiquettes(database)
