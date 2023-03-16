import flask

import BDD.Database as Database

import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Handlers.SequenceHandler as SequenceHandler


def createSequence(database: Database.Database, request: flask.Request):
    data = request.get_json()

    label: str = data.get("label")
    questions: list[str] = data.get("questions")

    for valeur in [label, questions]:
        if valeur is None:
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

    return SequenceHandler.addSequence(database, label, questions)
