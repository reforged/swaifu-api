import flask
from flask import request
import os
from Utils.Dotenv import getenv

from BDD.ConnectionHandler import initiate

import Utils.RoutesImporter as RoutesImporter

api_url = "/api/v1"
RoutesImporter.current_dir = os.path.dirname(__file__)

psql_params = {
    "database": getenv("database"),
    "url": getenv("url"),
    "user": getenv("user"),
    "password": getenv("password"),
    "port": getenv("port")
}

App = flask.Flask(__name__)
Db = initiate("psql", psql_params)

password_request = {
    "select": [
        ["users", "password"],
        ["users", "id"]
    ],
    "where": [
        ["users", "email", "moi@gmail.com"]
    ],
    "from": {
        "tables": ["users"]
    }
}

# print(Db.su("select * from information_schema.tables"))
# res = Db.query(password_request)[0]

# print(res[0])
# print(res[1])

param = {
    "database": Db,
    "request": request,
    "chiffre": 5
}

RoutesImporter.import_route(os.path.dirname(__file__), "Routes", "/", App, param, os.path.basename(__file__))

App.run()
