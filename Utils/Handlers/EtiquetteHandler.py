import datetime
import uuid

import BDD.Database as Database


def getEtiquetteByUuid(database: Database.Database, etiquette_id: str) -> list[dict]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir une étiquette par son id.

    :param database: Objet base de données
    :param etiquette_id: Id de l'étiquette concernée
    """

    get_etiquette = {
        "where": [
            ["etiquettes", "id", etiquette_id]
        ],
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(get_etiquette)


def getAllEtiquettes(database: Database.Database) -> list[dict]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir toutes les étiquettes.

    :param database: Objet base de données
    """
    etiquette_query = {
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(etiquette_query)


def getEtiquettesByQuestionId(database: Database.Database, question_id: str):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir toutes les étiquettes d'une
    fonction en fonction de son id.

    :param database: Objet base de données
    :param question_id: Id de l'étiquette concernée
    """

    sql_etiquette_query = {
        "select": [
            ["etiquettes", "id"],
            ["etiquettes", "label"],
            ["etiquettes", "color"],
            ["etiquettes", "created_at"],
            ["etiquettes", "updated_at"]
        ],
        "where": [
            ["questions", "id", question_id]
        ],
        "from": {
            "tables": ["questions", "etiquette_question", "etiquettes"],
            "cond": [
                [
                    ["questions", "id"],
                    ["etiquette_question", "question_id"]
                ],
                [
                    ["etiquette_question", "etiquette_id"],
                    ["etiquettes", "id"]
                ]
            ]
        }
    }

    return database.query(sql_etiquette_query)


def createEtiquette(database: Database.Database, label: str, colour: str) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une étiquette.

    :param database: Objet base de données
    :param label: Label de la nouvelle étiquette
    :param colour: Couleur de l'étiquette
    """

    etiquette_id: str = str(uuid.uuid4())

    while len(getEtiquetteByUuid(database, etiquette_id)) > 0:
        etiquette_id = str(uuid.uuid4())

    insert_etiquette = {
        "table": "etiquettes",
        "action": "insert",
        "valeurs": [
            ["id", etiquette_id],
            ["label", label],
            ["color", colour],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_etiquette)
    database.commit()

    return str(etiquette_id)


def removeEtiquette(database, etiquette_id):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour supprimer une étiquette par son id.

    :param database: Objet base de données
    :param etiquette_id: Id de l'étiquette concernée
    """

    question_etiquette_execute = {
        "table": "etiquette_question",
        "action": "delete",
        "valeurs": [
            ["question_id", etiquette_id]
        ]
    }

    etiquette_execute = {
        "table": "etiquettes",
        "action": "delete",
        "valeurs": [
            ["id", etiquette_id]
        ]
    }

    database.execute(question_etiquette_execute)
    database.execute(etiquette_execute)
    return database.commit()


def joinEtiquetteQuestion(database, question_id, etiquette_id, commit: bool = True):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour lier une étiquette et une question
    par une entrée dans la table `etiquette_question`

    :param database: Objet base de données
    :param question_id: Id de la question concernée
    :param etiquette_id: Id de l'étiquette concernée
    :param commit: Si la fonction devrait sauvegarder les changements à la base de données
    """

    insert_question_etiquette_query = {
        "table": "etiquette_question",
        "action": "insert",
        "valeurs": [
            ["etiquette_id", etiquette_id],
            ["question_id", question_id],
        ]
    }

    database.execute(insert_question_etiquette_query)

    if commit:
        database.commit()
