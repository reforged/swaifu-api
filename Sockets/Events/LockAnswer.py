from Sockets.Session import Session
import flask_socketio


def LockAnswer(data: dict[str, any], liste_session: list[Session], sio: flask_socketio.SocketIO):
    session_id = data.get("session", {}).get("id")
    code_salle = data.get("session", {}).get("code")
    lock = data.get("locked", True)

    print("Lock answer - received data : ", data)

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

    sio.emit("LockAnswer", {"session": data["session"], "locked": lock}, broadcast=True)
