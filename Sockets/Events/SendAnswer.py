import uuid
import json
import flask_socketio
import Sockets.Session as Session


def send_answer(data, liste_session, query_builder):
    print("ANSWER SENT")
    print("Data : ", json.dumps(data))
    session_id = data.get("session").get("id")
    user_id = data.get("user").get("id")
    question_id = data.get("question").get("id")

    found: Session.Session = None

    for session in liste_session:
        if session.session_id == session_id:
            found = session

    session = query_builder.table("sessions").where("id", session_id).execute()

    reponse = data.get("reponse")

    query_builder.table("reponse_user", "delete").where("user_id", user_id).where("session_id", session_id).execute()

    reponse_uuid = str(uuid.uuid4())

    while len(query_builder.table("reponse_user").where("id", reponse_uuid).execute()) != 0:
        reponse_uuid = str(uuid.uuid4())

    params = {
        "id": reponse_uuid,
        "body": reponse["body"],
        "valide": True,
        "user_id": user_id,
        "session_id": session_id,
        "question_id": question_id
    }

    query_builder.table("reponse_user", "insert").where(params).execute()

    session = query_builder.table("sessions").where("id", session_id).load("users")[0]
    session = session.export(True)

    res = query_builder.table("sequences").where("id", found.sequence_id).load("questions", None, "reponses")
    session["sequence"] = [row.export(True) for row in res]
    session["statut"] = "starting"

    res = query_builder.table("reponse_user").where("session_id", session_id).load("question")
    session["reponses"] = [row.export(True) for row in res]

    question = found.questionActuelle()
    question["reponses"] = query_builder.table("reponses").where("question_id", question["id"]).execute(export=False)
    question["reponses"] = [row.export(True) for row in question["reponses"]]

    session["questionId"] = question["id"]
    session["question"] = question

    print("Session : ", json.dumps(session))

    flask_socketio.emit('response_of_answer_sending', {"message": "Réponse enregistrée !", "session": session, "waiting": True})

    flask_socketio.emit("update_answers", {"session": session})