import flask_socketio
import flask
import os

import BDD.ConnectionHandler as ConnectionHandler
import BDD.Model as Model

import Utils.Handlers.CorsHandler as CorsHandler

import Utils.Dotenv as Dotenv
import Utils.RoutesImporter as RoutesImporter

import Sockets.SocketHandler as SocketHandler

RoutesImporter.current_dir = os.path.dirname(__file__)

App = flask.Flask(__name__)
Sio = flask_socketio.SocketIO(App, cors_allowed_origins=["http://localhost:3000", "http://localhost:3333"])

Sio.on("session_connexion")(SocketHandler.session_connexion)
Sio.on("lock_answer")(SocketHandler.lock_answer)
Sio.on("start_session")(SocketHandler.start_session)
Sio.on("new_question")(SocketHandler.new_question)
Sio.on("show_answer")(SocketHandler.show_answer)
Sio.on("send_answer")(SocketHandler.send_answer)
Sio.on("delete_session")(SocketHandler.delete_session)

App.after_request(CorsHandler.after_request_func)


Db = ConnectionHandler.initiate(Dotenv.getenv("DB_TYPE"))
QueryBuilder = Model.Model(Db)


SocketHandler.sio = Sio
SocketHandler.query_builder = QueryBuilder

param = {
    "database": Db,
    "query_builder": QueryBuilder,
    "request": flask.request,
    "sio": Sio
}

current_filepath = __file__.replace("\\", "/")
current_dirname = os.path.dirname(current_filepath)

RoutesImporter.import_route(current_dirname, f"{current_dirname}/Routes", "/", App, param, os.path.basename(__file__))


# ---------------------
# TODO : Supprimer ? Sert le côté client lorsqu'il est compilé.
serve_app = ['/', '/manager', '/login', '/register', '/manager/questions', '/manager/etiquettes']


def a():
    return flask.send_from_directory('Static', 'index.html')


for url in serve_app:
    App.route(url)(a)


@App.route('/assets/<name>')
def b(name):
    return flask.send_from_directory('Static/assets', name)


# App.run(port=3333)
Sio.run(App, port=3333)
