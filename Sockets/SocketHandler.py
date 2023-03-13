import flask
import flask_socketio

import Session

listeDeSession: dict[str, Session.Session] = {}
socket: flask_socketio.SocketIO = None


def addSession(database, sequence_id):
    if socket is None:
        return

    session_cree = Session.Session(database, sequence_id, socket)

    listeDeSession[session_cree.code] = session_cree


# start_diffuse
def start_diffuse(code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.envoiQuestions()


# accept_answers
def accept_answers(code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.affichage()


def nouvelle_reponse(user_id, reponse, code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.nouvelleReponse(user_id, reponse)


# reject_answers
def reject_answers(code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.finDiffusion()


# display_answers
def display_answers(code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.affichage()


# end_scene
def end_scene(code):
    session = listeDeSession.get(code)

    if session is None:
        return

    session.questionSuivante()


def subscribeFunctions(sio: flask_socketio.SocketIO):
    global socket
    socket = sio

    for func in [start_diffuse, accept_answers, reject_answers, display_answers, end_scene]:
        socket.event(func)




