import BDD.Database as Database


def getSessionsBySequenceId(database: Database.Database, sequence_id: str):
    get_session_query = {
        "where": {
            ["session", "sequence_id", sequence_id]
        },
        "from": {
            "tables": ["session"]
        }
    }

    return database.query(get_session_query)
