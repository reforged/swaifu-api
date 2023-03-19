import BDD.Database as Database

import Utils.Handlers.RoleHandler as RoleHandler


def getAllRoles(database: Database.Database):
    return RoleHandler.getAllRoles(database)
