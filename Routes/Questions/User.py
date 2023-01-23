from Utils.Route import route
from Utils.GetEtiquette import getEtiquette
from Utils.GetReponses import getReponses


@route(url='user/<user_id>')
def user(user_id, database):
    sql_question_query = {
        "from": {
            "tables": ["questions", "users"],
            "cond": [
                [
                    ["questions", "user_id"],
                    ["users", "id"]
                ]
            ]
        }
    }

    question_query_result = database.query(sql_question_query)

    for i in range(len(question_query_result)):
        question_query_result[i]["etiquettes"] = getEtiquette(database, question_query_result[i]["id"])
        question_query_result[i]["reponses"] = getReponses(database, question_query_result[i]['id'])

    return question_query_result
