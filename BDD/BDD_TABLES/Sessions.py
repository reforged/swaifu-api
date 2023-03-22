import datetime
from BDD.Decorator import decorator

from BDD.Table import Table
from BDD.ManyToMany import ManyToMany
from BDD.HasOne import HasOne
from BDD.HasMany import HasMany
from BDD.BDD_TABLES.Su import Su


@decorator
class Sessions(Table):
    id: str
    sequence_id: str
    code: str
    participants: str

    created_at: datetime.datetime.timestamp

    users: ManyToMany("users", Su)
    sequences: HasOne("sequences", "sequence_id")
    permissions: HasMany("permissions", "session_id")
