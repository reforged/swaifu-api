import BDD.Database as Database

import Utils.Handlers.PermissionHandler as PermissionHandler


def getAllPermissions(database: Database.Database):
    return PermissionHandler.getAllPermission(database)
