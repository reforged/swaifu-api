import datetime
from BDD.Decorator import decorator

from BDD.Table import Table
from BDD.HasOne import HasOne


@decorator
class Reponses(Table):
    id: str
    body: str
    valide: str
    question_id: str

    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    questions: HasOne("questions", "question_id")
