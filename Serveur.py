import flask
from flask import request, send_from_directory
from flask_cors import CORS
import os
from Utils.Dotenv import getenv
import logging
from BDD.ConnectionHandler import initiate

import Utils.RoutesImporter as RoutesImporter

RoutesImporter.current_dir = os.path.dirname(__file__)

psql_params = {
    "database": getenv("database"),
    "url": getenv("url"),
    "user": getenv("user"),
    "password": getenv("password"),
    "port": getenv("port")
}

App = flask.Flask(__name__)
CORS(App, support_credentials=True, ressources={
    "*": {
        "origins": ["*"],
        "methods": ["OPTIONS", "GET", "POST"],
        "allow_headers": ["Authorization", "Content-type"]
    }
})

Db = initiate("psql", psql_params)


param = {
    "database": Db,
    "request": request,
    "chiffre": 5
}

RoutesImporter.import_route(os.path.dirname(__file__), "Routes", "/", App, param, os.path.basename(__file__))

serve_app = ['/', '/manager', '/login', '/register', '/manager/questions', '/manager/etiquettes']


def a():
    return send_from_directory('Static', 'index.html')


for url in serve_app:
    App.route(url)(a)


@App.route('/assets/<name>')
def b(name):
    return send_from_directory('Static/assets', name)


App.run()
