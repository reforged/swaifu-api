import flask_socketio
from flask import request
from flask_socketio import close_room

import BDD.Database as Database

import Utils.Sockets.GenerateCode as GenerateCode
import Utils.SequenceHandler as SequenceHandler
import Utils.UserResponseHandler as UserReponseHandler
import Utils.ReponseHandler as GetReponses
import Utils.Types as Types


class Session:
    """
    Etats :
    0   -> Initialisation + Affichage code pour rejoindre
    1   -> Début Diffussion
    2   -> Acceptation Réponses
    3   -> Refus réponses
    4   -> Affichage réponses
    5   -> Fin diffusion scène actuelle
    """
    codesEnUtilisation: dict[str, int] = {}

    def __init__(self, database: Database.Database, sequence_id: str, socket: flask_socketio.SocketIO):
        self.socket = socket
        self.db_connection: Database.Database = database

        self.code: str = GenerateCode.generateCode(8)
        while self.code not in Session.codesEnUtilisation:
            self.code = GenerateCode.generateCode(8)

        self.population: int = 0
        self.etat: int = 0

        self.sequence_id: str = sequence_id
        self.session_sequence_id: Types.union_s_n = None

        self.bonne_reponse: Types.union_sl_n = None
        self.reponses_sequence_donnees = {}
        self.reponses_sequence_totalite = []

        Session.codesEnUtilisation[self.code] = self.population

        self.liste_questions = None
        self.index_question_actuelle = 0

    def __del__(self):
        del Session.codesEnUtilisation[self.code]

    def creerSession(self):
        self.session_sequence_id = SequenceHandler.creerSession(self.db_connection, self.sequence_id, self.code)
        self.liste_questions: Types.ty_que = SequenceHandler.getQuestionsBySequenceId(self.db_connection,
                                                                                      self.sequence_id)

        for question in self.liste_questions:
            question["reponses"] = GetReponses.getReponses(self.db_connection, question['id'])

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
