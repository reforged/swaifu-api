import flask

import flask_socketio
import BDD.Model as Model

import Permissions.Policies as Policies

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Sockets.SocketHandler as SocketHandler

import Utils.Route as Route

import json


@Policies.middleware(["store:session"])
@Route.route(method="POST")
def createSession(query_builder: Model.Model, request: flask.Request, sio: flask_socketio.SocketIO):
    """
    Gère la route .../sessions/create - Méthode POST

    Permet à un utilisateur de créer une nouvelle session.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    :param sio: Objet SocketIO
    """

    # Récupération du token
    token: dict[str, str] = Policies.check_token(request, query_builder)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data = request.get_json()

    sequence_id = data.get("sequence")

    # On s'assure de la bonne existence des données
    for value in [sequence_id]:
        if value is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    if len(query_builder.table("sequences").where("id", sequence_id).execute()) == 0:
        return flask.make_response({"Error": "Sequence not found"}, 404)

    sock = SocketHandler.createSession(sequence_id, query_builder, sio)

    session_id = query_builder.table("sessions", "insert").where("sequence_id", sequence_id).where("code", sock.code).execute()

    sock.session_id = session_id

    res = query_builder.table("sessions").where("id", session_id).load("sequence", None, "questions", "reponses")

    res = res[0]
    res = res.export(True)

    res["status"] = "wait"
    res["users"] = []
    
    for question in res["sequence"]["questions"]:
        question["enonce"] = json.loads(question["enonce"])

    print("!! : ", json.dumps(res))

    return res
