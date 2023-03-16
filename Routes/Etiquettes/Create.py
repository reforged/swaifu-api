import flask

import BDD.Database as Database

import Erreurs.HttpErreurs as HttpErreurs

import Permissions.Policies as Policies

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(method="POST")
def etiquette_create(database: Database.Database, request: flask.Request) -> Types.func_resp:

    # TODO : Enlever et utiliser décorateur de middleware
    token: dict[str, str] = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data: dict[str, str] = request.get_json()

    label: str = data.get("label")
    color: str = data.get("color")
    user_id: str = token.get('id')

    if None in [label, color, user_id]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    EtiquetteHandler.createEtiquette(database, label, color)

    return {"Message": "Succès"}
