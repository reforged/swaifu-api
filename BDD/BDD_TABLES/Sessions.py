import datetime
from BDD.Decorator import decorator
import uuid
import BDD.Table as Table
from BDD.ManyToMany import ManyToMany
from BDD.HasOne import HasOne
from BDD.HasMany import HasMany
from BDD.BDD_TABLES.Su import Su


@decorator
class Sessions(Table.Table):
    id: str = uuid.uuid4
    sequence_id: str
    code: str

    created_at: datetime.datetime.timestamp = Table.getTime

    users: ManyToMany("users", Su)
    sequence: HasOne("sequences", "sequence_id")
    permissions: HasMany("permissions", "session_id")
    reponses: HasMany("reponse_user", "session_id")
