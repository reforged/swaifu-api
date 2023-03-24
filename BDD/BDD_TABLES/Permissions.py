import datetime
from BDD.Table import Table
from BDD.ManyToMany import ManyToMany
from BDD.BDD_TABLES.PermissionRole import PermissionRole
from BDD.BDD_TABLES.PermissionUser import PermissionUser


class Permissions(Table):
    id: str
    key: str
    label: str

    created_at: datetime.datetime.timestamp
    updated_at: datetime.datetime.timestamp

    roles: ManyToMany("roles", PermissionRole)
    users: ManyToMany("users", PermissionUser)
