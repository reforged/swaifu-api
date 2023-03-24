import uuid
import datetime

import BDD.Model as Model


def createSession(sequence_id: str, code: str, query_builder: Model.Model, commit: bool = True):
    session_id = str(uuid.uuid4())

    while len(query_builder.table("sessions").where("id", session_id).execute()) != 0:
        session_id = str(uuid.uuid4())

    params = {
        "id": session_id,
        "sequence_id": sequence_id,
        "code": code,
        "created_at": datetime.datetime.now().astimezone()
    }

    query_builder.table("sessions", "insert").where(params).execute(commit=commit)

    return session_id
