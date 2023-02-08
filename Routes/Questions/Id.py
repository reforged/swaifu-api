import BDD.Database as Database

import Utils.EtiquetteHandler as EtiquetteHandler
import Utils.QuestionHandler as QuestionHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(url="<question_id>")
def getQuestionByUuid(question_id: str, database: Database.Database) -> Types.dict_ss_imb:
    # TODO: user_id not question_id ??
    queried_question: Types.dict_ss_imb = QuestionHandler.getQuestionByUuid(database, question_id)[0]

    queried_question["etiquettes"] = EtiquetteHandler.getEtiquettesByQuestionId(database, queried_question["id"])

    return queried_question


@Route.route(method="put", url="<question_id>")
def putByUuid(question_id: str, database: Database.Database):
    # TODO: Savoir quelle données sont données
    pass


@Route.route(method="delete", url="<question_id>")
def deleteByUuid(question_id: str, database: Database.Database) -> dict[str, str]:
    EtiquetteHandler.removeEtiquette(database, question_id)

    return {"Message": "yes"}
