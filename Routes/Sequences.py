import BDD.Database as Database

import Utils.Handlers.SequenceHandler as SequenceHandler
import Utils.Handlers.QuestionSequenceHandler as QuestionSequenceHandler
import Utils.Handlers.SessionHandler as SessionHandler
import Utils.Handlers.QuestionSequenceUserHandler as QuestionSequenceUserHandler
import Utils.Handlers.UserResponseHandler as UserResponseHandler


# TODO: Marche ??
def getAllSequences(database: Database.Database):
    sequences = SequenceHandler.getAllSequences(database)

    for sequence in sequences:
        sequence["questions"] = QuestionSequenceHandler.getQuestionBySequenceId(database, sequence["id"])
        sequence["sessions"] = SessionHandler.getSessionsBySequenceId(database, sequence["id"])

        for session in sequence["sessions"]:
            session["reponses"] = QuestionSequenceUserHandler.getQuestionSequenceUserBySessionId(database, session["id"])

            for reponse in session["reponses"]:
                resp = UserResponseHandler.getUserResponseByQSUId(reponse["id"])

                reponse["body"] = resp["body"]
                reponse["valide"] = resp["valide"]

                del reponse["user_id"]

    return sequences
