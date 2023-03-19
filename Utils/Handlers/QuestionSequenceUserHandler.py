import BDD.Database as Database


def getQuestionSequenceUserBySessionId(database: Database.Database, session_id):
    get_question_sequence_user_by_id_query = {
        "where": {
            ["question_sequence_user", "session_id", session_id]
        },
        "from": {
            "tables": ["question_sequence_user"]
        }
    }

    return database.query(get_question_sequence_user_by_id_query)
