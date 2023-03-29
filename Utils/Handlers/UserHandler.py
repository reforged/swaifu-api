import hashlib

import BDD.Model as Model


def addUser(query_builder: Model.Model, password: str, email, numero, firstname: str, lastname: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer un nouvel utilisateur.

    :param query_builder: Objet Model
    :param password: Mot de passe de l'utilisateur
    :param email: Email de l'utilisateur
    :param numero: Numero étudiant de l'utilisateur
    :param firstname: Prénom de l'utilisateur
    :param lastname: Nom de l'utilisateur
    :param commit: Si la fonction doit sauvegarder les changements
    """

    # Encodage du mot de passe bien sûr
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    del password

    # Préparation des paramètres
    params = {
        "email": email,
        "numero": numero,
        "firstname": firstname,
        "lastname": lastname,
        "password": hashed_password
    }

    return query_builder.table("users", "insert").where(params).execute(commit=commit)
