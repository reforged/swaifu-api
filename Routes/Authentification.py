import Utils.RoutesImporter as RoutesImporter
import os


def main(route: str, app) -> None:
    print(f"Authentification !\tRoute : {route}{os.path.basename(__file__)[:-3].lower()}/")

    filename = os.path.basename(__file__)[:-3]
    directory_name = os.path.dirname(__file__)
    RoutesImporter.import_route(filename, directory_name, f"{route}{filename.lower()}/", app)
