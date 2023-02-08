from BDD.Database import Database
import datetime


def addToken(database: Database, token: str, user_uuid):
    insert = {
        "table": "api_tokens",
        "action": "insert",
        "valeurs": [
            ["token", token],
            ["user_id", user_uuid],
            ["expires_at", str((datetime.datetime.now() + datetime.timedelta(hours=24)).astimezone())],
            ["created_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(insert)
    print(database.commit())

