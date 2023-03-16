import datetime
import uuid

import BDD.Database as Database


def getQuestionByUuid(database: Database.Database, question_id: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir une question par son id.

    :param database: Objet base de données
    :param question_id: Id de la question concernée
    """

    get_question = {
        "where": [
            ["questions", "id", question_id]
        ],
        "from": {
            "tables": ["questions"]
        }
    }

    return database.query(get_question)


def getAllQuestions(database: Database.Database) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir toutes les questions.

    :param database: Objet base de données
    """

    get_questions = {
        "from": {
            "tables": ["questions"]
        }
    }

    return database.query(get_questions)


def getQuestionByCreatorUuid(database: Database.Database, author_id: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir toutes les questions d'un
    utilisateur en fonction de son id.

    :param database: Objet base de données
    :param author_id: Id de l'étiquette concernée
    """

    get_question = {
        "where": [
            ["question", "user_id", author_id]
        ],
        "from": {
            "tables": ["questions"]
        }
    }

    return database.query(get_question)


def createQuestion(database: Database.Database, label: str, enonce: str, user_id: str, q_type, commit: bool = True) -> str:
    # TODO : Modifier pour qu'elle marche avec le nouveau système drag & drop de questions.
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une question.

    :param database: Objet base de données
    :param label: Label de la question
    :param enonce: Enonce de la question
    :param user_id: Id du créateur de la question
    :param q_type: Type de la question (qcm | libre)
    :param commit: Si la fonction doit sauvegarder les changements
    """

    question_id: str = str(uuid.uuid4())

    while len(getQuestionByUuid(database, question_id)) > 0:
        question_id = str(uuid.uuid4())

    insert_query = {
        "table": "questions",
        "action": "insert",
        "valeurs": [
            ["id", question_id],
            ["label", label],
            ["enonce", enonce],
            ["type", q_type],
            ["user_id", user_id],
            ["created_at", datetime.datetime.now().astimezone()],
            ["updated_at", datetime.datetime.now().astimezone()]
        ]
    }

    database.execute(insert_query)

    if commit:
        database.commit()

    return question_id
