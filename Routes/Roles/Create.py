import flask

import BDD.Database as Database

import Permissions.Policies as Policies

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.RoleHandler as RoleHandler

import Utils.Route as Route


@Route.route(method="POST")
def createRole(database: Database.Database, request: flask.Request):
    token: dict[str, str] = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data = request.get_json()

    label = data.get("label")
    power = data.get("power")

    for value in [label, power]:
        if value is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    role_id = RoleHandler.createRole(database, label, power)

    data["id"] = role_id

    return data
