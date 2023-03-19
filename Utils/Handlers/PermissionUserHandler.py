import BDD.Database as Database


def addPermissionUser(database: Database.Database, permission_id: str, user_id: str, commit: bool = True):
    insert_permission_user = {
        "table": "permission_user",
        "action": "insert",
        "valeurs": [
            ["permission_id", permission_id],
            ["user_id", user_id]
        ]
    }

    database.execute(insert_permission_user)

    if commit:
        database.commit()
