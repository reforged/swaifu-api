import flask
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
res = Db.query(password_request)[0]

print(res[0])
print(res[1])


# RoutesImporter.import_route("Routes", os.path.dirname(__file__), "/", App, os.path.basename(__file__))

# App.run()
