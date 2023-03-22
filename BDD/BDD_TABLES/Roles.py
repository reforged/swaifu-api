import datetime
from BDD.Decorator import decorator

from BDD.Table import Table
from BDD.ManyToMany import ManyToMany
from BDD.BDD_TABLES.RoleUser import RoleUser
from BDD.BDD_TABLES.PermissionRole import PermissionRole
from BDD.BDD_TABLES.QuestionRole import QuestionRole


@decorator
class Roles(Table):
    id: str
    label: str
    power: str

    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    users: ManyToMany("users", RoleUser)
    questions: ManyToMany("questions", QuestionRole)
    permissions: ManyToMany("permissions", PermissionRole)
