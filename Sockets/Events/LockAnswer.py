import flask_socketio


def lock_answer(data):
    print("QUESTION VEROUILLE")
    flask_socketio.emit("lock_answer", {"session": data.get("session"), "locked": data.get("locked")})
