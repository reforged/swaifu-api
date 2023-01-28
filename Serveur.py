import flask
from flask import request, send_from_directory, make_response
import os
from Utils.Dotenv import getenv
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


@App.after_request
def after_request_func(response):
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response


Db = initiate("psql", psql_params)


param = {
    "database": Db,
    "request": request
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


App.run(port=3333)
