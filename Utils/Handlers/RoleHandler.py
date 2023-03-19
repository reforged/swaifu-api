import datetime
import uuid

import BDD.Database as Database


def getRoleById(database: Database.Database, role_id: str):
    get_query = {
        "where": [
          ["roles", "id", role_id]
        ],
        "from": {
            "tables": ["roles"]
        }
    }

    return database.query(get_query)


def getAllRoles(database: Database.Database):
    get_query = {
        "from": {
            "tables": ["roles"]
        }
    }

    return database.query(get_query)


def createRole(database: Database.Database, label: str, power: str, commit: bool = True):
    role_id: str = str(uuid.uuid4())

    while len(getRoleById(database, role_id)) > 0:
        role_id = str(uuid.uuid4())

    insert_query = {
        "table": "roles",
        "action": "insert",
        "valeurs": [
            ["id", role_id],
            ["label", label],
            ["power", power],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_query)
    if commit:
        database.commit()

    return role_id
