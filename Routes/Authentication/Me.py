import flask

import BDD.Database as Database
import Erreurs.HttpErreurs as HttpErreurs
import Permissions.Policies as Policies
import Utils.Handlers.UserHandler as UserHandler
import Utils.Types as Types


def me(database: Database.Database, request: flask.Request) -> Types.func_resp:
    token: Types.union_dss_n = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    return_value = UserHandler.getUserByUuid(database, token['id'])[0]
    del return_value["password"]

    # TODO: [0] présent avant ?
    return return_value
