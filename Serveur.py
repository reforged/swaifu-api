import flask
import os

import BDD.ConnectionHandler as ConnectionHandler

import Utils.Dotenv as Dotenv
import Utils.RoutesImporter as RoutesImporter

RoutesImporter.current_dir = os.path.dirname(__file__)

App = flask.Flask(__name__)


@App.after_request
def after_request_func(response):
    origin = flask.request.headers.get('Origin')
    if flask.request.method == 'OPTIONS':
        response = flask.make_response()
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


Db = ConnectionHandler.initiate(Dotenv.getenv("DB_TYPE"))


param = {
    "database": Db,
    "request": flask.request
}

# RoutesImporter.import_route(os.path.dirname(__file__), "Routes", "/", App, param, os.path.basename(__file__))


RoutesImporter.import_route(os.path.dirname(__file__), r"C:/Users/ospat/PycharmProjects/Api/Routes", "/", App, param, os.path.basename(__file__))

serve_app = ['/', '/manager', '/login', '/register', '/manager/questions', '/manager/etiquettes']


def a():
    return flask.send_from_directory('Static', 'index.html')


for url in serve_app:
    App.route(url)(a)


@App.route('/assets/<name>')
def b(name):
    return flask.send_from_directory('Static/assets', name)


App.run(port=3333)
