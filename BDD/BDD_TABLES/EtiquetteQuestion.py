from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class EtiquetteQuestion(Pivot):
    table_name: str = "etiquette_question"

    id: str
    etiquettes: HasMany("etiquettes", "id", "etiquette_id")
    questions: HasMany("questions", "id", "question_id")
