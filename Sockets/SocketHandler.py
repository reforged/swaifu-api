import Sockets.Session as Session
import flask
import flask_socketio
from flask_socketio import SocketIO
import BDD.Model as Model
import json
import pprint

liste_session: list[Session] = []
sio: SocketIO = None
query_builder: Model.Model
req = flask.Request


def session_connexion(data):
    print("SESSION REJOINTE : ", data.get("code"))
    user = data.get("user", {})
    user_id = user.get("id")
    code = data.get("code")

    for value in [user, code]:
        if value is None:
            return flask_socketio.emit("error", {"message": "Valeurs manquantes", "code": code})

    found: Session.Session = None

    for session in liste_session:
        if session.code == code:
            found = session

    if found is None or found.lock:
        return flask_socketio.emit("error", {"message": "Cannot connect", "code": code})

    query_builder.table("su", "insert").where("session_id", found.session_id).where("user_id", user_id).execute()

    session = query_builder.table("sessions").where("id", found.session_id).load("sequence", None, "questions", "reponses")[0]

    session.load("users")
    session = session.export(True)
    session["reponses"] = []
    session["status"] = "wait"

    print("Session id : ", found.session_id)
    print(f"Sending : {session}")
    flask_socketio.emit("new_user", {"session": session}, broadcast=True)

    if found is None:
        return sio.emit("error", {"message": "Session non existante"})

    user = query_builder.table("users").where("id", user_id).execute()

    if len(user) == 0:
        return sio.emit("error", {"message": "Utilisateur non trouvé"})

    return


def lock_answer(data):
    print("QUESTION VEROUILLE")
    flask_socketio.emit("lock_answer", {"session": data.get("session"), "locked": data.get("locked")})


def start_session(data):
    print("START SESSION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    found.lock = True

    session = query_builder.table("sessions").where("id", session_id).load("sequence", None, "questions", "reponses")[0]
    session = session.export(True)
    session["status"] = "starting"

    # session["sequence"]["questions"] = [json.loads(row["enonce"]) for row in session["sequence"]["questions"]]

    for question in session["sequence"]["questions"]:
        question["enonce"] = json.loads(question["enonce"])

    question = found.questionActuelle()

    print(f"question : {question}")

    session["questionId"] = question["id"]

    res = query_builder.table("questions").where("id", question["id"]).load("reponses")[0]
    res = res.export(True)

    res["enonce"] = json.loads(res["enonce"])

    session["question"] = res

    send = {
        "session": session,
        "question": res
    }

    print(f"Send : {json.dumps(send)}")

    flask_socketio.emit("start_session", send, broadcast=True)


def new_question(data):
    print("NEW QUESTION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    found.questionSuivante()

    session = query_builder.table("sessions").where("id", session_id).execute(export=False)[0]
    session = session.export(True)

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute(export=False)
    question["reponses"] = [row.export(True) for row in question["reponses"]]

    session["questionId"] = question["id"]
    session["question"] = question

    sequence = query_builder.table("sequences").where("id", session["sequence_id"]).execute(export=False)[0]
    sequence = sequence.export(True)
    session["sequence"] = sequence

    send = {
        "session": session,
        "question": question
    }

    print(f"Data : {json.dumps(send)}")

    flask_socketio.emit("new_question", send, broadcast=True)


def show_answer(data):
    print("SHOW ANSWERS")
    session_id = data.get("sessions").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    session = query_builder.table("sessions").where("id", session_id).load("reponses", None, "question")[0]
    session = session.export()

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute()

    session["question"] = question

    send = {
        "session": session,
        "reponses": question
    }

    flask_socketio.emit("show_answer", send, broadcast=True)


def send_answer(data):
    print("ANSWER SENT")
    session_id = data.get("session").get("id")
    user_id = data.get("user_id")
    question_id = data.get("question_id")

    reponsesss: data.get("reponses")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    session = query_builder.table("sessions").where("id", session_id).execute()

    reponse = []

    for reponse in reponsesss:
        reponse.append(query_builder.table("reponses").where("id", reponse["id"]).execute())

    for reponse in reponsesss:
        query_builder.table("reponse_user", "delete").where("user_id", user_id).where("session_id", session_id).execute()

        params = {
            "body": reponse["body"],
            "valide": True,
            "user_id": user_id,
            "session_id": session_id,
            "question_id": question_id
        }

        query_builder.table("reponse_user", "insert").where(params).execute()

    session = query_builder.table("sessions").where("id", session_id).load("users")[0]
    session = session.export()

    res = query_builder.table("sequences").where("id", found.sequence_id).load("questions", "reponses")
    session["sequence"] = [row.export() for row in res]

    res = query_builder.table("reponse_user").where("session_id", session_id).load("question")
    session["reponses"] = [row.export() for row in res]

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute()

    flask_socketio.emit('response_of_answer_sending', {"message": "Réponse enregistrée !", "session": session, "waiting": True})

    flask_socketio.emit("update_answers", {"session", session})


def delete_session(data):
    print("DELETE SESSION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    del found

    flask_socketio.emit("session_deleted", broadcast=True)


def createSession(sequence_id: str, query_builder, sio) -> Session.Session:
    temp = (Session.Session(query_builder, sequence_id, sio))
    liste_session.append(temp)

    return temp
