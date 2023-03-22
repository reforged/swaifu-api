import datetime
import flask
import json

import BDD.Model as Model

import Utils.Route as Route

import Utils.Types as Types


@Route.route(url="<question_id>")
def getQuestionByUuid(question_id: str, query_builder: Model.Model) -> Types.dict_ss_imb:
    """
    Gère la route .../questions/<question_id> - Méthode GET

    Permet à un utilisateur de récupérer une question en fonction de son id.

    :param question_id: Id de la question désirée
    :param query_builder: Objet Model
    """

    # On récupère la question, et on charge les étiquettes, réponses et l'auteur !
    queried_question = query_builder.table("questions").where("id", question_id).load("etiquettes")[0]

    queried_question.load("user")
    queried_question.load("reponses")

    queried_question = queried_question.export()

    # Les énoncés sont du json, nous devons donc désérialiser
    queried_question["enonce"] = json.loads(queried_question["enonce"])

    return queried_question


@Route.route(method="put", url="<question_id>")
def putByUuid(question_id: str, query_builder: Model.Model, request):
    """
    Gère la route .../questions/<question_id> - Méthode PUT

    Permet à un utilisateur de modifier une question en fonction de son id.

    Nécessite d'être connecté.

    :param question_id: Id de la question désirée
    :param query_builder: Objet Model
    """

    old = query_builder.table("questions").where("id", question_id).execute()

    if len(old) == 0:
        return flask.make_response("Question non trouvée", 400, {"Error": "Question non trouvée"})

    old = old[0]

    data = request.get_json()

    # Forcément on met à jour updated_at nous même
    new_val = {
        "updated_at": datetime.datetime.now().astimezone()
    }

    # Pour chaque valeur à mettre à jour
    for key in ["label", "slug", "enonce", "type"]:
        if old.get(key) != data.get(key):
            if data.get(key) is not None:
                new_val[key] = data.get(key)

    # Si nous devons stocker un nouvel énoncé, il faut le sérialiser
    if "enonce" in new_val:
        new_val["enonce"] = (json.dumps(new_val["enonce"])).replace("'", '"')

    query_builder.table("questions", "alter", question_id).where(new_val).execute()

    return {"Message": "Succès"}


@Route.route(method="delete", url="<question_id>")
def deleteByUuid(question_id: str, query_builder: Model.Model) -> dict[str, str]:
    """
    Gère la route .../questions/<question_id> - Méthode DELETE

    Permet à un utilisateur de supprimer une question en fonction de son id.

    Nécessite d'être connecté.

    :param question_id: Id de la question désirée
    :param query_builder: Objet Model
    """

    query_builder.table("questions", "delete").where("id", question_id).execute()

    return {"message": "Supprimé avec succès"}

