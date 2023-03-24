import flask

import BDD.Model as Model

import Utils.Route as Route

import Permissions.Policies as Policies


@Policies.middleware(["update:permission"])
@Route.route(url="<permission_id>")
def getPermissionById(permission_id: str, query_builder: Model.Model):
    """
    Gère la route .../permissions/<permission_id> - Méthode GET

    Permet à un utilisateur de récupérer une question en fonction de son id.

    :param permission_id: Id de la permission désirée
    :param query_builder: Objet Model
    """

    res = query_builder.table("permissions").where("id", permission_id).load("roles", query_builder.select("roles.id"))

    if len(res) == 0:
        return flask.make_response({"Error": "Permission non trouvée"}, 404)

    res = res[0].load("users", query_builder.select("users.id"))

    return res.export()


@Policies.middleware(["destroy:permission"])
@Route.route(method="delete", url="<permission_id>")
def deletePermission(permission_id: str, query_builder: Model.Model):
    """
    Gère la route .../permissions/<permission_id> - Méthode DELETE

    Permet à un utilisateur de supprimer un compte utilisateur.

    Nécessite d'être connecté.

    :param permission_id: Id de la permission concerné
    :param query_builder: Objet Model
    """

    query_builder.table("permissions", "delete").where("id", permission_id).execute()

    return {"message": "Supprimé avec succès"}
