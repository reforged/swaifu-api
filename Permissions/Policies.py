import datetime
import flask
import jwt

import BDD.Model as Model

from Utils.Erreurs.HttpErreurs import *

import Utils.Dotenv as Dotenv


def check_perm(query_builder: Model.Model, user_id: str, *permissions_list: list[list[str]]) -> bool:
    """
    Fonction vérifiant quels droits possède un utilisateur donné et s'assure qu'il a tous les droits demandés

    :param query_builder: Objet Model
    :param user_id: Identifiant de l'utilisateur à vérifier
    :param permissions: Liste des labels des permissions à vérifier
    :return:
    """

    role_permissions_key = [row.export() for row in query_builder.table("users").where("id", user_id).load("roles", None, "permissions")]
    user_permissions_key = [row.export() for row in query_builder.table("users").where("id", user_id).load("permissions")]

    if len(role_permissions_key) == 0:
        return False

    role_permissions_key = (role_permissions_key[0]).get("roles", [])

    permissions_key = []

    for role in role_permissions_key:
        for permission in role.get("permissions", []):
            permission_label = permission.get("key")

            if permission_label not in permissions_key:
                permissions_key.append(permission_label)

    for user in user_permissions_key:
        for permission in user.get("permissions", []):
            permission_label = permission.get("key")

            if permission_label not in permissions_key:
                permissions_key.append(permission_label)

    if "admin" in permissions_key:
        return True

    for required_permission_list in permissions_list:
        found = 0

        for required_permission in required_permission_list:
            if required_permission in permissions_key:
                found += 1

        if found == len(required_permission_list):
            return True

    return False


def check_token(req: flask.Request, query_builder: Model.Model) -> str or None:
    """
    Fonction vérifiant pour une requête donnée si un token est bien donné, et s'il est valide
    :param req: Objet Request de flask
    :param query_builder: Objet Model
    :return:
    """
    if "Authorization" not in req.headers:
        return None

    # Les 7 premiers caractères sont 'Bearer '
    token = req.headers["Authorization"][7:]

    try:
        decoded_token = jwt.decode(token, Dotenv.getenv("token_key"), algorithms=["HS256"])
    except:
        return None

    query_result = query_builder.table("api_tokens").where("token", token).execute()

    if len(query_result) == 0:
        return None

    # Dans le cas de token sans limite de vie, la valeur par défaut est 10 secondes dans le futur pour valider la
    # Vérification sans soucis
    expires_at_datetime = query_result[0].get("expires_at", datetime.datetime.now().astimezone() +
                                              datetime.timedelta(seconds=10))

    if isinstance(expires_at_datetime, str):
        expires_at_datetime = datetime.datetime.fromisoformat(expires_at_datetime)

    if expires_at_datetime < datetime.datetime.now().astimezone():
        query_builder.table("api_tokens", "delete").where("token", token).execute()
        return None

    return decoded_token


def middleware(*policies: list[str]):
    """
    Fonction renvoyant un décorateur de fonction, initialise le décorateur en fonction des permissions à vérifier
    :param policies: Liste de labels de permissions
    """
    def wrapper(fonction):
        """
        Décorateur prenant en paramètre une fonction (celle qu'elle décore) et renvoie une autre fonction à appeler en
        Son lieu, nous permettant d'exécuter du code avant la fonction, notamment pour vérifier les permissions de
        L'utilisateur, ici.
        :param fonction: Fonction à décorer
        """
        def inner(*args, **kwargs):
            """
            Fonction dont le comportement remplace celle d'une autre
            Prends en arguments les paramètres de la fonction, et vérifie en fonction de 'policies' les permissions de
            L'utilisateur ayant fait la requête.
            Lève une exception en cas de paramètres Request ou Database manquant, et une erreur HTTP sinon
            """
            if "Authorization" not in flask.request.headers:
                return flask.make_response(non_authorise, 401, non_authorise)

            query_builder: Model.Model = kwargs.get("query_builder")

            if query_builder is None:
                raise KeyError("Fonction nécessitant une connection à la BDD sans pouvoir.")

            decoded_token = check_token(flask.request, query_builder)

            if decoded_token is None:
                return flask.make_response(token_invalide, 400, token_invalide)

            perm = check_perm(query_builder, decoded_token["id"], policies)

            if not perm:
                return flask.make_response(non_authorise, 403, non_authorise)

            # On appelle la fonction initiale que si l'utilisateur a les permissions suffisantes
            return fonction(*args, **kwargs)

        # En raison du remplacement de la fonction par une autre, les méta-données sont perdues et ne peuvent être
        # Transféré comme le nom de la fonction, nous insérons donc un dictionnaire contenant les informations
        # Importantes au bon fonctionnement
        inner.__name__ = fonction.__name__

        if hasattr(fonction, "info_fonction"):
            inner.info_fonction = fonction.info_fonction
            inner.info_fonction["co_argcount"] = getattr(getattr(fonction, "__code__"), "co_argcount")
            inner.info_fonction["co_varnames"] = getattr(getattr(fonction, "__code__"), "co_varnames")
            inner.info_fonction["__module__"] = getattr(fonction, "__module__")

        else:
            inner.info_fonction = {
                "co_argcount": getattr(getattr(fonction, "__code__"), "co_argcount"),
                "co_varnames": getattr(getattr(fonction, "__code__"), "co_varnames"),
                "__module__": getattr(fonction, "__module__")
            }

        if hasattr(fonction, "append_url"):
            inner.append_url = fonction.append_url

        elif hasattr(fonction, "url"):
            inner.url = fonction.url

        return inner

    return wrapper
