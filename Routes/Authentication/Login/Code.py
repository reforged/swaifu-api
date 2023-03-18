import flask
import hashlib

import BDD.Database as Database

import Utils.Handlers.PasswordHandler as PasswordHandler
import Utils.Route as Route
import Utils.Handlers.TokenHandler as TokenHandler
import Utils.Types as Types


@Route.route("POST")
def student_id_login(database: Database.Database, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../authentification/login/code - Méthode POST

    Permet aux utilisateurs de se connecter à leur compte utilisant leur numéro étudiant et renvoie un token si bon

    :param database: Objet base de données
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

    query_result: list[dict[str, str]] = PasswordHandler.getPasswordByStudentId(database, numero)

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

    TokenHandler.addToken(database, token, query_result["id"])

    return_value: Types.dict_ss_imb = {'token': "Bearer " + token, 'user': query_result}

    return return_value
