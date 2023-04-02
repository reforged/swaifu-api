from Sockets.Session import Session
from BDD.Model import Model
import flask_socketio


def JoinSuccessful(data: dict[str, any], query_builder: Model, liste_session: list[Session], sio: flask_socketio.SocketIO):
    session_id = data.get("session", {}).get("id")
    code_salle = data.get("session", {}).get("code")
    user_id = data["user"].get("id")

    for value in [session_id, user_id]:
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

    if len(query_builder.table("su").where("id", found.session_id).where("user_id", user_id).execute()) == 0:
        query_builder.table("su", "insert").where("user_id", user_id).where("session_id", found.session_id).execute()

        sio.emit("UserJoinSession", {"session": {"users": liste_utilisateurs}}, broadcast=True)

    to_send = {
        "session": {
            "users": liste_utilisateurs,
            "question": found.questionActuelle()
        },
        "waiting": False,
        "locked": False
    }

    return sio.emit("JoinSuccessful", to_send, broadcast=True)

