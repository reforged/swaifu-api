import flask
import hashlib

import Erreurs.HttpErreurs as HttpErreurs

import BDD.Database as Database

import Utils.PasswordHandler as PasswordHandler
import Utils.Route as Route
import Utils.TokenHandler as TokenHandler
import Utils.Types as Types

# from Permissions.Policies import middleware


# @middleware(["post:etiquette", "post:question"])
@Route.route("POST")
def login(database: Database.Database, request: flask.Request) -> Types.func_resp:
    data: dict[str, any] = request.get_json()

    email: Types.union_s_n = data.get("email")
    password: Types.union_s_n = data.get("password")

    if None in [email, password]:
        return flask.make_response("Email ou Mot de Passe manquant",
                                   400,
                                   {'Authentication': '"Identifiants nécessaires"'}
                                   )

    hashed_password: str = hashlib.sha256(password.encode()).hexdigest()

    del password

    query_result: list[dict[str, str]] = PasswordHandler.getPasswordByEmail(database, email)

    if len(query_result) == 0:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    query_result: dict[str, str] = query_result[0]

    if hashed_password != query_result["password"]:
        return flask.make_response("Nom d`utilisateur ou mot de passe incorrect",
                                   401,
                                   {'Authentication': '"Authentication requise"'}
                                   )

    del query_result["password"]

    token: str = TokenHandler.createToken(query_result['id'])

    TokenHandler.addToken(database, token, query_result["id"])

    return_value: Types.dict_ss_imb = {'token': "Bearer " + token, 'user': query_result}

    return return_value
