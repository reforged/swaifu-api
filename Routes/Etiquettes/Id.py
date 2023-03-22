import datetime
import flask

import BDD.Model as Model

import Utils.Route as Route


@Route.route(url="<etiquette_id>")
def etiquette_get_etiquette_id(etiquette_id: str, query_builder: Model.Model) -> dict[str, str]:
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode GET

    Permet à un utilisateur d'obtenir les informations d'une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param query_builder: Objet Model
    """

    res = query_builder.table("etiquettes").where("id", etiquette_id).execute()

    if len(res) == 0:
        return {"Error": "Etiquette non trouvée"}

    return res[0]


@Route.route(method="put", url="<etiquette_id>")
def put_id(etiquette_id: str, query_builder: Model.Model, request: flask.Request):
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode PUT

    Permet à un utilisateur de modifier une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param query_builder: Objet Model
    :param request: Objet Request de flask
    """

    old = query_builder.table("etiquettes").where("id", etiquette_id).execute()

    if len(old) == 0:
        return flask.make_response("Erreur", 400, {"Error": "Etiquette non trouvée"})

    old = old[0]

    data = request.get_json()

    new_val = {
        "updated_at": datetime.datetime.now().astimezone()
    }

    # On compare ce qu'il y a en BDD à la nouvelle pour savoir quoi remplacer
    # On n'utilise pas les clés de old et code en dur dans l'éventuellement ou des valeurs sont None
    for key in ["label", "color"]:
        if old.get(key) != data.get(key):
            if data.get(key) is not None:
                new_val[key] = data.get(key)

    query_builder.table("etiquettes", "alter", etiquette_id).where(new_val).execute()

    return {"Message": "Succès"}


@Route.route(method="delete", url="<etiquette_id>")
def delete_id(etiquette_id: str, query_builder: Model.Model) -> dict[str, str]:
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode DELETE

    Permet à un utilisateur de supprimer une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param query_builder: Objet Model
    """

    query_builder.table("etiquettes", "delete").where("id", etiquette_id).execute()

    return {"Message": "Succès"}
