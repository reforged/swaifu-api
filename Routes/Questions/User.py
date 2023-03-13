import BDD.Database as Database

import Utils.EtiquetteHandler as EtiquetteHandler
import Utils.QuestionHandler as QuestionHandler
import Utils.ReponseHandler as ReponseHandler
import Utils.Route as Route
import Utils.Types as Types
import Utils.HandleUser as UserHandler


@Route.route(url='user/<user_numero>')
def user(user_numero: str, database: Database.Database) -> list[Types.dict_ss_imb]:
    user_id: str = UserHandler.getUserByNumero(database, user_numero)["id"]

    user_questions: list[Types.dict_ss_imb] = QuestionHandler.getQuestionByCreatorUuid(database, user_id)

    for question in user_questions:
        question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, question["id"])
        question["reponses"] = ReponseHandler.getReponses(database, question['id'])

    return user_questions
