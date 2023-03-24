import BDD.Model as Model

import Permissions.Policies as Policies


@Policies.middleware(["store:session"], ["update:session"], ["destroy:session"])
def getAllSessions(query_builder: Model.Model):
    """
    Gère la route .../sessions - Méthode GET

    Permet à un utilisateur de créer une question.

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    """

    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname",
                   "users.created_at", "users.updated_at"]

    res = query_builder.table("sessions").load("reponses")

    for session in res:
        session.load("users", query_builder.select(*info_wanted))

        for reponse in session.reponses:
            reponse.load("users", query_builder.select(*info_wanted))

    res = [row.export() for row in res]

    return res

