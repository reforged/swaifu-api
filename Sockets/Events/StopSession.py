from Sockets.Session import Session
import flask_socketio


def StopSession(data: dict[str, any], liste_session: list[Session], sio: flask_socketio.SocketIO):
    print("Session ended")
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

    del found

    sio.emit("StopSession", data.get("session"), broadcast=True)
