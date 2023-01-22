import jwt
from Utils.Dotenv import getenv
from BDD.Database import Database
from flask import Request, make_response
from Erreurs.HttpErreurs import requete_malforme, creation_impossible
import uuid
import hashlib
from Utils.Route import route
import datetime
from Permissions.Policies import middleware


# @middleware(["post:user"])
@route(method="post")
def register(database: Database, request: Request):
    data = request.get_json()

    firstname = data.get("firstname", None)
    lastname = data.get("lastname", None)
    email = data.get("email", None)
    password = data.get("password", None)

    if firstname is None or lastname is None or email is None or password is None:
        return make_response(requete_malforme, 400, requete_malforme)

    check_user_query = {
        "where": [
            ["users", "email", email, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    if len(database.query(check_user_query)) != 0:
        return make_response(creation_impossible, 409, creation_impossible)

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

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    del password

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
    database.commit()

    token = jwt.encode({'id': user_uuid}, getenv("token_key"), algorithm="HS256")

    insert = {
        "table": "api_tokens",
        "action": "insert",
        "valeurs": [
            ["token", token],
            ["user_id", user_uuid],
            ["expires_at", str((datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone())],
            ["created_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(insert)
    print(database.commit())

    return {'token':  "Bearer " + token, 'user': {
        'id': user_uuid,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'created_at': str(datetime.datetime.now().astimezone()),
        'updated_at': str(datetime.datetime.now().astimezone())
    }
            }
