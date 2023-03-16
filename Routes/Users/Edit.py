import Utils.UserHandler as UserHandler
import Utils.Route as Route
import BDD.Database as Database


@Route.route(method="delete", url="<user_id>")
def delete_user(user_id: str, database: Database.Database):
    UserHandler.delete_user(database, user_id)
