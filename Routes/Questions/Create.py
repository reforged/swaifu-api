import flask

import BDD.Model as Model

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Permissions.Policies as Policies

import Utils.Handlers.QuestionHandler as QuestionHandler
import Utils.Handlers.ReponseHandler as ReponseHandler
import Utils.Route as Route
import Utils.Types as Types


@Route.route(method="POST")
def questions_create(query_builder: Model.Model, request: flask.Request) -> Types.func_resp:
    """
    Gère la route .../questions/create - Méthode POST

    Permet à un utilisateur de créer une question.

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    # Obtention de l'id du créateur
    token: dict[str, str] = Policies.check_token(request, query_builder)

    if token is None:
        return flask.make_response(HttpErreurs.token_invalide, 400, HttpErreurs.token_invalide)

    data = request.get_json()

    label: str = data.get("label")

    slug = label.lower().replace(" ", "-")

    enonce: str = data.get("enonce")
    q_type: str = data.get("type")
    reponses: list[dict[str, str]] = data.get("reponses")
    etiquettes: list[str] = data.get("etiquettes")
    user_id: str = token.get('id')

    if None in [label, enonce, q_type, user_id, reponses, etiquettes]:
        return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    question_id: str = QuestionHandler.createQuestion(query_builder, label, slug, enonce, q_type, user_id, False)
    data["id"] = question_id
    data["user_id"] = user_id

    # Vérification du bon format pour les réponses avant le début des transactions
    for reponse in reponses:
        body: str = reponse.get("body")
        valide: str = reponse.get("valide")

        if None in [body, valide]:
            # En cas d'erreurs, on rollback et on pleure au client
            query_builder.rollback()
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

        # Sinon on ajoute la réponse
        reponse_id = ReponseHandler.createReponse(query_builder, body, bool(valide), question_id, False)
        reponse["id"] = reponse_id

    error_message = {"errors": []}
    i = 0

    # Puisque toutes les étiquettes sont censées exister, on vérifie cela, et en cas de non-existence,
    # On soulève une erreur et on annule, plutôt que de la créer silencieusement
    for etiquette_id in etiquettes:
        if len(query_builder.table("etiquettes").where("id", etiquette_id).execute()) == 0:
            error_message["errors"].append({
                "rule": "exists",
                "field": f"etiquette.{i}",
                "message": "exists validation failure"
            })

            i += 1

    # S'il y a une erreur on rollback et on soulève l'erreur
    if len(error_message["errors"]) > 0:
        query_builder.rollback()
        return flask.make_response("Exists validation failure", 422, error_message)

    # Sinon on lie la question et l'étiquette en cas de succès
    for etiquette_id in etiquettes:
        query_builder.table("etiquette_question", "insert").where("etiquette_id", etiquette_id).where("question_id", question_id).execute(commit=False)

    # Commit à la toute fin en cas d'erreurs
    query_builder.commit()

    data["user"] = query_builder.table("users").where('id', data["user_id"]).execute()[0]

    return data
