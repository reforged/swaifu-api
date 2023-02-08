import datetime
import jwt

import BDD.Database as Database

import Utils.Dotenv as Dotenv


def createToken(user_id: str) -> str:
    return jwt.encode({'id': user_id}, Dotenv.getenv("token_key"), algorithm="HS256")


def addToken(database: Database.Database, token: str, user_id: str) -> None:
    insert_token = {
        "table": "api_tokens",
        "action": "insert",
        "valeurs": [
            ["token", token],
            ["user_id", user_id],
            ["expires_at", str((datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone())],
            ["created_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(insert_token)
    database.commit()


def removeToken(database: Database.Database, token: str, commit: bool = True) -> None:
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
