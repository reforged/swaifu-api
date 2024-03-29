import BDD.Model as Model

from Permissions.Policies import middleware


@middleware(["store:etiquette"], ["update:etiquette"], ["destroy:etiquette"])
def etiquettes(query_builder: Model.Model) -> list[dict]:
    """
    Gère la route /etiquettes - Méthode GET

    Permet à un utilisateur d'obtenir toutes les étiquettes.

    :param query_builder: Objet Model
    """

    res = query_builder.table("etiquettes").load("questions")
    return [row.export() for row in res]
