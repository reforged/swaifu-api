import uuid
import datetime
from BDD.Decorator import decorator

import BDD.Table as Table
from BDD.HasOne import HasOne


@decorator
class Reponses(Table.Table):
    id: str = uuid.uuid4
    body: str
    valide: str
    question_id: str

    created_at: datetime.datetime.timestamp = Table.getTime
    updated_at: datetime.datetime.timestamp = Table.getTime

    questions: HasOne("questions", "question_id")
