from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class PermissionRole(Pivot):
    table_name: str = "permission_role"

    id: str
    permission_id: str
    role_id: str

    permissions: HasMany("permissions", "id", "permission_id")
    roles: HasMany("roles", "id", "role_id")
