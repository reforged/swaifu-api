import flask

import BDD.Database as Database

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Permissions.Policies as Policies

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Handlers.ReponseHandler as ReponseHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(method="POST")
def questions_create(database: Database.Database, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../questions/create - Méthode POST

    Permet à un utilisateur de créer une question.

    Nécessite d'être connecté.

    :param database: Objet base de données
    :param request: Objet Request de flask
    """

    token: dict[str, str] = Policies.check_token(request, database)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data: Types.new_que = request.get_json()

    label: str = data.get("label")
    slug: str = data.get("slug")
    enonce: str = data.get("enonce")
    q_type: str = data.get("type")
    reponses: list[dict[str, str]] = data.get("reponses")
    etiquettes: list[dict[str]] = data.get("etiquettes")
    user_id: str = token.get('id')

    if None in [label, enonce, q_type, user_id, reponses, etiquettes]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    question_id: str = QuestionHandler.createQuestion(database, label, slug, enonce, q_type, user_id, False)
    data["id"] = question_id

    for reponse in reponses:
        body: str = reponse.get("body")
        valide: str = reponse.get("valide")

        if None in [body, valide]:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

        reponse_id = ReponseHandler.createReponse(database, body, bool(valide), question_id, False)
        reponse["id"] = reponse_id

    error_message = {"errors": []}
    i = 0

    for etiquette in etiquettes:
        if len(EtiquetteHandler.getEtiquetteByUuid(database, etiquette["id"])) == 0:
            error_message["errors"].append({
                "rule": "exists",
                "field": f"etiquette.{i}",
                "message": "exists validation failure"
            })

            i += 1

    if len(error_message["errors"]) > 0:
        database.rollback()
        return flask.make_response("Exists validation failure", 422, error_message)
       
    for etiquette in etiquettes:
        EtiquetteHandler.joinEtiquetteQuestion(database, question_id, etiquette["id"], False)

    # Commit à la toute fin en cas d'erreurs
    database.commit()

    return data
