import datetime
import uuid

import BDD.Database as Database


def getUserResponseByUuid(database: Database.Database, reponse_user_id: str) -> list[dict[str, str]]:
    get_reponse_user = {
        "where": [
            ["reponse_user", "id", reponse_user_id]
        ],
        "from": {
            "tables": ["reponse_user"]
        }
    }

    return database.query(get_reponse_user)


def addQuestionSequenceUser(database: Database.Database, user_id: str, question_id: str, session_sequence_id: str) -> dict[str, str]:
    current_timestamp = datetime.datetime.now().astimezone()

    add_question_sequence_user = {
        "table": "question_sequence_user",
        "action": "insert",
        "valeurs": [
            ["user_id", user_id],
            ["question_id", question_id],
            ["session_sequence_id", session_sequence_id],
            ["created_at", current_timestamp]
        ]
    }

    database.execute(add_question_sequence_user)
    return database.lastVal()


def addUserResponse(database: Database.Database, body: str, valide: bool, qsu_id: str, commit: bool = True) -> str:
    reponse_user_id: str = str(uuid.uuid4())

    while len(getUserResponseByUuid(database, reponse_user_id)) > 0:
        reponse_user_id = str(uuid.uuid4())

    add_response_user = {
        "table": "response_user",
        "action": "insert",
        "valeurs": [
            ["id", reponse_user_id],
            ["body", body],
            ["valide", valide],
            ["qsu_id", qsu_id]
        ]
    }

    database.execute(add_response_user)

    if commit:
        database.commit()

    return reponse_user_id
