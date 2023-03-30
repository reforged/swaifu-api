import Sockets.Session as Session
import json
import flask_socketio


def new_question(data, liste_session, query_builder):
    print("NEW QUESTION")
    session_id = data.get("session").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    found.questionSuivante()

    session = query_builder.table("sessions").where("id", session_id).load("users")[0]
    session = session.export(True)

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute(export=False)
    question["reponses"] = [row.export(True) for row in question["reponses"]]

    session["questionId"] = question["id"]
    session["question"] = question
    session["status"] = "starting"

    sequence = query_builder.table("sequences").where("id", session["sequence_id"]).execute(export=False)[0]
    sequence = sequence.export(True)
    session["sequence"] = sequence

    send = {
        "session": session,
        "question": question
    }

    print(f"Data : {json.dumps(send)}")

    flask_socketio.emit("new_question", send, broadcast=True)