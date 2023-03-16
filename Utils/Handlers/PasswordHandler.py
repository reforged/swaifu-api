import BDD.Database as Database


def getPasswordByEmail(database: Database.Database, email: str) -> list[dict[str, str]]:
    # TODO : Vérifier le bon fonctionnement ?

    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir le mot de passe d'un
    utilisateur en fonction de son adresse email (unique).

    Pas tous les utilisateurs ont un email. Remplacée par l'INE.

    :param database: Objet base de données
    :param email: Id de l'étiquette concernée
    """

    password_request = {
        "where": [
            ["users", "email", email, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(password_request)
