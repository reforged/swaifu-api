import flask
import os

import importlib.util
from Utils.ObjectInspector import retrieveAttr, checkAttr

import types
current_dir = None
ignore_dir = ["__pycache__"]
ignore_functions = ["main"]


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

        spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module,
                                                      f"{rel_path_to_dir}/{repertoire}.py")
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        if not hasattr(module, "main"):
            print(f"Nom répertoire : {repertoire}\tChemin relatif : {rel_path_to_dir}/{repertoire}\tRoute : {route}{repertoire}/")

            import_route(repertoire, rel_path_to_dir + f"/{repertoire}", f"{route}{repertoire.lower()}/", app,
                         arguments, repertoire)

    for file in fichier_repertoire:
        print(f"Nom fichier : {file}\tChemin relatif : {rel_path_to_dir}/{file}\tRoute : {route}{file[:-3]}/")
        spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module, f"{rel_path_to_dir}/{file}")
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            module.main(rel_path_to_dir, route, app, arguments)

        nom_fichier = file[:-3].lower()

        listeFonctions = [
            getattr(module, object) for object in dir(module)
            if isinstance(getattr(module, object), types.FunctionType)
            and retrieveAttr(getattr(module, object), '__module__') == module.__name__
            and getattr(getattr(module, object), "__name__") not in ignore_functions
        ]

        print(f"fichier : {module.__name__}\tlisteFonctions : {[fonc.__name__ for fonc in listeFonctions]}")

        for fonction in listeFonctions:
            methods = [retrieveAttr(fonction, "method", "GET")]
            url = f"{route}{nom_fichier}/"

            if checkAttr(fonction, "append_url"):
                url = f"{route}/{retrieveAttr(fonction, 'append_url')}/"

            elif checkAttr(fonction, "url"):
                url = retrieveAttr(fonction, "url")

            nb_arguments = retrieveAttr(fonction, "co_argcount") or getattr(getattr(fonction, "__code__"), "co_argcount")

            print(f"{fonction.__name__} has {nb_arguments} parameters")

            print(f"URL FINALE DE {fonction.__name__} est {url} en utilisant méthode {methods}")

            if nb_arguments > 0:
                app.route(url, methods=methods)(add_attributes(arguments)(fonction))

            else:
                app.route(url, methods=methods)(fonction)
