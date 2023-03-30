import flask_socketio
import flask
import os

import BDD.ConnectionHandler as ConnectionHandler
import BDD.Model as Model

import Utils.Handlers.CorsHandler as CorsHandler

import Utils.Dotenv as Dotenv
import Utils.RoutesImporter as RoutesImporter

import Sockets.SocketHandler as SocketHandler

App = flask.Flask(__name__)
Sio = flask_socketio.SocketIO(App, cors_allowed_origins=["http://localhost:3000", "http://localhost:3333"], logger=True, engineio_logger=True)

App.after_request(CorsHandler.after_request_func)


Db = ConnectionHandler.initiate(Dotenv.getenv("DB_TYPE"))
QueryBuilder = Model.Model(Db)

SocketHandler.load_sessions(Sio, QueryBuilder)


param = {
    "database": Db,
    "query_builder": QueryBuilder,
    "request": flask.request,
    "sio": Sio
}

current_filepath = __file__.replace("\\", "/")
current_dirname = os.path.dirname(current_filepath)

RoutesImporter.import_route(current_dirname, f"{current_dirname}/Routes", "/", App, param, os.path.basename(__file__))

Sio.run(App, port=3333)
