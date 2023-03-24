import flask

import BDD.Model as Model

import Permissions.Policies as Policies

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Types as Types


def me(query_builder: Model.Model, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../authentication/me - Méthode GET

    Permet aux utilisateurs d'obtenir des informations sur eux-mêmes (Hors mot-de-passe)

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """
    token: Types.union_dss_n = Policies.check_token(request, query_builder)

    if token is None:
        return flask.make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    res = query_builder.table("users").where("id", token["id"]).load("roles")

    if len(res) == 0:
        return {"Error": "User not found"}

    # Nous ne voulons qu'un seul élément (-> unique donc assuré)
    res = res[0]
    # Sur lequel nousn chargeons les permissions que l'utilisateur à, en plus des rôles
    res.load("permissions")
    [row.load("permissions") for row in res.roles]

    res = res.export()

    # Evitons d'envoyer au client le mot de passe
    del res["password"]

    return res
