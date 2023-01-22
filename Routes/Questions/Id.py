from Utils.Route import route
from Utils.GetEtiquette import getEtiquette


@route(url="<question_id>")
def question_get_question_id(question_id, database):
    sql_question_query = {
        "where": [
            ["questions", "user_id", question_id, "and"]
        ],
        "from": {
            "tables": ["questions"]
        }
    }

    question_query_result = database.query(sql_question_query)[0]

    question_query_result["etiquettes"] = getEtiquette(database, question_query_result["id"])

    return question_query_result


@route(method="put", url="<question_id>")
def get_id(question_id, database):
    # TODO: Savoir quelle données sont données
    pass


@route(method="delete", url="<question_id>")
def get_id(question_id, database):
    question_etiquette_execute = {
        "table": "etiquette_question",
        "action": "delete",
        "valeurs": [
            ["question_id", question_id]
        ]
    }

    question_execute = {
        "table": "questions",
        "action": "delete",
        "valeurs": [
            ["id", question_id]
        ]
    }

    database.execute(question_etiquette_execute)
    database.execute(question_execute)
    database.commit()

    return "yes"
