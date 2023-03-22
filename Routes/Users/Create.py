import flask

import BDD.Model as Model

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.UserHandler as UserHandler

import Utils.Route as Route


@Route.route(method="POST")
def createUser(query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../users/create - Méthode POST

    Permet à un utilisateur de créer un autre utilisateur.

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    data = request.get_json()

    firstname: str = data.get("firstname")
    lastname: str = data.get("lastname")
    password: str = data.get("password")

    email: str = data.get("email")
    numero: str = data.get("numero")

    # Si les valeurs sont bien présentes
    for value in [firstname, lastname, password]:
        if value is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    # Seul l'un des deux champs peut être nul.
    if email is None and numero is None:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    roles = data.get("roles", [])
    permissions = data.get("permissions", [])

    role_list = query_builder.table("roles").execute()
    permission_list = query_builder.table("permissions").execute()

    role_list = [role["id"] for role in role_list]
    permission_list = [permission["id"] for permission in permission_list]

    i = 0
    error_message = {"errors": []}

    # Puisque nous ne créons aucun rôle ou permissions, on vérifie la bonne existence des roles et étiquettes avant
    # De commencer quoi que ce soit
    for role_id in roles:
        if role_id not in role_list:
            error_message["errors"].append({
                "rule": "exists",
                "field": f"roles.{i}",
                "message": "exists validation failure"
            })

            i += 1

    i = 0

    for permission_id in permissions:
        if permission_id not in permission_list:
            error_message["errors"].append({
                "rule": "exists",
                "field": f"permissions.{i}",
                "message": "exists validation failure"
            })

            i += 1

    # Dans le cas de non-présence, on annule tout et on renvoie une erreur
    if len(error_message["errors"]) > 0:
        query_builder.rollback()
        return flask.make_response("Exists validation failure", 422, error_message)

    # Et enfin sinon on crée les questions
    user_id = UserHandler.addUser(query_builder, password, email, numero, firstname, lastname, commit=False)

    for role_id in roles:
        query_builder.table("role_user", "insert").where("user_id", user_id).where("role_id", role_id).execute(commit=False)

    for permission_id in permissions:
        query_builder.table("permission_user", "insert").where("permission_id", permission_id).where("user_id", user_id).execute(commit=False)

    # Bien sûr, on évite de renvoyer le mot de passe (viande-haché)
    del data["password"]

    return data
