import flask_socketio
import json
import Sockets.Session as Session


def session_connexion(data, liste_session, query_builder, sio):
    print("SESSION REJOINTE : ", data.get("code"))
    print("Received : ", json.dumps(data))
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

    if found is None:
        return flask_socketio.emit("error", {"message": "Session non trouvée"})

    users = query_builder.table("sessions").where("id", found.session_id).load("users")[0]
    users = users.export(True)["users"]

    known_user = False

    for user in users:
        if user["id"] == user_id:
            known_user = True

    if not known_user and not found.lock:
        query_builder.table("su", "insert").where("session_id", found.session_id).where("user_id", user_id).execute()

    session = query_builder.table("sessions").where("id", found.session_id).load("sequence", None, "questions", "reponses")[0]

    session.load("users")
    session = session.export(True)
    session["reponses"] = []

    for question in session["sequence"]["questions"]:
        question["enonce"] = json.loads(question["enonce"])

    if not found.lock:
        session["status"] = "wait"
    else:
        session["status"] = "starting"

    print("Session id : ", found.session_id)
    print("Users : ", session["users"])

    for user in session["users"]:
        if user["id"] == user_id:
            known_user = True

    if found is None or (found.lock and not known_user):
        return flask_socketio.emit("error", {"message": "Cannot connect", "code": code})

    if found.lock:
        session["questionId"] = found.questionActuelle()["id"]
        session["question"] = query_builder.table("questions").where("id", session["questionId"]).load("reponses")[0]
        session["question"] = session["question"].export(True)
        session["question"]["enonce"] = json.loads(session["question"]["enonce"])

    print(f"Sending : {json.dumps(session)}")

    flask_socketio.emit("new_user", {"session": session}, broadcast=True)

    user = query_builder.table("users").where("id", user_id).execute()

    if len(user) == 0:
        return sio.emit("error", {"message": "Utilisateur non trouvé"})

    return