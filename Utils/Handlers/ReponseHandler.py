import uuid
import datetime

import BDD.Database as Database
import BDD.Model as Model


# TODO: SUPPRIMER
def getReponses(database: Database.Database, question_id: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir toutes les réponses à une
    question en fonction de son id.

    :param database: Objet base de données
    :param question_id: Id de la question concernée
    """

    sql_etiquette_query = {
        "where": [
            ["reponses", "question_id", question_id]
        ],
        "from": {
            "tables": ["reponses"]
        }
    }

    return database.query(sql_etiquette_query)


def createReponse(query_builder: Model.Model, body: str, valide: bool, question_id: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une réponse.

    :param database: Objet base de données
    :param body: Corps de la réponse
    :param valide: Si la réponse est juste ou pas
    :param question_id: Id de la question concernée
    :param commit: Si la fonction doit sauvegarder les changements
    """

    reponse_id: str = str(uuid.uuid4())

    while len(query_builder.table("reponses").where("id", reponse_id).execute()) > 0:
        reponse_id = str(uuid.uuid4())

    params = {
        "id": reponse_id,
        "body": body,
        "valide": valide,
        "question_id": question_id,
        "created_at": datetime.datetime.now().astimezone(),
        "updated_at": datetime.datetime.now().astimezone()
    }

    query_builder.table("reponses", "insert").where(params).execute(commit=commit)

    return reponse_id
