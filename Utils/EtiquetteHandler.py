import datetime
import uuid


def getEtiquetteByUuid(database, etiquette_id):
    get_etiquette = {
        "where": [
            ["etiquettes", "id", etiquette_id]
        ],
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(get_etiquette)


def getAllEtiquettes(database):
    etiquette_query = {
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(etiquette_query)


def getEtiquettesByQuestionId(database, question_id):
    sql_etiquette_query = {
        "select": [
            ["etiquettes", "id"],
            ["etiquettes", "label"],
            ["etiquettes", "description"],
            ["etiquettes", "color"],
            ["etiquettes", "created_at"],
            ["etiquettes", "updated_at"]
        ],
        "where": [
            ["questions", "id", question_id]
        ],
        "from": {
            "tables": ["questions", "etiquette_question", "etiquettes"],
            "cond": [
                [
                    ["questions", "id"],
                    ["etiquette_question", "question_id"]
                ],
                [
                    ["etiquette_question", "etiquette_id"],
                    ["etiquettes", "id"]
                ]
            ]
        }
    }

    return database.query(sql_etiquette_query)


def createEtiquette(database, label, description, color) -> str:
    etiquette_id = uuid.uuid4()

    while len(getEtiquetteByUuid(database, etiquette_id)) > 0:
        etiquette_id = uuid.uuid4()

    insert_etiquette = {
        "table": "etiquettes",
        "action": "insert",
        "valeurs": [
            ["id", etiquette_id],
            ["label", label],
            ["description", description],
            ["color", color],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_etiquette)
    database.commit()

    return str(etiquette_id)


def removeEtiquette(database, etiquette_id):
    question_etiquette_execute = {
        "table": "etiquette_question",
        "action": "delete",
        "valeurs": [
            ["question_id", etiquette_id]
        ]
    }

    etiquette_execute = {
        "table": "etiquettes",
        "action": "delete",
        "valeurs": [
            ["id", etiquette_id]
        ]
    }

    database.execute(question_etiquette_execute)
    database.execute(etiquette_execute)
    return database.commit()


def joinEtiquetteQuestion(database, question_id, etiquette_id, commit: bool = True):
    insert_question_etiquette_query = {
        "table": "etiquette_question",
        "action": "insert",
        "valeurs": [
            ["etiquette_id", etiquette_id],
            ["question_id", question_id],
        ]
    }

    database.execute(insert_question_etiquette_query)

    if commit:
        database.commit()
