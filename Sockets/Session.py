import flask_socketio
import json

import BDD.Model as Model

import Utils.Sockets.GenerateCode as GenerateCode

codesEnUtilisation: dict[str, any] = {}


class Session:
    """
    Etats :
    0   -> Initialisation + Affichage code pour rejoindre
    1   -> Début Diffusion: start_diffuse
    2   -> Acceptation Réponses: accept_answers
    3   -> Refus réponses : reject_answers
    4   -> Affichage réponses: display_answers
    5   -> Fin diffusion scène actuelle: end_scene
    """

    liste_questions = []
    liste_de_reponse = [{}]
    population: int = 0
    etat: int = 0
    lock: bool = False

    reponse_actuelle: list = None

    session_id: str = None

    def __init__(self, query_builder: Model.Model, sequence_id: str, socket: flask_socketio.SocketIO):
        self.socket = socket
        self.db_connection: Model.Model = query_builder
        self.sequence_id: str = sequence_id

        self.query_builder = query_builder

        self.code: str = GenerateCode.generateCode(8)
        while self.code in codesEnUtilisation:
            self.code = GenerateCode.generateCode(8)

        codesEnUtilisation[self.code] = self

        self.liste_questions = query_builder.table("sequences").where("id", sequence_id).load("questions")[0]

        print(f"Liste de questions : {self.liste_questions}")

        self.liste_questions = self.liste_questions.export(True)["questions"]

        for question in self.liste_questions:
            question["enonce"] = json.loads(question["enonce"])

        self.index_question_actuelle = 0

        self.reponse_actuelle = self.reponsesActuelle()

    def __del__(self):
        del codesEnUtilisation[self.code]

    def questionActuelle(self):
        return self.liste_questions[self.index_question_actuelle]

    def questionSuivante(self):
        self.index_question_actuelle += 1
        self.liste_de_reponse.append({})

    def reponsesActuelle(self) -> list[dict]:
        return self.query_builder.table("reponses").where("question_id", self.questionActuelle()["id"]).execute()

    def addAnswers(self, reponses: list[dict[str, str]], user_id: str):
        del self.liste_de_reponse[self.index_question_actuelle][user_id]

        for reponse in reponses:
            body = reponse.get("body")

            data = {
                "body": body,
                "valide": True,
                "user_id": user_id,
                "session_id": self.session_id,
                "question_id": self.questionActuelle()["id"]
            }

            self.liste_de_reponse[self.index_question_actuelle][user_id] = data
