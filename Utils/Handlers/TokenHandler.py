import datetime
import jwt

import BDD.Database as Database

import Utils.Dotenv as Dotenv


def createToken(user_id: str) -> str:
    """
    Fonction renvoyant l'id de l'utilisateur encodée dans un token.

    :param user_id: Id de l'utilisateur concerné
    :return:
    """

    return jwt.encode({'id': user_id}, Dotenv.getenv("token_key"), algorithm="HS256")


def getToken(database: Database.Database, token: str) -> list[dict]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir un token.

    :param database: Objet base de données
    :param token: Token de l'utilisateur
    """

    get_token = {
        "select": [
            ["api_tokens", "token"]
        ],
        "where": [
            ["api_tokens", "token", token, "and"]
        ],
        "from": {
            "tables": ["api_tokens"]
        }
    }

    return database.query(get_token)


def addToken(database: Database.Database, token: str, user_id: str, commit: bool = True) -> None:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour insérer un token.

    :param database: Objet base de données
    :param token: Token de l'utilisateur
    :param user_id: Id de l'utilisateur concerné
    :param commit: Si la fonction doit sauvegarder les changements
    """

    insert_token = {
        "table": "api_tokens",
        "action": "insert",
        "valeurs": [
            ["token", token],
            ["user_id", user_id],
            ["name", "Bearer"],
            ["expires_at", str((datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone())],
            ["created_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(insert_token)

    if commit:
        database.commit()


def removeToken(database: Database.Database, token: str, commit: bool = True) -> None:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir un token en fonction de son
    id.

    :param database: Objet base de données
    :param token: Token de l'utilisateur
    :param commit: Si la fonction doit sauvegarder les changements
    """

    remove_token_query = {
        "table": "api_tokens",
        "action": "delete",
        "valeurs": [
            ["token", "Bearer " + token]
        ]
    }

    database.execute(remove_token_query)

    if commit:
        database.commit()
