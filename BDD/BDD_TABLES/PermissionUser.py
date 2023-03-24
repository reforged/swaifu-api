from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class PermissionUser(Pivot):
    table_name: str = "permission_user"

    id: str
    permission_id: str
    user_id: str

    permissions: HasMany("permissions", "id", "permission_id")
    users: HasMany("users", "id", "user_id")
