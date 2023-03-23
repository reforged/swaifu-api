import BDD.Model as Model

import Permissions.Policies as Policies


@Policies.middleware(["store:permission"], ["update:permission"], ["destroy:permissions"])
def getAllPermissions(query_builder: Model.Model):
    """
    Gère la route .../permissions - Méthode GET

    Permet à un utilisateur de récupérer toutes les permissions.

    :param query_builder: Objet Model
    """

    res = query_builder.table("permissions").load("roles", query_builder.select("roles.id"))

    # On souhaite charger les roles et utilisateurs possédant chaque permissions,
    # Puisque seul l'id est nécessaire et par souci de pratique, seul l'id est demandé
    for row in res:
        row.load("users", query_builder.select("users.id"))

    return [row.export() for row in res]
