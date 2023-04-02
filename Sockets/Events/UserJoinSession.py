from Sockets.Session import Session
from BDD.Model import Model
import flask_socketio


def UserJoinSession(data: dict[str, any], query_builder: Model, liste_session: list[Session], sio: flask_socketio.SocketIO):
    found = None
    code_salle = data["session"].get("code")
    user_id = data["user"].get("id")

    if code_salle is None or user_id is None:
        return sio.emit("error", {"message": "Valeurs manquantes", "code": code_salle})

    for session in liste_session:
        if session.code == code_salle:
            found = session
            break

    if found is None:
        return sio.emit("error", {"message": "Session non trouvée", "code": code_salle})

    if len(query_builder.table("su").where("id", found.session_id).where("user_id", user_id).execute()) == 0:
        query_builder.table("su", "insert").where("user_id", user_id).where("session_id", found.session_id).execute()

    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname", "users.created_at",
                   "users.updated_at"]
    liste_utilisateurs = query_builder.table("sessions").select(*info_wanted).where("id", found.session_id).load("users")[0].export()["users"]

    return sio.emit("UserJoinSession", {"session": {"users": liste_utilisateurs}})
