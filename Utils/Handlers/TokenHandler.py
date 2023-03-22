import datetime
import jwt

import BDD.Model as Model

import Utils.Dotenv as Dotenv


def createToken(user_id: str) -> str:
    """
    Fonction renvoyant l'id de l'utilisateur encodée dans un token.

    :param user_id: Id de l'utilisateur concerné
    :return:
    """

    return jwt.encode({'id': user_id}, Dotenv.getenv("token_key"), algorithm="HS256")


def addToken(query_builder: Model.Model, token: str, user_id: str, commit: bool = True) -> None:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour insérer un token.

    :param query_builder: Objet Model
    :param token: Token de l'utilisateur
    :param user_id: Id de l'utilisateur concerné
    :param commit: Si la fonction doit sauvegarder les changements
    """

    params = {
        "token": token,
        "user_id": user_id,
        "name": "Bearer",
        "expires_at": str((datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone()),
        "created_at": str(datetime.datetime.now().astimezone())
    }

    query_builder.table("api_tokens", "insert").where(params).execute(commit=commit)
