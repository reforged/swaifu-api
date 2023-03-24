import os

current_dirname = os.path.dirname(__file__.replace("\\", "/"))


with open(f"{current_dirname}/../.env", "r") as file:
    result = (file.read()).split("\n")

store = {key: value for key, value in [line.split("=") for line in result]}


def getenv(key):
    """
    Fonction renvoyant la variable d'environnement donnée (Simulé, les variables sont stockés dans un fichier '.env'

    :param key: Nom de la variable demandée
    """

    return store.get(key)
