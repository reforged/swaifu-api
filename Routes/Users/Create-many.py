import BDD.Model as Model
import flask

import Utils.Handlers.UserHandler as UserHandler
import Utils.Erreurs.HttpErreurs as HttpErreurs

import Utils.Route as Route

import Permissions.Policies as Policies


@Policies.middleware(["store:user"])
@Route.route(method="POST")
def createMany(query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../users/create-many - Méthode POST

    Permet à un utilisateur de créer plusieurs utilisateurs à la fois.

    Nécessite d'être connecté.

    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    # Liste des utilisateurs à inscrire
    liste_a_inscrire = request.get_json().get("users", [])
    user_id_list = []

    # Pour chaque utilisateur on vérifie la bonne présence des données
    for user_data in liste_a_inscrire:
        firstname: str = user_data.get("firstname")
        lastname: str = user_data.get("lastname")

        email: str = user_data.get("email")
        numero: str = user_data.get("numero")

        if numero is not None:
            if numero[-1] == '\r':
                numero = numero[:-1]

        password: str = user_data.get("password", numero)

        if numero is not None:
            if len(numero) > 8:
                numero = None

        for value in [firstname, lastname]:
            if value is None:
                query_builder.rollback()
                return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

        if email is None and numero is None:
            query_builder.rollback()
            return flask.make_response(HttpErreurs.requete_malforme, 400, HttpErreurs.requete_malforme)

        # On ne commiy bien sûr pas encore
        user_id = UserHandler.addUser(query_builder, password, email, numero, firstname, lastname, commit=False)

        # On stocke la liste des id des utilisateurs créés
        user_id_list.append(user_id)

    # A la fin, on commit
    query_builder.commit()

    # Et on renvoie les id
    return user_id_list

