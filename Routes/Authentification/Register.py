import jwt
from Utils.Dotenv import getenv
from BDD.Database import Database
from flask import Request, make_response
from Erreurs.HttpErreurs import requete_malforme, creation_impossible
import uuid
import hashlib
from Utils.Route import route
from Permissions.Policies import middleware


@route(method="post")
@middleware(["post:user"])
def register(database: Database, request: Request):
    data = request.get_json()

    name = data.get("name", None)
    email = data.get("email", None)
    password = data.get("password", None)

    if name is None or email is None or password is None:
        return make_response(requete_malforme, 400, requete_malforme)

    check_user_query = {
        "where": [
            ["users", "email", email]
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
                ["users", "id", user_uuid]
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
            ["name", name],
            ["password", hashed_password]
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
            ["user_id", user_uuid]
        ]
    }

    database.execute(insert)
    print(database.commit())

    return {'token': token, 'user': {
        'id': user_uuid,
        'email': email,
        'name': name
    }
            }
