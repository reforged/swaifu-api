import BDD.Model as Model

import Utils.Route as Route


@Route.route(url='<user_id>')
def user(user_id: str, query_builder: Model.Model):
    """
    Gère la route .../questions/user/<user_id> - Méthode GET

    Permet à un utilisateur de récupérer toutes les questions créé par un auteur en fonction de son id.

    :param user_id: Id de l'auteur
    :param query_builder: Objet Model
    """

    user_questions = query_builder.table("questions").where("user_id", user_id).load("etiquettes")

    for question in user_questions:
        question.load("reponses")

    return [row.export() for row in user_questions]
