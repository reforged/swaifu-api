import datetime
from BDD.Decorator import decorator

from BDD.Table import Table
from BDD.ManyToMany import ManyToMany
from BDD.HasMany import HasMany
from BDD.BDD_TABLES.QuestionSequence import QuestionSequence


@decorator
class Sequences(Table):
    id: str
    label: str

    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    sessions: HasMany("sessions", "sequence_id")
    questions: ManyToMany("questions", QuestionSequence)
