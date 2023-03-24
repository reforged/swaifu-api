import flask

import BDD.Model as Model

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Route as Route

import Utils.Types as Types


@Route.route(method="delete")
def logout(query_builder: Model.Model, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../authentication/logout - Méthode DELETE

    Permet aux utilisateurs de se déconnecter de leur compte

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """
    token: Types.union_s_n = None

    if "Authorization" in request.headers:
        # [7:] Puisque le token est précédé par 'Bearer '
        token = request.headers["Authorization"][7:]

    if token is None:
        return flask.make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    query_builder.table("api_tokens", "delete").where("token", token).execute()

    return {"token": token}
