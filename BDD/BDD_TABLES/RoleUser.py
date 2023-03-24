from BDD.HasMany import HasMany
from BDD.Pivot import Pivot
from BDD.Decorator import decorator


@decorator
class RoleUser(Pivot):
    table_name: str = "role_user"

    id: str
    role_id: str
    user_id: str

    roles: HasMany("roles", "id", "role_id")
    users: HasMany("users", "id", "user_id")
