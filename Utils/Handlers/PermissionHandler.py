import BDD.Database as Database


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


def getPermissionById(database: Database.Database, permission_id: str):
    get_query = {
        "where": [
            ["permissions", "id", permission_id]
        ],
        "from": {
            "tables": ["permissions"]
        }
    }

    return database.query(get_query)


def getAllPermission(database: Database.Database):
    get_query = {
        "from": {
            "tables": ["permissions"]
        }
    }

    return database.query(get_query)
