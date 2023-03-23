import flask_socketio
from flask import request
from flask_socketio import close_room

import BDD.Model as Model

import Utils.Sockets.GenerateCode as GenerateCode
import Utils.Handlers.SequenceHandler as SequenceHandler
import Utils.Handlers.UserResponseHandler as UserReponseHandler
import Utils.Handlers.ReponseHandler as GetReponses
import Utils.Types as Types

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
    population: int = 0
    etat: int = 0

    def __init__(self, query_builder: Model.Model, sequence_id: str, socket: flask_socketio.SocketIO):
        self.socket = socket
        self.db_connection: Model.Model = query_builder
        self.sequence_id: str = sequence_id

        res = query_builder.table("sequences").where("id", sequence_id).load("questions")
        res = [row.export() for row in res]

        self.liste_questions = res.get("questions", [])

        self.code: str = GenerateCode.generateCode(8)
        while self.code not in codesEnUtilisation:
            self.code = GenerateCode.generateCode(8)

        codesEnUtilisation[self.code] = self

        self.index_question_actuelle = 0

    def __del__(self):
        del codesEnUtilisation[self.code]

    def envoiQuestions(self):
        self.socket.emit("question", self.liste_questions[self.index_question_actuelle], to=self.code)

    def modificationVisibilite(self):
        # State = 1 - 3
        self.socket.emit("visibilite", {}, to=self.code)

    def nouvelleReponse(self, user_id: str, reponses: list):
        # State = 2
        if self.etat != 2:
            return

        add_response = []

        for reponse in reponses:
            reponse_data = {
                "id": request.sid,
                "body": reponse["payload"]["body"],
                # TODO: Vérif réponse
                "valide": reponse == ""
            }

            if reponse["type"] == "qcm":
                if len(GetReponses.getReponses(self.db_connection, reponse["payload"]["id"])) == 0:
                    return

            add_response.append(reponse_data)

        self.reponses_sequence_donnees[request.sid] = add_response

    def finDiffusion(self):
        # State = 3
        # Broadcast signal de fin
        self.socket.emit("fin", {}, to=self.code)

    def affichage(self):
        # State = 4
        # Broadcast les réponses justes
        self.socket.emit("reponse", self.bonne_reponse, to=self.code)

    def questionSuivante(self):
        # State = 5
        """
        Stockage des réponses dans la BDD
        Récupération de la prochaine valeur
        Réinitialisations des valeurs pertinentes -> bonne_reponse, incrémentation de listeQuestions, . . .
        Récupération de la bonne réponse
        """
        self.index_question_actuelle += 1
        # write to db

        self.envoiQuestions()
        self.bonne_reponse = self.liste_questions[self.index_question_actuelle]["reponses"]

        for user_id in self.reponses_sequence_donnees:
            # TODO: CHECK LASTVAL RETURN
            question_sequence_user_id = UserReponseHandler.addQuestionSequenceUser(self.db_connection, user_id, self.liste_questions[self.index_question_actuelle], self.session_sequence_id)['id']

            for reponse in self.reponses_sequence_donnees[user_id]:
                UserReponseHandler.addUserResponse(self.db_connection, reponse["body"], reponse["valide"], question_sequence_user_id)

    def finSequence(self):
        # State = 6
        """
        Stockage de la séquence + nombre d'utilisateurs
        Suppression de la salle (/ Désinscription de tout le monde dedans)
        Envoie statistiques ?
        Suppression de la session pour libérer le code
        """
        close_room(self.socket)

        SequenceHandler.addSession(self.db_connection, self.sequence_id, self.code, self.session_sequence_id, self.population, True)

        del Session.codesEnUtilisation[self.code]
