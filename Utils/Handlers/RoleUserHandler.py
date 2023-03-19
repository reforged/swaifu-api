import BDD.Database as Database


def addRoleUser(database: Database.Database, user_id: str, role_id: str, commit: bool = True):
    # TODO: Ajout vérification existence roles
    insert_role_user = {
        "table": "role_user",
        "action": "insert",
        "valeurs": [
            ["role_id", role_id],
            ["user_id", user_id]
        ]
    }

    database.execute(insert_role_user)

    if commit:
        database.commit()
