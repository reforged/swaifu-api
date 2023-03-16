import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler
import Utils.Route as Route


@Route.route(url="<etiquette_id>")
def etiquette_get_etiquette_id(etiquette_id: str, database: Database.Database) -> dict[str, str]:
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode GET

    Permet à un utilisateur d'obtenir les informations d'une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param database: Objet base de données
    """
    return EtiquetteHandler.getEtiquetteByUuid(database, etiquette_id)[0]


@Route.route(method="put", url="<etiquette_id>")
def put_id(etiquette_id: str, database: Database.Database) -> None:
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode PUT

    Non implémentée.

    Permet à un utilisateur de modifier une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param database: Objet base de données
    """
    pass


@Route.route(method="delete", url="<etiquette_id>")
def delete_id(etiquette_id: str, database: Database.Database) -> dict[str, str]:
    """
    Gère la route .../etiquettes/<etiquette_id> - Méthode DELETE

    Permet à un utilisateur de supprimer une étiquette en fonction de son id.

    Nécessite d'être connecté.

    :param etiquette_id: Id de l'étiquette concernée
    :param database: Objet base de données
    """

    EtiquetteHandler.removeEtiquette(database, etiquette_id)

    return {"Message": "Succès"}
