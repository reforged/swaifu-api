import uuid
from BDD.Decorator import decorator

import BDD.Table as Table
from BDD.HasOne import HasOne


@decorator
class ReponseUser(Table.Table):
    table_name: str = "reponse_user"

    id: str = uuid.uuid4
    body: str
    valide: str
    user_id: str
    session_id: str
    question_id: str

    users: HasOne("users", "user_id")
    sessions: HasOne("sessions", "session_id")
    question: HasOne("questions", "question_id")
