import os

with open(r"C:\Users\ospat\PycharmProjects\Api\.env", "r") as file:
    result = (file.read()).split("\n")

store = {key: value for key, value in [line.split("=") for line in result]}


def getenv(key):
    """
    Fonction renvoyant la variable d'environnement donnée (Simule, les variables sont stockés dans un fichier '.env'

    :param key: Nom de la variable demandée
    """

    return store.get(key)
