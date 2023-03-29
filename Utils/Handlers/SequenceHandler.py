import BDD.Database as Database
import BDD.Model as Model


# TODO : Supprimer
def getSessionSequenceByUuid(database: Database.Database, session_sequence_id: str) -> list[dict[str, str]]:
    get_session_sequence = {
        "where": [
            ["session_sequence", "id", session_sequence_id]
        ],
        "from": {
            "tables": ["session_sequence"]
        }
    }

    return database.query(get_session_sequence)


def addSequence(query_builder: Model.Model, label: str, question_list: list, commit: bool = True) -> str:
    params = {
        "label": label
    }

    sequence_uuid = query_builder.table("sequences", "insert").where(params).execute(commit=False)

    for id_question in question_list:
        params = {
            "question_id": id_question,
            "sequence_id": sequence_uuid
        }

        query_builder.table("question_sequence", "insert").where(params).execute(commit=False)

    if commit:
        query_builder.commit()

    return sequence_uuid
