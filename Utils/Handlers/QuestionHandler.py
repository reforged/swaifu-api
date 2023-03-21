import datetime
import uuid
import json

import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler


def parseQuestions(func):
    def inner(*args, **kwargs):
        questions = func(*args, **kwargs)

        for question in questions:
            if "enonce" in question.keys():
                question["enonce"] = json.loads(question["enonce"])

        return questions

    return inner


@parseQuestions
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


@parseQuestions
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


@parseQuestions
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


def createQuestion(database: Database.Database, label: str, slug: str, enonce: str, q_type: str, user_id: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une question.

    :param database: Objet base de données
    :param label: Label de la question
    :param slug: Identifiant textuel de la question
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
            ["slug", slug],
            ["enonce", (json.dumps(enonce)).replace("'", '"')],
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


# TODO: Comment
def deleteQuestion(database, question_id, commit: bool = True):
    delete_question_query = {
        "table": "questions",
        "action": "delete",
        "valeurs": [
            ["id", question_id]
        ]
    }

    EtiquetteHandler.unlinkEtiquetteQuestion(database, question_id, False)

    database.execute(delete_question_query)

    if commit:
        database.commit()

    return


def alterQuestion(database: Database.Database, valeurs: dict, commit: bool = True):

    nouvelles_valeurs = []

    if "label" in valeurs :
        nouvelles_valeurs.append(["label", valeurs["label"]])
    if "slug" in valeurs :
        nouvelles_valeurs.append(["slug", valeurs["slug"]])
    if "enonce" in valeurs :
        nouvelles_valeurs.append(["enonce", valeurs["enonce"]])
    if "type" in valeurs :
        nouvelles_valeurs.append(["type", valeurs["type"]])
    nouvelles_valeurs.append(["updated_at", datetime.datetime.now().astimezone()])


    alter_query = {
        "primary" : ["id", question_id]
        "table": "questions",
        "action": "alter",
        "valeurs": nouvelles_valeurs
    }

    database.execute(alter_query)

    if commit:
        database.commit()

    return question_id

