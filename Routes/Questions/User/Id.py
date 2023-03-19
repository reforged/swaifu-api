import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Handlers.ReponseHandler as ReponseHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(url='<user_id>')
def user(user_id: str, database: Database.Database) -> list[Types.dict_ss_imb]:
    user_questions: list[Types.dict_ss_imb] = QuestionHandler.getQuestionByCreatorUuid(database, user_id)

    for question in user_questions:
        question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, question["id"])
        question["reponses"] = ReponseHandler.getReponses(database, question['id'])

    return user_questions
