import uuid
import datetime
from BDD.Decorator import decorator

import BDD.Table as Table
from BDD.ManyToMany import ManyToMany
from BDD.HasOne import HasOne
from BDD.HasMany import HasMany
from BDD.BDD_TABLES.EtiquetteQuestion import EtiquetteQuestion
from BDD.BDD_TABLES.QuestionSequence import QuestionSequence
from BDD.BDD_TABLES.QuestionRole import QuestionRole


@decorator
class Questions(Table.Table):
    id: str = uuid.uuid4
    label: str
    slug: str
    enonce: str
    type: str
    user_id: str
    created_at: datetime.datetime.timestamp = Table.getTime
    updated_at: datetime.datetime.timestamp = Table.getTime

    etiquettes: ManyToMany("etiquettes", EtiquetteQuestion)
    sequences: ManyToMany("sequences", QuestionSequence)
    roles: ManyToMany("roles", QuestionRole)

    user: HasOne("users", "user_id")

    reponses: HasMany("reponses", "question_id")
