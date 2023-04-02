from Sockets.Session import Session
import flask_socketio

import json


def NewAnswer(data: dict[str, any], liste_session: list[Session], sio: flask_socketio.SocketIO, query_builder):
    print(f"New answer : {json.dumps(data)}")

    session_id = data.get("session", {}).get("id")
    code_salle = data.get("session", {}).get("code")
    user_id = data["user"].get("id")

    reponse = data.get("reponse", "")

    for value in [session_id, reponse, user_id]:
        if value is None:
            return sio.emit("error", {"message": "Valeurs manquantes", "code": code_salle})

    found = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session
            break

    found.addAnswers([reponse], user_id)

    session = query_builder.table("sessions").where("id", found.session_id).load("sequence", None, "questions", "reponses")[0].export(convert=True)

    session["question"] = found.questionActuelle()

    to_send = {
        "session": session,
        "reponses": found.reponsesCourantes(),
        "waiting": True,
        "locked": False,
        "message": "Réponse enregistré"
    }

    sio.emit("ResponseOfAnswerSending", to_send)

    return sio.emit("NewAnswer", to_send, broadcast=True)
