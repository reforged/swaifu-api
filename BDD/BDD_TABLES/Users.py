import datetime
from BDD.Decorator import decorator

from BDD.Table import Table
from BDD.HasMany import HasMany
from BDD.ManyToMany import ManyToMany
from BDD.BDD_TABLES.RoleUser import RoleUser
from BDD.BDD_TABLES.PermissionUser import PermissionUser
from BDD.BDD_TABLES.Su import Su


@decorator
class Users(Table):

    table_name = "users"

    id: str
    email: str
    numero: str
    firstname: str
    lastname: str
    password: str

    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    questions: HasMany("questions", "user_id")
    roles: ManyToMany("roles", RoleUser)
    permissions: ManyToMany("permissions", PermissionUser)
    sessions: ManyToMany("sessions", Su)
    tokens: HasMany("api_tokens", "user_id")
    reponses: HasMany("reponse_user", "user_id")
