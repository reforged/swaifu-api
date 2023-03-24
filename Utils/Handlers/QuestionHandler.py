import datetime
import uuid
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

    question_id: str = str(uuid.uuid4())

    # On cherche un uuid disponible
    while len(query_builder.table("questions").where("id", question_id).execute()) > 0:
        question_id = str(uuid.uuid4())

    # On sérialise l'énoncé
    params = {
        "id": question_id,
        "label": label,
        "slug": slug,
        "enonce": (json.dumps(enonce)).replace("'", '"'),
        "type": q_type,
        "user_id": user_id,
        "created_at": datetime.datetime.now().astimezone(),
        "updated_at": datetime.datetime.now().astimezone()
    }

    query_builder.table("questions", "insert").where(params).execute(commit=commit)

    return question_id
