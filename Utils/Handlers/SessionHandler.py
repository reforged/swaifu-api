import BDD.Model as Model


def createSession(sequence_id: str, code: str, query_builder: Model.Model, commit: bool = True):
    params = {
        "sequence_id": sequence_id,
        "code": code
    }

    return query_builder.table("sessions", "insert").where(params).execute(commit=commit)
