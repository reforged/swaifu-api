import BDD.Database as Database

import Utils.Handlers.UserHandler as UserHandler

import Utils.Route as Route


@Route.route(method="delete", url="<user_id>")
def delete_user(user_id: str, database: Database.Database):
    """
    Gère la route .../users/<user_id> - Méthode DELETE

    Permet à un utilisateur de supprimer un compte utilisateur.

    Nécessite d'être connecté.

    :param user_id: Id de l'utilisateur concerné
    :param database: Objet base de données
    """

    UserHandler.delete_user(database, user_id)
