import datetime
import uuid

from BDD.Decorator import decorator

import BDD.Table as Table

from BDD.HasOne import HasOne


@decorator
class ApiTokens(Table.Table):
    table_name: str = "api_tokens"

    id: str
    user_id: str
    name: str
    token: str

    created_at: datetime.datetime.timestamp = Table.getTime
    expires_at: datetime.datetime.timestamp = Table.defaultExpire

    users: HasOne("users", "user_id")
