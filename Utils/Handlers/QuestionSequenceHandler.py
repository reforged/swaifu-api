import BDD.Database as Database


def getQuestionBySequenceId(database: Database.Database, sequence_id: str):
    get_question_by_sequence_query = {
        "where": {
            ["question_sequence", "sequence_id", sequence_id]
        },
        "from": {
            "tables": ["question_sequence", "questions"]
        },
        "cond": [
            [
                ["question_sequence", "question_id"],
                ["questions", "id"]
            ]
        ]
    }

    return database.query(get_question_by_sequence_query)
