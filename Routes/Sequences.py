import json

import BDD.Model as Model


def getAllSequences(query_builder: Model.Model):
    """
    Gère la route .../sequences - Méthode GET

    Permet à un utilisateur de récupérer toutes les permissions.

    :param query_builder: Objet Model
    """

    # Pour chaque séquence, on charge également la liste des questions associée
    res = [row.export() for row in query_builder.table("sequences").load("questions")]

    for row in res:
        # Et pour ces questions, on désérialise l'énoncé
        for question in row.get("questions", []):
            question["enonce"] = json.loads(question["enonce"])

    return res
