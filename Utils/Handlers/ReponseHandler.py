import uuid
import datetime

import BDD.Database as Database


def getReponseByUuid(database: Database.Database, reponse_id: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir une réponse par son id.

    :param database: Objet base de données
    :param reponse_id: Id de la réponse concernée
    """

    get_reponse = {
        "where": [
            ["reponses", "id", reponse_id]
        ],
        "from": {
            "tables": ["reponses"]
        }
    }

    return database.query(get_reponse)


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


def createReponse(database: Database.Database, body: str, valide: bool, question_id: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une réponse.

    :param database: Objet base de données
    :param body: Corps de la réponse
    :param valide: Si la réponse est juste ou pas
    :param question_id: Id de la question concernée
    :param commit: Si la fonction doit sauvegarder les changements
    """

    reponse_id: str = str(uuid.uuid4())

    while len(getReponseByUuid(database, reponse_id)) > 0:
        reponse_id = str(uuid.uuid4())

    insert_reponse_query = {
        "table": "reponses",
        "action": "insert",
        "valeurs": [
            ["id", reponse_id],
            ["body", body],
            ["valide", valide],
            ["question_id", question_id],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_reponse_query)

    if commit:
        database.commit()

    return reponse_id
