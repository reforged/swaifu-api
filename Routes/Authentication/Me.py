import flask

import BDD.Database as Database
import Utils.Erreurs.HttpErreurs as HttpErreurs
import Permissions.Policies as Policies
import Utils.Handlers.UserHandler as UserHandler
import Utils.Types as Types


def me(database: Database.Database, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../authentification/me - Méthode GET

    Permet aux utilisateurs d'obtenir des informations sur eux-mêmes (Hors mot-de-passe)

    Nécessite d'être connecté.

    :param database: Objet base de données
    :param request: Objet Request de flask
    """
    token: Types.union_dss_n = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    return_value = UserHandler.getUserByUuid(database, token['id'])[0]
    del return_value["password"]

    return return_value
