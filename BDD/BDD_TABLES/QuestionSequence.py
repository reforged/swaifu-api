from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class QuestionSequence(Pivot):
    table_name: str = "question_sequence"

    id: str
    question_id: str
    sequence_id: str

    questions: HasMany("questions", "id", "question_id")
    sequences: HasMany("sequences", "id", "sequence_id")
