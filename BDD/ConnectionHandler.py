import Database

handlers = {"fichier": None, "sql": None}


def initiate(systeme: str) -> Database:
    if systeme.lower() not in handlers.keys():
        return
        # Raise Error

    handlers.get(systeme.lower())()


