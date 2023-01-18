import flask
import os

import importlib.util

from BDD.Database import Database

current_dir = None
ignore_dir = ["__pycache__"]


def add_attributes(dict_arguments):
    def wrapper(fonction):
        co_varnames = getattr(getattr(fonction, "__code__"), "co_varnames")

        if hasattr(fonction, "info_fonction"):
            co_varnames = (getattr(fonction, "info_fonction")).get("co_varnames", co_varnames)

        arguments_demandes = {key: dict_arguments[key] for key in dict_arguments if key in co_varnames}

        def inner(*args, **kwargs):
            return fonction(*args, **kwargs, **arguments_demandes)

        inner.__name__ = f"{fonction.__name__}"

        return inner

    return wrapper


def import_route(caller_filename: str, rel_path_to_dir: str, route: str, app: flask.Flask, arguments: dict, parent_module: str = None) -> None:
    print(f"Chemin : {rel_path_to_dir}")
    liste_du_repertoire = os.listdir(rel_path_to_dir)

    fichier_repertoire = [f for f in liste_du_repertoire if os.path.isfile(os.path.join(rel_path_to_dir, f)) and f[-3:] == ".py"]
    repertoires_repertoire = [r for r in liste_du_repertoire if os.path.isdir(os.path.join(rel_path_to_dir, r)) and r not in ignore_dir]

    for repertoire in repertoires_repertoire:
        if f"{repertoire}.py" not in fichier_repertoire:
            print(f"Nom répertoire : {repertoire}\tChemin relatif : {rel_path_to_dir}/{repertoire}\tRoute : {route}{repertoire}/")

            import_route(repertoire, rel_path_to_dir + f"/{repertoire}", f"{route}{repertoire.lower()}/", app, arguments, repertoire)

    for file in fichier_repertoire:
        print(f"Nom fichier : {file}\tChemin relatif : {rel_path_to_dir}/{file}\tRoute : {route}{file[:-3]}/")
        spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module, f"{rel_path_to_dir}/{file}")
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            module.main(rel_path_to_dir, route, app, arguments)

        nom_fichier = file[:-3].lower()

        if hasattr(module, nom_fichier):
            fonction = getattr(module, nom_fichier)

            methods = ["GET"]
            url = f"{route}{nom_fichier}/"

            if hasattr(fonction, "method"):
                methods = [getattr(fonction, "method")]

            if hasattr(fonction, "append_url"):
                url = f"{route}/{getattr(fonction, 'append_url')}/"

            elif hasattr(fonction, "url"):
                url = getattr(fonction, "url")

            nb_arguments = getattr(getattr(fonction, "__code__"), "co_argcount")

            if hasattr(fonction, "info_fonction"):
                nb_arguments = (getattr(fonction, "info_fonction")).get("co_argcount", nb_arguments)

            print(f"{fonction.__name__} has {nb_arguments} parameters")

            if nb_arguments > 0:
                app.route(url, methods=methods)(add_attributes(arguments)(fonction))

            else:
                app.route(url, methods=methods)(fonction)
