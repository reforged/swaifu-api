from BDD.Table import Table
import datetime
from BDD.ManyToMany import ManyToMany
from BDD.BDD_TABLES.EtiquetteQuestion import EtiquetteQuestion


class Etiquettes(Table):
    id: str
    label: str
    color: str
    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    questions: ManyToMany("questions", EtiquetteQuestion)
