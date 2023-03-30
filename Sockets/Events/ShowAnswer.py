import flask_socketio
import Sockets.Session as Session
import json


def show_answer(data, liste_session, query_builder):
    print("SHOW ANSWERS")
    print("Data session : ", data)
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    session = query_builder.table("sessions").where("id", session_id).load("reponses", None, "question")[0]
    session = session.export()

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute()

    session["question"] = question

    send = {
        "session": session,
        "reponses": question
    }

    send = json.loads(json.dumps(send, default=str))

    flask_socketio.emit("show_answer", send, broadcast=True)
