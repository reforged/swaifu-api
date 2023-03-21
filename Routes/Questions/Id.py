import BDD.Database as Database

import Utils.Handlers.ReponseHandler as ResponseHandler

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(url="<question_id>")
def getQuestionByUuid(question_id: str, database: Database.Database) -> Types.dict_ss_imb:
    """
    Gère la route .../questions/id - Méthode GET

    Permet à un utilisateur de récupérer une question en fonction de son id.

    :param question_id: Id de la question désirée
    :param database: Objet base de données
    """
    queried_question: Types.dict_ss_imb = QuestionHandler.getQuestionByUuid(database, question_id)[0]

    queried_question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, question_id)
    queried_question["response"] = ResponseHandler.getReponses(database, question_id)

    return queried_question


@Route.route(method="put", url="<question_id>")
def putByUuid(question_id: str, database: Database.Database, request):
    # TODO: Savoir quelle données sont données
    """
    Gère la route .../questions/id - Méthode PUT

    Non implémentée.

    Permet à un utilisateur de modifier une question en fonction de son id.

    Nécessite d'être connecté.

    :param question_id: Id de la question désirée
    :param database: Objet base de données
    """
    data = request.get_json()
    QuestionHandler.alterQuestion(database, data)
    return data


@Route.route(method="delete", url="<question_id>")
def deleteByUuid(question_id: str, database: Database.Database) -> dict[str, str]:
    """
    Gère la route .../questions/id - Méthode DELETE

    Permet à un utilisateur de supprimer une question en fonction de son id.

    Nécessite d'être connecté.

    :param question_id: Id de la question désirée
    :param database: Objet base de données
    """

    QuestionHandler.deleteQuestion(database, question_id)

    return {"message": "Supprimé avec succès"}

