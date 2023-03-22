import flask

import BDD.Model as Model

import Utils.Route as Route

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.SequenceHandler as SequenceHandler


@Route.route("POST")
def createSequence(query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../sequences/<sequence_id> - Méthode POST

    Permet à un utilisateur de récupérer une séquence en fonction de son id.

    Nécessite d'être connecté

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    data = request.get_json()

    label: str = data.get("label")
    questions: list[str] = data.get("questions")

    # Vérification de la bonne présence des données
    for valeur in [label, questions]:
        if valeur is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    sequence_id = SequenceHandler.addSequence(query_builder, label, questions)

    # Il est plus simple de juste créer une requête pour récupérer ce que nous venons de créer, puisque nous souhaitons
    # Egalement charger les questions
    res = query_builder.table("sequences").where("id", sequence_id).load("questions")[0]

    return res.export()
