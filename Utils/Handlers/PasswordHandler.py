import BDD.Database as Database


def getPasswordByEmail(database: Database.Database, email: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir le mot de passe d'un
    utilisateur en fonction de son adresse email (unique).

    :param database: Objet base de données
    :param email: Email de l'utilisateur
    """

    password_request_via_email = {
        "where": [
            ["users", "email", email]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(password_request_via_email)


def getPasswordByStudentId(database: Database.Database, numero: str) -> list[dict[str, str]]:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir le mot de passe d'un
    utilisateur en fonction de son numéro étudiant (unique).

    :param database: Objet base de données
    :param numero: Numéro étudiant de l'utilisateur
    """

    password_request_via_student_id = {
        "where": [
            ["users", "numero", numero]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(password_request_via_student_id)
