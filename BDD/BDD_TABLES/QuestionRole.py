from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class QuestionRole(Pivot):
    table_name: str = "question_role"

    id: str
    question_id: str
    role_id: str

    questions: HasMany("questions", "id", "question_id")
    roles: HasMany("roles", "id", "role_id")
