from flask import request

import Utils.Sockets.GenerateCode as GenerateCode
import Utils.SequenceHandler as SequenceHandler
import Utils.UserResponseHandler as UserReponseHandler
import Utils.ReponseHandler as GetReponses


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
    codesEnUtilisation = {}

    def __init__(self, database, sequence_id, socket):
        self.socket = socket
        self.db_connection = database

        self.code = GenerateCode.generateCode(8)
        while self.code not in Session.codesEnUtilisation:
            self.code = GenerateCode.generateCode(8)

        self.population = 0
        self.etat = 0
        self.sid_animateur = None

        self.sequence_id = sequence_id
        self.session_sequence_id = None

        self.bonne_reponse = None
        self.reponses_sequence_donnees = {}
        self.reponses_sequence_totalite = []

        Session.codesEnUtilisation[self.code] = self.population

        self.liste_questions = None
        self.index_question_actuelle = 0

    def __del__(self):
        del Session.codesEnUtilisation[self.code]

    def creerSession(self):
        self.session_sequence_id = SequenceHandler.creerSession(self.db_connection, self.sequence_id, self.code)
        self.liste_questions = SequenceHandler.getQuestionsBySequenceId(self.sequence_id)

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
                "valide": reponse == "" # TODO: Vérif réponse
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
        Réinitialisations des valeurs pertinantes -> bonne_reponse, incrémentation de listeQuestions, . . .
        Récupération de la bonne réponse
        """
        self.index_question_actuelle += 1
        # write to db

        self.envoiQuestions()
        self.bonne_reponse = self.liste_questions[self.index_question_actuelle]["reponses"]

        for user_id in self.reponses_sequence_donnees:
            question_sequence_user_id = UserReponseHandler.addQuestionSequenceUser(self.db_connection, user_id, self.liste_questions[self.index_question_actuelle], self.session_sequence_id)

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
        pass
