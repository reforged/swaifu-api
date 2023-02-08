import BDD.Database as Database

import Utils.EtiquetteHandler as EtiquetteHandler
import Utils.Route as Route


@Route.route(url="<etiquette_id>")
def etiquette_get_etiquette_id(etiquette_id: str, database: Database.Database) -> dict[str, str]:
    return database.query(EtiquetteHandler.getEtiquetteByUuid(database, etiquette_id))[0]


@Route.route(method="put", url="<etiquette_id>")
def put_id(etiquette_id: str, database: Database.Database) -> None:
    pass


@Route.route(method="delete", url="<etiquette_id>")
def delete_id(etiquette_id: str, database: Database.Database) -> dict[str, str]:
    EtiquetteHandler.removeEtiquette(database, etiquette_id)

    return {"Message": "Succès"}
