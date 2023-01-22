from Utils.Route import route
from Utils.GetEtiquette import getEtiquette


@route(url='user/<user_id>')
def user(user_id, database):
    sql_question_query = {
        "where": [
            ["questions", "user_id", user_id, "and"]
        ],
        "from": {
            "tables": ["questions"]
        }
    }

    question_query_result = database.query(sql_question_query)

    for i in range(len(question_query_result)):
        question_query_result[i]["etiquettes"] = getEtiquette(database, question_query_result[i]["id"])

    return question_query_result
