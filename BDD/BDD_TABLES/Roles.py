import uuid
import datetime
from BDD.Decorator import decorator

import BDD.Table as Table
from BDD.ManyToMany import ManyToMany
from BDD.BDD_TABLES.RoleUser import RoleUser
from BDD.BDD_TABLES.PermissionRole import PermissionRole
from BDD.BDD_TABLES.QuestionRole import QuestionRole


@decorator
class Roles(Table.Table):
    id: str = uuid.uuid4
    label: str
    power: str

    created_at: datetime.datetime.timestamp = Table.getTime
    updated_at: datetime.datetime.timestamp = Table.getTime

    users: ManyToMany("users", RoleUser)
    questions: ManyToMany("questions", QuestionRole)
    permissions: ManyToMany("permissions", PermissionRole)
