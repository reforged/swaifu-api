import flask

import BDD.Database as Database
import Erreurs.HttpErreurs as HttpErreurs
import Utils.Route as Route
import Utils.TokenHandler as TokenHandler
import Utils.Types as Types


@Route.route(method="delete")
def logout(database: Database.Database, request: flask.Request) -> Types.func_resp:
    token: Types.union_s_n = None

    if "Authorization" in request.headers:
        # [7:] Puisque le token est précédé par 'Bearer '
        token = request.headers["Authorization"][7:]

    if token is None:
        return flask.make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    TokenHandler.removeToken(database, token)

    return {"token": token}
