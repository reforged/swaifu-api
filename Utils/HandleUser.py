import datetime
import hashlib
import uuid
from flask import make_response
from Erreurs.HttpErreurs import requete_malforme


def addUser(database, password, email, firstname, lastname, commit=True):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    del password

    conflict = True
    user_uuid = None

    while conflict:
        user_uuid = str(uuid.uuid4())

        check_uuid_query = {
            "where": [
                ["users", "id", user_uuid, "and"]
            ],
            "from": {
                "tables": ["users"]
            }
        }

        if len(database.query(check_uuid_query)) == 0:
            conflict = False

    creation_utilisateur = {
        "table": "users",
        "action": "insert",
        "valeurs": [
            ["id", user_uuid],
            ["email", email],
            ["firstname", firstname],
            ["lastname", lastname],
            ["password", hashed_password],
            ["created_at", str(datetime.datetime.now().astimezone())],
            ["updated_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(creation_utilisateur)

    if commit:
        database.commit()

    return user_uuid


def addUsers(database, user_create_list):
    return_uuid = []

    for utilisateur in user_create_list:
        email = utilisateur.get("email", None)
        firstname = utilisateur.get("firstname", None)
        lastname = utilisateur.get("lastname", None)
        password = utilisateur.get("password", None)

        for data in [email, firstname, lastname, password]:
            if data is None:
                return make_response(requete_malforme, 400, requete_malforme)

        return_uuid.append(addUser(database, password, email, firstname, lastname, commit=False))

    database.commit()

    return return_uuid


def getUserByEmail(database, email):
    check_user_query = {
        "where": [
            ["users", "email", email, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(check_user_query)


def getUserByUuid(database, uuid):
    get_user_query = {
        "select": [
            ["users", "firstname"],
            ["users", "email"],
            ["users", "lastname"],
            ["users", "created_at"],
            ["users", "updated_at"]
        ],
        "where": [
            ["users", "id", uuid, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(get_user_query)
