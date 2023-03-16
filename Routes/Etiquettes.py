import BDD.Database as Database

import Utils.Handlers.EtiquetteHandler as EtiquetteHandler


def etiquettes(database: Database.Database):
    return EtiquetteHandler.getAllEtiquettes(database)
