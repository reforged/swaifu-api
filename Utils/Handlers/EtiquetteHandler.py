import BDD.Model as Model


def createEtiquette(query_builder: Model.Model, label: str, colour: str, commit: bool = True) -> str:
    """
    Fonction gérant la connection à la base de données, abstrait le processus pour créer une étiquette.

    :param query_builder: Objet Model
    :param label: Label de la nouvelle étiquette
    :param colour: Couleur de l'étiquette
    :param commit: Si la fonction doit sauvegarder les changements
    """

    params = {
        "label": label,
        "color": colour
    }

    return query_builder.table("etiquettes", "insert").where(params).execute(commit=commit)
