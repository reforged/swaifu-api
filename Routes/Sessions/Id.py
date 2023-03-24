import flask

import BDD.Model as Model

import Utils.Route as Route

import Permissions.Policies as Policies


@Policies.middleware(["update:session"])
@Route.route(url="<session_id>")
def getSessionById(session_id: str, query_builder: Model.Model):
    """
    Gère la route .../sessions/<session_id> - Méthode GET

    Permet à un utilisateur de récupérer une session en fonction de son id.

    :param session_id: Id de la session désirée
    :param query_builder: Objet Model
    """

    # On ne souhaite pas récupérer les mots de passe des utilisateurs
    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname", "users.created_at", "users.updated_at"]

    # On charge les utilisateurs, ainsi que les permissions que le rôle possède peu après
    res = query_builder.table("sessions").where("id", session_id).load("reponses")

    if len(res) == 0:
        return flask.make_response({"Error": "Role non trouvée"}, 404)

    res = res[0]

    for reponse in res.reponses:
        reponse.load("users", query_builder.select(*info_wanted))

    res.load("users")

    return res.export()
