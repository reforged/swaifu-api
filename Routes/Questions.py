from BDD.Database import Database


def questions(database: Database, request):
    sql_question_query = {
        "from": {
            "tables": ["questions"]
        }
    }

    question_query_result = database.query(sql_question_query)

    # TODO: Obtenir étiquettes pour les questions
