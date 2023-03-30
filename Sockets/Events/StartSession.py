import Sockets.Session as Session
import json
import flask_socketio


def start_session(data, liste_session, query_builder):
    print("START SESSION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    found.lock = True

    session = query_builder.table("sessions").where("id", session_id).load("sequence", None, "questions", "reponses")[0]
    session.load("users")
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