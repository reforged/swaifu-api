import datetime
import flask
import hashlib

import BDD.Model as Model

import Utils.Route as Route

import Permissions.Policies as Policies


@Policies.middleware(["update:user"])
@Route.route(url="<user_id>")
def getUserById(user_id: str, query_builder: Model.Model):
    """
    Gère la route .../users/<user_id> - Méthode GET

    Permet à un utilisateur de récupérer un utilisateur en fonction de son id.

    :param user_id: Id de l'utilisateur' désirée
    :param query_builder: Objet Model
    """

    # roles + permissions + reponses_user
    # On récupère l'utilisateur demandé, puis on charge ses permissios, roles, et réponses données aux sessions
    res = query_builder.table("users").where("id", user_id).load("roles")

    if len(res) == 0:
        return {"Error": "User not found"}

    res = res[0]
    res.load("permissions")
    res.load("reponses")
    res = res.export()

    del res["password"]

    return res


@Policies.middleware(["update:user"])
@Route.route("PUT", "<user_id>")
def putUserById(user_id: str, query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../users/<user_id> - Méthode PUT

    Permet à un utilisateur de modifier un utilisateur en fonction de son id.

    :param user_id: Id de l'utilisateur' désirée
    :param query_builder: Objet Model
    """

    old = query_builder.table("users").where("id", user_id).execute()

    if len(old) == 0:
        return flask.make_response({"Error": "Utilisateur non trouvée"}, 404)

    old = old[0]

    data = request.get_json()

    new_val = {
        "updated_at": datetime.datetime.now().astimezone()
    }

    # Vérification des champs à remplacer
    for key in ["email", "numero", "firstname", "lastname"]:
        if old.get(key) != data.get(key):
            if data.get(key) is not None:
                new_val[key] = data.get(key)

    # Si l'utilisateur souhaite modifier son mot de passe il faut bien sûr le hacher...
    if "password" in data:
        hashed_new_password = hashlib.sha256(data["password"].encode()).hexdigest()
        del data["password"]

        if hashed_new_password != old["password"]:
            new_val["password"] = hashed_new_password

    query_builder.table("users", "alter", user_id).where(new_val).execute()

    if data.get("roles", []):
        old_role = query_builder.table("users").where("id", user_id).load("roles")[0]
        old_role = [row.get("id") for row in old_role.export().get("roles")]

        new_role_val = []
        del_role = []

        for role_id in data.get("roles", []):
            if role_id not in new_role_val:
                if len(query_builder.table("roles").where("id", role_id).execute()) != 0:
                    new_role_val.append(role_id)

        for role_id in old_role:
            if role_id not in new_role_val:
                del_role.append(role_id)

        for role_id in new_role_val:
            if role_id not in old_role:
                params = {
                    "role_id": role_id,
                    "user_id": user_id
                }

                query_builder.table("role_user", "insert").where(params).execute(commit=False)

        for role_id in del_role:
            if role_id in old_role:
                query_builder.table("role_user", "delete").where("role_id", role_id).where("user_id", user_id).execute(commit=False)

    if data.get("permissions", []):
        old_permission = query_builder.table("users").where("id", user_id).load("permissions")[0]
        old_permission = [row.get("id") for row in old_permission.export().get("permissions")]

        new_permission_val = []
        del_permission = []

        for permission_id in data.get("permissions", []):
            if permission_id not in new_permission_val:
                if len(query_builder.table("permissions").where("id", permission_id).execute()) != 0:
                    new_permission_val.append(permission_id)

        for permission_id in old_permission:
            if permission_id not in new_permission_val:
                del_permission.append(permission_id)

        for permission_id in new_permission_val:
            if permission_id not in old_permission:
                params = {
                    "permission_id": permission_id,
                    "user_id": user_id
                }

                query_builder.table("permission_user", "insert").where(params).execute(commit=False)

        for permission_id in del_permission:
            if permission_id in old_permission:
                query_builder.table("permission_user", "delete").where("permission_id", permission_id).where("user_id",user_id).execute(commit=False)

    query_builder.commit()

    return {"Message": "Succès"}


@Policies.middleware(["destroy:user"])
@Route.route(method="delete", url="<user_id>")
def delete_user(user_id: str, query_builder: Model.Model):
    """
    Gère la route .../users/<user_id> - Méthode DELETE

    Permet à un utilisateur de supprimer un compte utilisateur.

    Nécessite d'être connecté.

    :param user_id: Id de l'utilisateur concerné
    :param query_builder: Objet Model
    """

    query_builder.table("users", "delete").where("id", user_id).execute()

    return {"message": "Supprimé avec succès"}
