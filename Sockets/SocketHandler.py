import importlib.util
import os

from Utils.AttributeAdder import add_attributes

import Sockets.Session as Session

liste_session: list[Session] = []


def load_sessions(Sio, query_builder):
    """
    Permet de charger tout les events des sockets située dans .../Sockets/Events
    :param Sio: Object SocketIO
    :param query_builder: Objet Model
    """
    table_dir = os.path.join(os.path.dirname(__file__), "Events").replace("\\", "/")

    liste_fichiers = [file for file in os.listdir(table_dir) if os.path.isfile(os.path.join(table_dir, file))]

    params = {
        "query_builder": query_builder,
        "sio": Sio,
        "liste_session": liste_session
    }

    for name_fichier in liste_fichiers:
        print(f"Fichier : {name_fichier}")
        spec = importlib.util.spec_from_file_location(f"Sockets.Events.{name_fichier[:-3]}", f"{table_dir}/{name_fichier}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        liste_fonctions = [
            getattr(module, object) for object in dir(module)
            if (type(getattr(module, object)) == type(load_sessions))
            and getattr(getattr(module, object), "__module__") == module.__name__
        ]

        for fonction in liste_fonctions:
            print(f"Fonction nom : {fonction.__name__}")

            Sio.on(fonction.__name__)(add_attributes(params)(fonction))


def createSession(sequence_id: str, query_builder, sio) -> Session.Session:
    temp = (Session.Session(query_builder, sequence_id, sio))
    liste_session.append(temp)

    return temp
