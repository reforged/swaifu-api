import flask

import BDD.Database as Database

import Erreurs.HttpErreurs as HttpErreurs

import Permissions.Policies as Policies

import Utils.EtiquetteHandler as EtiquetteHandler
import Utils.QuestionHandler as QuestionHandler
import Utils.ReponseHandler as ReponseHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(method="POST")
def questions_create(database: Database.Database, request: flask.Request) -> Types.func_resp:
    token: dict[str, str] = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data: Types.new_que = request.get_json()

    label: str = data.get("label")
    enonce: str = data.get("enonce")
    type: str = data.get("type")
    reponses: list[dict[str, str]] = data.get("reponses")
    etiquettes: str = data.get("etiquettes")
    user_id: str = token.get('id')

    if None in [label, enonce, type, user_id, reponses, etiquettes]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    question_id: str = QuestionHandler.createQuestion(database, label, enonce, user_id, False)

    for reponse in reponses:
        body: str = reponse.get("body")
        valide: str = reponse.get("valide")

        if None in [body, valide]:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

        ReponseHandler.createReponse(database, body, bool(valide), question_id, False)
       
    for etiquette_id in etiquettes:
        EtiquetteHandler.joinEtiquetteQuestion(database, question_id, etiquette_id, False)

    database.commit()

    return {"success": "yes"}
