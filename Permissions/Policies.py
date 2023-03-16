import datetime
import flask
import jwt

import BDD.Database as Database

from Erreurs.HttpErreurs import *

import Utils.Dotenv as Dotenv

import Utils.Handlers.TokenHandler as TokenHandler
import Utils.Handlers.PermissionHandler as PermissionHandler


def check_perm(database: Database.Database, user_id: str, permissions: list[str]) -> bool:
    """
    Fonction vérifiant quels droits possède un utilisateur donné et s'assure qu'il ait tout les droits demandés
    :param database: Objet base de données
    :param user_id: Identifiant de l'utilisateur à vérifier
    :param permissions: Liste des labels des permissions à vérifier
    :return:
    """
    permission_labels = [valeur["label"] for valeur in PermissionHandler.getPermissionByUser(database, user_id)]

    print(f"Query res : {permission_labels}")

    if "admin" in permission_labels:
        return True

    for required_permission in permissions:
        if required_permission not in permission_labels:
            return False

    return True


def check_token(req: flask.Request, database: Database.Database) -> str or None:
    """
    Fonction vérifiant pour une requête donnée si un token est bien donné, et s'il est valide
    :param req: Objet Request de flask
    :param database: Objet base de données
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

    query_result = TokenHandler.getToken(database, token)

    if len(query_result) == 0:
        return None

    # Dans le cas de token sans limite de vie, la valeur par défaut est 10 secondes dans le futur pour valider la
    # Vérification sans soucis
    expires_at_datetime = query_result[0].get("expires_at", datetime.datetime.now() + datetime.timedelta(seconds=10))

    if expires_at_datetime < datetime.datetime.now():
        return None

    return decoded_token


def middleware(policies: list):
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

            db: Database.Database = kwargs.get("database")

            if db is None:
                raise KeyError("Fonction nécessitant une connection à la BDD sans pouvoir.")

            decoded_token = check_token(flask.request, db)

            if decoded_token is None:
                return flask.make_response(token_invalide, 400, token_invalide)

            perm = check_perm(db, decoded_token["id"], policies)

            if not perm:
                return flask.make_response(non_authorise, 403, non_authorise)

            # On appelle la fonction initiale que si l'utilisateur a les permissions suffisantes
            return fonction(*args, **kwargs)

        # En raison du remplacement de la fonction par une autre, les méta-données sont perdues et ne peuvent être
        # Transféré comme le nom de la fonction, nous insérons donc un dictionnaire contenant les informations
        # Importantes au bon fonctionnement
        inner.__name__ = fonction.__name__

        inner.info_fonction = {
            "co_argcount": getattr(getattr(fonction, "__code__"), "co_argcount"),
            "co_varnames": getattr(getattr(fonction, "__code__"), "co_varnames"),
            "__module__": getattr(fonction, "__module__")
        }

        return inner

    return wrapper
