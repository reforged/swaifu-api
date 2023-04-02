import uuid
import datetime

import BDD.Table as Table
from BDD.Decorator import decorator

from BDD.HasMany import HasMany
from BDD.ManyToMany import ManyToMany

from BDD.BDD_TABLES.RoleUser import RoleUser
from BDD.BDD_TABLES.PermissionUser import PermissionUser
from BDD.BDD_TABLES.Su import Su


@decorator
class Users(Table.Table):

    table_name = "users"

    id: str = uuid.uuid4
    email: str
    numero: str
    firstname: str
    lastname: str
    password: str

    created_at: datetime.datetime.timestamp = Table.getTime
    updated_at: datetime.datetime.timestamp = Table.getTime

    questions: HasMany("questions", "user_id")
    roles: ManyToMany("roles", RoleUser)
    permissions: ManyToMany("permissions", PermissionUser)
    sessions: ManyToMany("sessions", Su)
    tokens: HasMany("api_tokens", "user_id")
    reponses: HasMany("reponse_user", "user_id")
