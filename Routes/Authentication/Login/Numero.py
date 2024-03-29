import flask
import hashlib

import BDD.Model as Model

import Utils.Handlers.TokenHandler as TokenHandler

import Utils.Route as Route

import Utils.Types as Types


@Route.route("POST")
def student_id_login(query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../authentification/login/code - Méthode POST

    Permet aux utilisateurs de se connecter à leur compte utilisant leur numéro étudiant et renvoie un token si bon

    :param query_builder: Objet Model
    :param request: Objet requête de flask
    :return:
    """
    data: dict[str, any] = request.get_json()

    numero: Types.union_s_n = data.get("numero")
    password: Types.union_s_n = data.get("password")

    if None in [numero, password]:
        return flask.make_response("Numéro étudiant ou Mot de Passe manquant",
                                   400,
                                   {'Authentication': '"Identifiants nécessaires"'}
                                   )

    hashed_password: str = hashlib.sha256(password.encode()).hexdigest()

    # Petite prudence probablement inutile vu le fonctionnement de python
    del password

    query_result: list[dict[str, str]] = query_builder.table("users").where("numero", numero).execute()

    if len(query_result) == 0:
        query_result = [{"password": ""}]

    query_result: dict[str, str] = query_result[0]

    if hashed_password != query_result["password"]:
        return flask.make_response("Numéro étudiant ou Mot de Passe incorrect",
                                   401,
                                   {'Authentication': '"Authentication requise"'}
                                   )

    del query_result["password"]

    token: str = TokenHandler.createToken(query_result['id'])

    TokenHandler.addToken(query_builder, token, query_result["id"])

    return_value: Types.dict_ss_imb = {'token': "Bearer " + token, 'user': query_result}

    return return_value
