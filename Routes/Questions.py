import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Handlers.ReponseHandler as ReponseHandler

import Utils.Types as Types


def questions(database: Database.Database) -> list[Types.dict_ss_imb]:
    # TODO : Implémenter correctement (Connection et ne peut tout voir)
    """
    Gère la route .../questions - Méthode GET

    Permet de récupérer toutes les questions sur le serveur ainsi que leurs étiquettes et réponses.

    :param database: Objet base de données
    """

    liste_questions = QuestionHandler.getAllQuestions(database)

    for question in liste_questions:
        question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, question['id'])
        question["reponses"] = ReponseHandler.getReponses(database, question['id'])

    return liste_questions
