import flask_socketio
import Sockets.Session as Session


def delete_session(data, liste_session):
    print("DELETE SESSION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    del found

    flask_socketio.emit("session_deleted", broadcast=True)
