import BDD.Database as Database


# TODO: Supprimer
def getPermissionByUser(database: Database.Database, user_id: str) -> list[dict]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir les permissions d'un
    utilisateur en fonction de son id.

    :param database: Objet base de données
    :param user_id: Id de l'utilisateur concerné
    """

    get_user_permissions = {
        "select": [
            ["permissions", "key"]
        ],
        "where": [
            ["users", "id", user_id, "and"]
        ],
        "from": {
            "tables": ["users", "permission_user", "permissions"],

            "cond": [
                [
                    ["users", "id"],
                    ["permission_user", "user_id"]
                ],
                [
                    ["permission_user", "permission_id"],
                    ["permissions", "id"]
                ]
            ]
        }
    }

    return database.query(get_user_permissions)
