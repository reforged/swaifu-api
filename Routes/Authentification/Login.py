import hashlib
import datetime
import jwt

from Utils.Dotenv import getenv
from flask import Request, make_response, Response

from BDD.Database import Database
from Utils.Route import route

from Permissions.Policies import middleware


# @middleware(["post:etiquette", "post:question"])
@route("POST", "/login")
def login(database: Database, request: Request) -> dict[str, str | dict[str, str]] | Response:
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if email is None or password is None:
        return make_response("Email ou Mot de Passe manquant",
                             400,
                             {'Authentification': '"Identifiants nécessaires"'}
                             )

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    del password

    password_request = {
        "select": [
            ["users", "password"],
            ["users", "id"],
            ["users", "name"]
        ],
        "where": [
            ["users", "email", email]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    query_result = (database.query(password_request))[0]

    if hashed_password == query_result["password"]:
        token = jwt.encode({'id': query_result["id"]}, getenv("token_key"), algorithm="HS256")

        insert = {
            "table": "api_tokens",
            "action": "insert",
            "valeurs": [
                ["token", token],
                ["user_id", query_result["id"]]
            ]
        }

        database.execute(insert)
        print(database.commit())

        return {'token': token, 'user': {
                        'id': query_result["id"],
                        'email': email,
                        'name': query_result["name"]
                    }
                }

    return make_response("Nom d'utilisateur ou mot de passe incorrect",
                         401,
                         {'Authentification': '"Authentification requise"'}
                         )
