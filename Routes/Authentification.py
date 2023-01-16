import Utils.RoutesImporter as RoutesImporter
import os


def main(route: str, app) -> None:
    print(f"Authentification !\tRoute : {route}{os.path.basename(__file__)[:-3].lower()}/")

    filename = os.path.basename(__file__)[:-3]
    RoutesImporter.import_route(filename, os.path.dirname(__file__), f"{route}{filename.lower()}/", app)
