import BDD.Database as Database

import Utils.Handlers.RoleHandler as RoleHandler

import Utils.Route as Route


@Route.route(url="<role_id>")
def getRoleById(role_id: str, database: Database.Database):
    return RoleHandler.getRoleById(database, role_id)[0]
