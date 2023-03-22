import flask

import BDD.Model as Model

import Utils.Route as Route


@Route.route(url="<role_id>")
def getRoleById(role_id: str, query_builder: Model.Model):
    """
    Gère la route .../roles/<role_id> - Méthode GET

    Permet à un utilisateur de récupérer un rôle en fonction de son id.

    :param role_id: Id de la permission désirée
    :param query_builder: Objet Model
    """

    # On ne souhaite pas récupérer les mots de passe des utilisateurs
    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname", "users.created_at", "users.updated_at"]

    # On charge les utilisateurs, ainsi que les permissions que le rôle possède peu après
    res = query_builder.table("roles").where("id", role_id).load("users", query_builder.select(*info_wanted))

    if len(res) == 0:
        return flask.make_response({"Error": "Role non trouvée"}, 404)

    res = res[0]
    res.load("permissions")

    return res.export()
