import BDD.Database as Database

import Utils.EtiquetteHandler as EtiquetteHandler


def etiquettes(database: Database.Database):
    return EtiquetteHandler.getAllEtiquettes(database)
