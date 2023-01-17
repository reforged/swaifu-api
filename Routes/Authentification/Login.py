import hashlib
import datetime
import jwt

from flask import request, make_response, Response

from BDD.Database import Database
from Utils.Route import route


@route("POST", "/login")
def login(Db: Database) -> dict[str, str | dict[str, str]] | Response:
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
            ["users", "id"]
        ],
        "where": [
            ["users", "email", email]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    query_result = (Db.query(password_request))[0]

    stored_password = query_result[0]
    stored_id = query_result[1]

    if hashed_password == stored_password:
        token = jwt.encode({'user_id': stored_id}, "clé", algorithm="HS256")

        return {'token': token, 'user': {'id': stored_id}}

    return make_response("Nom d'utilisateur ou mot de passe incorrect",
                         401,
                         {'Authentification': '"Authentification requise"'}
                         )
