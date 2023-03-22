import BDD.Model as Model


def etiquettes(query_builder: Model.Model) -> list[dict]:
    """
    Gère la route /etiquettes - Méthode GET

    Permet à un utilisateur d'obtenir toutes les étiquettes.

    :param query_builder: Objet Model
    """

    return query_builder.table("etiquettes").execute()
