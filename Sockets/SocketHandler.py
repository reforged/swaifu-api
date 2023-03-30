import Sockets.Session as Session
import flask
import os
import importlib.util

liste_session: list[Session] = []

req = flask.Request


def add_attributes(dict_arguments: dict[str, any]):
    """
    Fonction fournissant des paramètres à la fonction décorée en fonction des paramètres déclarés.

    :param dict_arguments: Liste des paramètres potentiellement fournissables aux fonctions
    """
    def wrapper(fonction):
        """
        Fonction récupérant et stockant les paramètres demandés pour pouvoir les fournir lors des appels de la fonction.

        :param fonction: Fonction à qui fournir les paramètres à
        """
        co_varnames = getattr(getattr(fonction, "__code__"), "co_varnames")

        if hasattr(fonction, "info_fonction"):
            co_varnames = (getattr(fonction, "info_fonction")).get("co_varnames", co_varnames)

        arguments_demandes = {key: dict_arguments[key] for key in dict_arguments if key in co_varnames}

        def inner(*args, **kwargs):
            return fonction(*args, **kwargs, **arguments_demandes)

        inner.__name__ = fonction.__name__

        return inner

    return wrapper


def load_sessions(Sio, query_builder):
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
