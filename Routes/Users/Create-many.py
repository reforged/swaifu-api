import BDD.Database as Database
import flask

import Utils.Handlers.UserHandler as UserHandler


def createMany(database: Database.Database, request: flask.Request):
    listeAInscrire = request.get_json()

    UserHandler.addUsers(database, listeAInscrire)
