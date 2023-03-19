import BDD.Database as Database

import Utils.Handlers.PermissionHandler as PermissionHandler

import Utils.Route as Route


@Route.route(url="<permission_id>")
def getPermissionById(permission_id: str, database: Database.Database):
    return PermissionHandler.getPermissionById(database, permission_id)[0]
