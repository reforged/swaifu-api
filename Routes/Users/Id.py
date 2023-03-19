import BDD.Database as Database

import Utils.Handlers.UserHandler as UserHandler

import Utils.Route as Route


@Route.route(url="<user_id>")
def getUserById(user_id: str, database: Database.Database):
    return UserHandler.getUserByUuid(database, user_id)
