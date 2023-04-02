from Sockets.Session import Session
from BDD.Model import Model
import flask_socketio

import json


def StartSession(data: dict[str, any], query_builder: Model, liste_session: list[Session], sio: flask_socketio.SocketIO):
    session_id = data.get("session", {}).get("id")
    code_salle = data.get("session", {}).get("code")

    for value in [session_id]:
        if value is None:
            return sio.emit("error", {"message": "Valeurs manquantes", "code": code_salle})

    found = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session
            break

    if found is None:
        return sio.emit("error", {"message": "Session non trouvée", "code": code_salle})

    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname", "users.created_at",
                   "users.updated_at"]
    liste_utilisateurs = query_builder.table("sessions").select(*info_wanted).where("id", found.session_id).load("users")[0].export()["users"]

    session = query_builder.table("sessions").where("id", found.session_id).load("sequence")[0].export(convert=True)
    session["sequence"]["questions"] = found.liste_questions

    session["users"] = liste_utilisateurs
    session["question"] = found.questionActuelle()

    to_send = {
        "session": session,
        "waiting": False,
        "locked": False
    }

    print("DEBUT SESSION : ", json.dumps(to_send, default=str))

    sio.emit("StartSession", to_send, broadcast=True)
