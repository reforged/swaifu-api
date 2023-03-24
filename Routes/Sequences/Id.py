import flask
import json
import datetime

import BDD.Model as Model

import Utils.Route as Route

import Permissions.Policies as Policies


@Policies.middleware(["update:sequence"])
@Route.route(url="<sequence_id>")
def getSequenceById(sequence_id: str, query_builder: Model.Model):
    """
    Gère la route .../sequences/<sequence_id> - Méthode GET

    Permet à un utilisateur de récupérer une séquence en fonction de son id.

    :param sequence_id: Id de la séquence désirée
    :param query_builder: Objet Model
    """

    # None puisque nous ne souhaitons limiter les colonnes récupérées
    res = query_builder.table("sequences").where("id", sequence_id).load("questions", None, "reponses")

    if len(res) == 0:
        return flask.make_response({"Error": "Sequence not found"}, 404)

    res = res[0].export()

    # Pour chaque question chargée, nous souhaitons également charger correctement les énoncés
    for question in res.get("questions", []):
        question["enonce"] = json.loads(question["enonce"])

    return res


@Policies.middleware(["update:sequence"])
@Route.route("PUT", "<sequence_id>")
def putBySequenceId(sequence_id: str, query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../sequences/<sequence_id> - Méthode PUT

    Permet à un utilisateur de modifier une séquence en fonction de son id.

    :param sequence_id: Id de la séquence désirée
    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    old = query_builder.table("sequences").where("id", sequence_id).execute()

    if len(old) == 0:
        return flask.make_response({"Error": "Séquence non trouvée"}, 404)

    # Nous récupérons une liste, au lieu de l'unique élément souhaité
    old = old[0]

    data = request.get_json()

    # On ne fait bien sûr pas confiance à l'utilisateur pour le champ updated_at
    new_val = {
        "updated_at": datetime.datetime.now().astimezone()
    }

    for key in ["label"]:
        if old.get(key) != data.get(key):
            if data.get(key) is not None:
                new_val[key] = data.get(key)

    query_builder.table("sequences", "alter", sequence_id).where(new_val).execute()

    return {"Message": "Succès"}


@Policies.middleware(["destroy:sequence"])
@Route.route("DELETE", "<sequence_id>")
def deleteSequenceById(sequence_id: str, query_builder: Model.Model):
    """
    Gère la route .../sequences/<sequence_id> - Méthode DELETE

    Permet à un utilisateur de supprimer une séquence en fonction de son id.

    :param sequence_id: Id de la séquence désirée
    :param query_builder: Objet Model
    """

    query_builder.table("sequences", "delete").where("id", sequence_id).execute()

    return {"message": "Supprimé avec succès"}
