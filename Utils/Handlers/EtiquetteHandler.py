import datetime
import uuid

import BDD.Model as Model


def createEtiquette(query_builder: Model.Model, label: str, colour: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une étiquette.

    :param query_builder: Objet Model
    :param label: Label de la nouvelle étiquette
    :param colour: Couleur de l'étiquette
    :param commit: Si la fonction doit sauvegarder les changements
    """

    etiquette_id: str = str(uuid.uuid4())

    while len(query_builder.table("etiquettes").where("id", etiquette_id).execute()) > 0:
        etiquette_id = str(uuid.uuid4())

    params = {
        "id": etiquette_id,
        "label": label,
        "color": colour,
        "created_at": datetime.datetime.now().astimezone(),
        "updated_at": datetime.datetime.now().astimezone()
    }

    query_builder.table("etiquettes", "insert").where(params).execute(commit=commit)

    return etiquette_id
