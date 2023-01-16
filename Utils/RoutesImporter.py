import flask
import os

import importlib.util

current_dir = None


def import_route(caller_filename: str, target_directory_name: str, route: str, app: flask.Flask, parent_module: str = None) -> None:
    rel_path_to_dir = os.path.relpath(target_directory_name, current_dir) + f"/{caller_filename}"

    fichier_repertoire = [f for f in os.listdir(rel_path_to_dir) if os.path.isfile(os.path.join(rel_path_to_dir, f)) and f[-3:] == ".py"]

    for file in fichier_repertoire:
        print(f"Nom fichier : {file}\tChemin relatif : {rel_path_to_dir}/{file}")
        spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module, f"{rel_path_to_dir}/{file}")
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)
        module.main(route, app)
