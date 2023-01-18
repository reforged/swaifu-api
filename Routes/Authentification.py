import Utils.RoutesImporter as RoutesImporter
import os
from flask import Flask


def main(rel_path_to_dir: str, route: str, app: Flask, arguments: dict) -> None:
    print(f"Authentification !\tRoute : {route}{os.path.basename(__file__)[:-3].lower()}/")

    filename = os.path.basename(__file__)[:-3]
    rel_path_to_dir += f"/{filename}"
    RoutesImporter.import_route(filename, rel_path_to_dir, f"{route}{filename.lower()}/", app, arguments)
