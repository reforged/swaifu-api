import flask
import importlib.util
import os
import types

from Utils.Handlers.ObjectInspector import retrieveAttr, checkAttr
from Utils.AttributeAdder import add_attributes

ignore_dir = ["__pycache__"]
ignore_functions = ["main"]


def import_route(caller_filename: str, rel_path_to_dir: str, route: str, app: flask.Flask, arguments: dict, parent_module: str = None) -> None:
    """
    Fonction qui pour un répertoire donné, url, objet serveur, arguments éventuels et nom du module parent appelant
    cette fonction, importe automatiquement tous les fichiers dans l'arborescence indiqué, en prenant soin de ne
    regarder que les fichiers python et répertoires, et ignorant certains répertoires indiqués dans `ignore_dir`

    :param caller_filename: Nom du fichier appelant pour organiser la hiérarchie des imports
    :param rel_path_to_dir: Chemin relatif au répertoire que nous explorons
    :param route: url construite jusqu'à présent, du groupe actuel
    :param app: L'objet correspondant à l'application Serveur, nécessaire pour créer les routes
    :param arguments: Dictionnaire contenant des arguments pouvant être demandés par les fonctions (voir add_attributes)
    :param parent_module: Module parent des fonctions qui vont être importés, important pour rester propre et éviter des conflits
    """

    # Liste de tout les objets dans le répertoire
    liste_du_repertoire = os.listdir(os.path.join(rel_path_to_dir))

    # Séparation en fichiers et en répertoires puisque nous aggisserons différemment
    # Nous vérifions également les extensions de fichiers, et évitons tout fichier oiu répertoire interdit
    fichier_repertoire = [f for f in liste_du_repertoire if os.path.isfile(os.path.join(rel_path_to_dir, f)) and f[-3:] == ".py"]
    repertoires_repertoire = [r for r in liste_du_repertoire if os.path.isdir(os.path.join(rel_path_to_dir, r)) and r not in ignore_dir]

    for repertoire in repertoires_repertoire:
        # Pour chaque répertoire, nous vérifions si un fichier python portant le nom du répertoire existe,
        # Puisque nous pouvons avoir besoin d'un gestionnaire de groupe spécial
        if f"{repertoire}.py" not in fichier_repertoire:
            # Si ce fichier n'existe pas nous faisons un simple appel récursif
            import_route(repertoire, rel_path_to_dir + f"/{repertoire}", f"{route}{repertoire.lower()}/", app,
                         arguments, repertoire)

        else:
            # Si le fichier existe, nous le chargeons et vérifions s'il possède une méthode main, si oui nous l'appelons
            spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module,
                                                          f"{rel_path_to_dir}/{repertoire}.py")
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if not hasattr(module, "main"):
                import_route(repertoire, rel_path_to_dir + f"/{repertoire}", f"{route}{repertoire.lower()}/", app,
                             arguments, repertoire)

    for file in fichier_repertoire:
        # Pour chaque fichier dans le répertoire, nous les chargeons en tant que modules
        spec = importlib.util.spec_from_file_location(caller_filename if parent_module is None else parent_module, f"{rel_path_to_dir}/{file}")
        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            # S'il possède un fichier main on y fait appel, afin de le permettre d'éventuellement mettre en place
            # Certaines données
            module.main(rel_path_to_dir, route, app, arguments)

        # Suppression du `.py` à la fin
        nom_fichier = file[:-3].lower()

        # On récupère chaque fonction du fichier
        # Verbose car dir() renvoie tout attributs
        # On vérifie donc d'abord s'il s'agit d'un objet de type Fonction
        # Puis on récupère le nom du module et on vérifie que c'est le même que celui que nous souhaitons charger
        #   Si le module fait import json alors json.dumps ou json.load apparaitra dans dir() en tant que fonction
        #   Du module
        # Puis on s'assure qu'il ne s'agit pas d'une fonction avec un nom sépcial, nous indiquant de l'ignorer

        liste_fonctions = [
            getattr(module, object) for object in dir(module)
            if isinstance(getattr(module, object), types.FunctionType)
            and retrieveAttr(getattr(module, object), '__module__') == module.__name__
            and getattr(getattr(module, object), "__name__") not in ignore_functions
        ]

        for fonction in liste_fonctions:
            # Pour chacune de ces méthodes, on récupère leur méthode déclarée
            methods = [retrieveAttr(fonction, "method", "GET")]
            # Url de base
            url = f"{route}{nom_fichier}/"

            # Si l'url commence **pas** par /, alors ce n'est qu'un remplacement de nom_fichier et on l'ajoute à
            # `route` pour former l'url
            if checkAttr(fonction, "append_url"):
                url = f"{route}{retrieveAttr(fonction, 'append_url')}"

            # SInon si l'url commence par /, il s'agit d'un chemin absolu, ignorant les chemins précédant (route)
            elif checkAttr(fonction, "url"):
                url = retrieveAttr(fonction, "url")

            # On récupère le nombre d'arguments de la fonction, et si > 0
            nb_arguments = retrieveAttr(fonction, "co_argcount") or getattr(getattr(fonction, "__code__"), "co_argcount")

            print(f"URL FINALE DE {fonction.__name__} est {url} en utilisant méthodes {retrieveAttr(fonction, 'method', 'GET')}")

            # On les regarde pour éventuellement charger des paramètres nommés, tels que query_builder ou request
            if nb_arguments > 0:
                app.route(url, methods=methods)(add_attributes(arguments)(fonction))

            # Sinon, on crée la route telle quel
            else:
                app.route(url, methods=methods)(fonction)
