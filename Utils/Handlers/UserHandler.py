import datetime
import hashlib
import flask
import uuid

import BDD.Database as Database

from Erreurs.HttpErreurs import requete_malforme


def addUser(database: Database.Database, password: str, email: str, firstname: str, lastname: str, commit: bool = True):
    # TODO : Mettre à jour pour INE et email
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer un nouvel utilisateur.

    :param database: Objet base de données
    :param password: Mot de passe de l'utilisateur
    :param email: Email de l'utilisateur
    :param firstname: Prénom de l'utilisateur
    :param lastname: Nom de l'utilisateur
    :param commit: Si la fonction doit suavegarder les changements
    """

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    del password

    conflict = True
    user_uuid = None

    while conflict:
        user_uuid = str(uuid.uuid4())

        check_uuid_query = {
            "where": [
                ["users", "id", user_uuid, "and"]
            ],
            "from": {
                "tables": ["users"]
            }
        }

        if len(database.query(check_uuid_query)) == 0:
            conflict = False

    creation_utilisateur = {
        "table": "users",
        "action": "insert",
        "valeurs": [
            ["id", user_uuid],
            ["email", email],
            ["firstname", firstname],
            ["lastname", lastname],
            ["password", hashed_password],
            ["created_at", str(datetime.datetime.now().astimezone())],
            ["updated_at", str(datetime.datetime.now().astimezone())]
        ]
    }

    database.execute(creation_utilisateur)

    if commit:
        database.commit()

    return user_uuid


def delete_user(database: Database.Database, user_id: str):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour supprimer un utilisateur en fonction
    de son id.

    :param database: Objet base de données
    :param user_id: Id de l'utilisateur concerné
    """

    execute_delete_user = {
        "table": "users",
        "action": "delete",
        "valeurs": [
            ["id", user_id]
        ]
    }

    database.execute(execute_delete_user)
    return database.commit()


def addUsers(database: Database.Database, user_create_list: list[dict]):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer plusieurs utilisateurs.

    :param database: Objet base de données
    :param user_create_list: Liste d'informations d'utilisateurs à créer
    """

    return_uuid = []

    for utilisateur in user_create_list:
        email = utilisateur.get("numero")
        firstname = utilisateur.get("firstname")
        lastname = utilisateur.get("lastname")
        password = utilisateur.get("password")

        for data in [email, firstname, lastname, password]:
            if data is None:
                return flask.make_response(requete_malforme, 400, requete_malforme)

        return_uuid.append(addUser(database, password, email, firstname, lastname, commit=False))

    database.commit()

    return return_uuid


def getUserByNumero(database: Database.Database, numero: str):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir une étiquette par son id.

    :param database: Objet base de données
    :param numero: Id de l'étiquette concernée
    """

    check_user_query = {
        "where": [
            ["users", "numero", numero]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(check_user_query)


def getUserByUuid(database: Database.Database, user_id: str):
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour obtenir un utilisateur par son id.

    :param database: Objet base de données
    :param user_id: Id de l'utilisateur concerné
    """

    get_user_query = {
        "select": [
            ["users", "firstname"],
            ["users", "email"],
            ["users", "lastname"],
            ["users", "created_at"],
            ["users", "updated_at"]
        ],
        "where": [
            ["users", "id", user_id, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(get_user_query)
