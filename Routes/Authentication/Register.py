import BDD.Database as Database
import flask
import Erreurs.HttpErreurs as HttpErreurs
import Utils.Route as Route
import datetime
import Utils.Handlers.TokenHandler as TokenHandler
import Utils.Handlers.UserHandler as UserHandler
import Utils.Types as Types

# from Permissions.Policies import middleware


# @middleware(["post:user"])
@Route.route(method="post")
def register(database: Database.Database, request: flask.Request) -> Types.func_resp:
    data: dict[any] = request.get_json()

    firstname: str = data.get("firstname")
    lastname: str = data.get("lastname")
    numero: str = data.get("numero")
    password: str = data.get("password")

    if None in [firstname, lastname, numero, password]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    if len(UserHandler.getUserByNumero(database, numero)) != 0:
        return flask.make_response(HttpErreurs.creation_impossible, 409, HttpErreurs.creation_impossible)

    user_uuid = UserHandler.addUser(database, password, numero, firstname, lastname)

    token: str = TokenHandler.createToken(user_uuid)

    TokenHandler.addToken(database, token, user_uuid)

    return_value = {'token':  "Bearer " + token, 'user': {
        'id': user_uuid,
        'numero': numero,
        'firstname': firstname,
        'lastname': lastname,
        'created_at': str(datetime.datetime.now().astimezone()),
        'updated_at': str(datetime.datetime.now().astimezone())
    }
            }

    return return_value
