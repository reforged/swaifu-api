import BDD.Database as Database
import flask

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.UserHandler as UserHandler
import Utils.Handlers.RoleUserHandler as RoleUserHandler
import Utils.Handlers.PermissionUserHandler as PermissionUserHandler

import Utils.Route as Route


@Route.route(method="POST")
def createUser(database: Database.Database, request: flask.Request):
    """
    Gère la route .../users/create - Méthode POST

    Permet à un utilisateur de créer plusieurs utilisateurs à la fois.

    Nécessite d'être connecté.

    :param database: Objet base de données
    :param request: Objet Request de flask
    """

    data = request.get_json()

    firstname: str = data.get("firstname")
    lastname: str = data.get("lastname")
    password: str = data.get("password")

    email: str = data.get("email")
    numero: str = data.get("numero")

    for value in [firstname, lastname, password, email, numero]:
        if value is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    user_id = UserHandler.addUser(database, password, email, numero, firstname, lastname)

    roles = data.get("roles", [])
    permissions = data.get("permissions", [])

    for role_id in roles:
        RoleUserHandler.addRoleUser(database, user_id, role_id)

    for permission_id in permissions:
        PermissionUserHandler.addPermissionUser(database, permission_id, user_id)

    del data["password"]

    return data
