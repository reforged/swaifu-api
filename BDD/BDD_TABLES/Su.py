from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class Su(Pivot):
    id: str
    session_id: str
    user_id: str

    sessions: HasMany("sessions", "id", "session_id")
    users: HasMany("users", "id", "user_id")
