import BDD.Database as Database
import flask

import Utils.HandleUser as HandleUser


def createMany(database: Database.Database, request: flask.Request):
    listeAInscrire = request.get_json()

    HandleUser.addUsers(database, listeAInscrire)
