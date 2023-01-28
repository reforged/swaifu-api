from BDD.Database import Database
import uuid
import datetime
import hashlib


def getUserByUuid(database: Database, user_uuid: str):
    check_uuid_query = {
        "where": [
            ["users", "id", user_uuid, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(check_uuid_query)


def addUser(database: Database, arguments):
    conflict = True
    user_uuid = None

    while conflict:
        if len(getUserByUuid(database, user_uuid := str(uuid.uuid4()))) == 0:
            conflict = False

    hashed_password = hashlib.sha256(arguments["password"].encode()).hexdigest()
    del arguments["password"]

    creation_utilisateur = {
        "table": "users",
        "action": "insert",
        "valeurs": [
            ["id", user_uuid],
            ["email", arguments["email"]],
            ["firstname", arguments["firstname"]],
            ["lastname", arguments["lastname"]],
            ["password", hashed_password],
            ["created_at", str(datetime.datetime.now().astimezone())],
            ["updated_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(creation_utilisateur)
    database.commit()

    return user_uuid


def getUserByEmail(database: Database, email: str):
    check_user_query = {
        "where": [
            ["users", "email", email, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(check_user_query)
