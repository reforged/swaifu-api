import json

import BDD.Model as Model


def createQuestion(query_builder: Model.Model, label: str, slug: str, enonce: str, q_type: str, user_id: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une question.

    :param query_builder: Objet Model
    :param label: Label de la question
    :param slug: Identifiant textuel de la question
    :param enonce: Enonce de la question
    :param user_id: Id du créateur de la question
    :param q_type: Type de la question (qcm | libre)
    :param commit: Si la fonction doit sauvegarder les changements
    """

    # On sérialise l'énoncé
    params = {
        "label": label,
        "slug": slug,
        "enonce": (json.dumps(enonce)).replace("'", '"'),
        "type": q_type,
        "user_id": user_id
    }

    return query_builder.table("questions", "insert").where(params).execute(commit=commit)
