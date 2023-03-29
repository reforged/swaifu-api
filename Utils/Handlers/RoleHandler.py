import BDD.Model as Model


def createRole(query_builder: Model.Model, label: str, power: str, commit: bool = True):
    """
    Fonction simplifiant le processus pour créer un rôle

    :param query_builder: Objet Model
    :param label: Label du rôle
    :param power: Pouvoir du rôle ?
    :param commit: Si les changements doivent être sauvegarder
    """

    params = {
        "label": label,
        "power": power
    }

    return query_builder.table("roles", "insert").where(params).execute(commit=commit)
