from BDD.Database import Database
from Utils.GetEtiquette import *
from Utils.GetReponses import getReponses


def questions(database: Database):
    sql_question_query = {
        "from": {
            "tables": ["questions"]
        }
    }

    question_query_result = database.query(sql_question_query)

    for i in range(len(question_query_result)):
        question_query_result[i]["etiquettes"] = getEtiquette(database, question_query_result[i]["id"])
        question_query_result[i]["reponses"] = getReponses(database, question_query_result[i]['id'])

    return question_query_result
