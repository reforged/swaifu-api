import hashlib
import jwt

from Utils.Dotenv import getenv
from flask import Request, make_response, Response
import Erreurs.HttpErreurs as HttpErreurs

from BDD.Database import Database
from Utils.Route import route
from Utils.HandleToken import addToken
import Utils.HandleUser as HandleUser

from Permissions.Policies import middleware


# @middleware(["post:etiquette", "post:question"])
@route("POST")
def login(database: Database, request: Request) -> dict[str, str | dict[str, str]] | Response:
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if email is None or password is None:
        return make_response("Email ou Mot de Passe manquant",
                             400,
                             {'Authentication': '"Identifiants nécessaires"'}
                             )

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    del password

    query_result = HandleUser.getUserByEmail(database, email)

    if len(query_result) == 0:
        return make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    query_result = query_result[0]

    if hashed_password != query_result["password"]:
        return make_response("Nom d'utilisateur ou mot de passe incorrect",
                             401,
                             {'Authentication': '"Authentication requise"'}
                             )

    token = jwt.encode({'id': query_result["id"]}, getenv("token_key"), algorithm="HS256")

    addToken(database, token, query_result["id"])

    return_data = {'token': "Bearer " + token, 'user': {
        'id': query_result["id"],
        'email': email,
        'firstname': query_result["firstname"],
        'lastname': query_result["lastname"],
        'created_at': query_result["created_at"],
        'updated_at': query_result["updated_at"]
    }
                   }

    print(return_data)

    return return_data
