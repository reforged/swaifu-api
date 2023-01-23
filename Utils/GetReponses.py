def getReponses(database, question_id):
    sql_etiquette_query = {
        "where": [
            ["reponses", "question_id", question_id, "and"]
        ],
        "from": {
            "tables": ["reponses"]
        }
    }

    return database.query(sql_etiquette_query)
