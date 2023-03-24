import json

import BDD.Model as Model

import Utils.Types as Types

import Permissions.Policies as Policies


@Policies.middleware(["store:question"], ["update:question"], ["destroy:question"])
def questions(query_builder: Model.Model) -> list[Types.dict_ss_imb]:
    """
    Gère la route .../questions - Méthode GET

    Permet de récupérer toutes les questions sur le serveur ainsi que leurs étiquettes et réponses.

    :param query_builder: Objet Model
    """

    liste_questions = query_builder.table("questions").execute(False, False)
    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname",
                   "users.created_at", "users.updated_at"]

    # Pour chaque question, on charge les étiquettes, les réponses ainsi que le créateur de la question
    for question in liste_questions:
        question.load("etiquettes")
        question.load("reponses")
        # On ne récupère pas le mot de passe...
        question.load("user", query_builder.select(*info_wanted))

    res = [row.export() for row in liste_questions]

    for question in res:
        # Pour chaque question il faut également désérialiser l'énoncé
        question["enonce"] = json.loads(question["enonce"])

    return res
