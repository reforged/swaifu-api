import flask
import datetime

import BDD.Database as Database

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.TokenHandler as TokenHandler
import Utils.Handlers.UserHandler as UserHandler

import Utils.Route as Route
import Utils.Types as Types

# from Permissions.Policies import middleware


# @middleware(["post:user"])
@Route.route(method="POST")
def register(database: Database.Database, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../authentification/register - Méthode POST

    Permet aux utilisateurs de créer un compte

    :param database: Objet base de données
    :param request: Objet Request de flask
    """

    data: dict[any] = request.get_json()

    firstname: str = data.get("firstname")
    lastname: str = data.get("lastname")
    email: str = data.get("email")
    password: str = data.get("password")

    if None in [firstname, lastname, email, password]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    if len(UserHandler.getUserByEmail(database, email)) != 0:
        return flask.make_response(HttpErreurs.creation_impossible, 409, HttpErreurs.creation_impossible)

    user_uuid = UserHandler.addUser(database, password, email, None, firstname, lastname)

    token: str = TokenHandler.createToken(user_uuid)

    TokenHandler.addToken(database, token, user_uuid)

    return_value = {'token':  "Bearer " + token, 'user': {
        'id': user_uuid,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'created_at': str(datetime.datetime.now().astimezone()),
        'updated_at': str(datetime.datetime.now().astimezone())
    }
            }

    return return_value
