import BDD.Model as Model


def createReponse(query_builder: Model.Model, body: str, valide: bool, question_id: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une réponse.

    :param database: Objet base de données
    :param body: Corps de la réponse
    :param valide: Si la réponse est juste ou pas
    :param question_id: Id de la question concernée
    :param commit: Si la fonction doit sauvegarder les changements
    """

    params = {
        "body": body,
        "valide": valide,
        "question_id": question_id
    }

    return query_builder.table("reponses", "insert").where(params).execute(commit=commit)
