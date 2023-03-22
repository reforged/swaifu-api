import flask

import BDD.Model as Model

import Permissions.Policies as Policies

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.RoleHandler as RoleHandler

import Utils.Route as Route


@Route.route(method="POST")
def createRole(query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../roles/create - Méthode POST

    Permet à un utilisateur de créer un nouveau rôle.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    # Récupération du token
    token: dict[str, str] = Policies.check_token(request, query_builder)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data = request.get_json()

    label = data.get("label")
    power = data.get("power")

    # On s'assure de la bonne existence des données
    for value in [label, power]:
        if value is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    role_id = RoleHandler.createRole(query_builder, label, power)

    # On renvoie l'id de l'objet créé
    data["id"] = role_id

    return data
