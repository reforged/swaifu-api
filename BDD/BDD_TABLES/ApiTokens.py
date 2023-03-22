import datetime
from BDD.Decorator import decorator

from BDD.Table import Table

from BDD.HasOne import HasOne


@decorator
class ApiTokens(Table):
    table_name: str = "api_tokens"

    id: str
    user_id: str
    name: str
    token: str

    created_at: datetime.datetime.timestamp
    expires_at: datetime.datetime.timestamp

    users: HasOne("users", "user_id")
