with open(".env", "r") as file:
    result = (file.read()).split("\n")

store = {key: value for key, value in [line.split("=") for line in result]}


def getenv(key):
    return store.get(key)
