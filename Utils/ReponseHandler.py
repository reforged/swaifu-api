import uuid
import datetime

import BDD.Database as Database


def getReponseByUuid(database: Database.Database, reponse_id: str) -> list[dict[str, str]]:
    get_reponse = {
        "where": [
            ["reponses", "id", reponse_id]
        ],
        "from": {
            "tables": ["reponses"]
        }
    }

    return database.query(get_reponse)


def getReponses(database: Database.Database, question_id: str) -> list[dict[str, str]]:
    sql_etiquette_query = {
        "where": [
            ["reponses", "question_id", question_id]
        ],
        "from": {
            "tables": ["reponses"]
        }
    }

    return database.query(sql_etiquette_query)


def createReponse(database: Database.Database, body: str, valide: bool, question_id: str, commit: bool = True) -> str:
    reponse_id: str = str(uuid.uuid4())

    while len(getReponseByUuid(database, reponse_id)) > 0:
        reponse_id = str(uuid.uuid4())

    insert_reponse_query = {
        "table": "reponses",
        "action": "insert",
        "valeurs": [
            ["id", reponse_id],
            ["body", body],
            ["valide", valide],
            ["question_id", question_id],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_reponse_query)

    if commit:
        database.commit()

    return reponse_id
