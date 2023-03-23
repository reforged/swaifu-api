import BDD.Model as Model

import Permissions.Policies as Policies


@Policies.middleware(["store:user"], ["update:user"], ["destroy:user"])
def getAllUsers(query_builder: Model.Model):
    """
    Gère la route .../users - Méthode GET

    Permet à un utilisateur de récupérer toutes les permissions.

    :param query_builder: Objet Model
    """

    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname",
                   "users.created_at", "users.updated_at"]

    # Pour chaque utilisateur, on charge leur role et on ne charge pas le ...
    res = query_builder.table("users").select(*info_wanted).load("roles")

    # Ainsi que chaque permission individuelle, non associé à un rôle
    for row in res:
        row.load("permissions")

    return [row.export() for row in res]
