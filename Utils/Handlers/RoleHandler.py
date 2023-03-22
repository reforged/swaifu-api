import datetime
import uuid

import BDD.Model as Model


def createRole(query_builder: Model.Model, label: str, power: str, commit: bool = True):
    """
    Fonction simplifiant le processus pour créer un rôle

    :param query_builder: Objet Model
    :param label: Label du rôle
    :param power: Pouvoir du rôle ?
    :param commit: Si les changements doivent être sauvegarder
    """

    role_id: str = str(uuid.uuid4())

    while len(query_builder.table("roles").where("id", role_id).execute()) > 0:
        role_id = str(uuid.uuid4())

    params = {
        "id": role_id,
        "label": label,
        "power": power,
        "created_at": datetime.datetime.now().astimezone(),
        "updated_at": datetime.datetime.now().astimezone()
    }

    query_builder.table("roles", "insert").where(params).execute(commit=commit)

    return role_id
