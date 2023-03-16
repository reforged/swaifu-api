import BDD.Database as Database
import flask

import Utils.Handlers.UserHandler as UserHandler

import Utils.Route as Route


@Route.route(method="POST")
def createMany(database: Database.Database, request: flask.Request):
    """
    Gère la route .../users/create-many - Méthode POST

    Permet à un utilisateur de créer plusieurs utilisateurs à la fois.

    Nécessite d'être connecté.

    :param database: Objet base de données
    :param request: Objet Request de flask
    """

    listeAInscrire = request.get_json()

    # TODO : Ajout vérification format.

    UserHandler.addUsers(database, listeAInscrire)
