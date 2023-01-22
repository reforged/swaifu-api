from Utils.Route import route
from Utils.GetEtiquette import getEtiquette


@route(url='etiquette/<etiquette_id>')
def etiquette(etiquette_id, database):
    sql_etiquette_query = {
        "where": [
            ["etiquettes", "id", etiquette_id, "and"]
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

    question_query_result = database.query(sql_etiquette_query)

    for i in range(len(question_query_result)):
        question_query_result[i]["etiquettes"] = getEtiquette(database, question_query_result[i]["id"])

    return question_query_result
