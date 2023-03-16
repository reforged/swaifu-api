import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Handlers.ReponseHandler as ReponseHandler
import Utils.Types as Types


def questions(database: Database.Database) -> list[Types.dict_ss_imb]:
    liste_questions = QuestionHandler.getAllQuestions(database)

    for question in liste_questions:
        question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, question['id'])
        question["reponses"] = ReponseHandler.getReponses(database, question['id'])

    return liste_questions
