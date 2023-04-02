import datetime
import uuid
from BDD.Decorator import decorator

import BDD.Table as Table
from BDD.ManyToMany import ManyToMany
from BDD.HasMany import HasMany
from BDD.BDD_TABLES.QuestionSequence import QuestionSequence


@decorator
class Sequences(Table.Table):
    id: str = uuid.uuid4
    label: str

    created_at: datetime.datetime.timestamp = Table.getTime
    updated_at: datetime.datetime.timestamp = Table.getTime

    sessions: HasMany("sessions", "sequence_id")
    questions: ManyToMany("questions", QuestionSequence)
