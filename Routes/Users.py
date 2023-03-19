import BDD.Database as Database

import Utils.Handlers.UserHandler as UserHandler


def getAllUsers(database: Database.Database):
        return UserHandler.getAllUsers(database)
