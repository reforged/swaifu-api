from __future__ import annotations

import copy
import importlib.util
import os
from typing import Union

import BDD.Database as Database

import BDD.Table as Table


tables = {}


class A:
    pass


ignore_directory = ["__pycache__"]

table_dir = os.path.join(os.path.dirname(__file__), "BDD_TABLES").replace("\\", "/")

liste_fichiers = [file for file in os.listdir(table_dir) if os.path.isfile(os.path.join(table_dir, file))]

for name_fichier in liste_fichiers:
    spec = importlib.util.spec_from_file_location(f"BDD.BDD_TABLES.{name_fichier[:-3]}", f"{table_dir}/{name_fichier}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    liste_classes = [
                    getattr(module, object) for object in dir(module)
                    if (isinstance(getattr(module, object), type))
                    and getattr(getattr(module, object), "__module__") == module.__name__
                ]

    liste_classes: list[Table.Table] = [classe for classe in liste_classes if issubclass(classe, Table.Table)]

    # print(dir(module))
    if liste_classes:
        table_name = liste_classes[0].__dict__.get("table_name", liste_classes[0].__name__).lower()

        tables[table_name] = liste_classes[0]


class Model:
    """
    Classe représentant une usine de construction de requêtes.

    Prends un objet de type Base de données et est capable d'effectuer des requêtes dessus.
    """
    database: Database.Database
    table_name: str
    query: dict
    action: str = None

    def __init__(self, database: Database.Database):
        """
        :param database: Objet base de donnée sur lequel effectuer les requêtes
        """

        self.database = database
        self.query = {}

    def table(self, table_name: str, action: str = None, pk_value: str = None) -> Model:
        """
        Permet de sélectionner la table sur laquelle s'effectuera la requête

        Renvoie une copie de soi-même pour éviter la contamination d'informations puisque le même objet est partagé
        par souci d'efficacité et de mémoire.

        :param table_name: Nom de la table sur laquelle agir
        :param pk_value: Dans le cas de l'action = alter, la valeur de la clé primaire de l'objet souhaité est donnée, puisque le where est utilisé pour autre chose
        """

        new_model = self.copy()

        new_model.action = action

        # On supporte le renommage de table grâce au mot clé 'and' pour les requêtes complexes,
        # Il faut donc le prendre en compte lorsqu'on récupère le nom de la table
        if " as " in table_name:
            stripped_table_name = table_name.split(" as ")[0].rstrip().lower()
        else:
            stripped_table_name = table_name.lower()

        if action is None:
            # Dans le cas d'une requête n'entrainant aucune modification,
            # Nous stockons les informations suivant un format spécifique tout en créant les objets éventuellement
            # Manquant dans le .query
            new_model.table_name = stripped_table_name

            if "from" not in new_model.query:
                new_model.query["from"] = {}

            if "tables" not in new_model.query["from"]:
                new_model.query["from"]["tables"] = []

            new_model.query["from"]["tables"].append(table_name)

        else:
            # Une autre syntaxe est employée dans le cas de modifications à la BDD, nottament puisqu'une seule table
            # Sera modifié (Choix obligatoire)
            new_model.query["table"] = stripped_table_name
            new_model.query["action"] = action

            if action == "alter":
                # Et si nous modifions une ligne, il nous faut penser à la clé primaire
                if pk_value is None:
                    raise ValueError("Valeur clé primaire manquante dans alter")

                pk_name = tables.get(stripped_table_name).primary_key

                new_model.query["primary"] = [pk_name, pk_value]

        return new_model

    def select(self, *args: str) -> Model:
        """
        Permet d'indiquer dans une requête les colonnes souhaitées
        """

        if len(args) == 0:
            raise ValueError("Select was given no arguments")

        model = self

        # Pour autoriser la création de 'templates', si aucune table est spécifiée, nous sommes sur l'objet racine qui
        # Ne doit être modifié, et donc nous travaillions sur une copie
        if "table_name" not in self.__dict__:
            model = self.copy()

        if "*" in args:
            model.query["select"] = ["*"]
            return model

        if "select" not in model.query:
            model.query["select"] = []

        # Nous prenons un nombre non fixé de paramètres, représentée sous forme de liste
        for value in args:
            model.query["select"].append(value)

        return model

    def where(self, key: Union[str, dict[str, str]], value: str = None) -> Model:
        """
        Permet d'indiquer une paire clé valeur à respecter dans la requête

        Dans le cas de query et de delete permet d'indiquer une colonne
        Sinon pour insert et alter, une colonne et la nouvelle donnée
        """

        if value is None and type(key) == str:
            raise ValueError("Paramètre 'value' manquant dans le where")

        if self.action is None:
            # Si type query, on stocke d'une manière
            if "where" not in self.query:
                self.query["where"] = []

            self.query["where"].append([key, value])

        else:
            # Sinon, d'une autre manière
            if "valeurs" not in self.query:
                self.query["valeurs"] = []

            if type(key) == str:
                self.query["valeurs"].append([key, value])
            else:
                for value in key:
                    self.query["valeurs"].append([value, key[value]])

        return self

    def join(self, new_table: str, first_field: str, second_field: str) -> Model:
        """
        Permet d'effectuer une jointure entre deux tables, seulement applicable pour les query
        """

        # Ajout des clés éventuellement manquantes dans le query
        if "from" not in self.query:
            self.query["from"] = {}

        if "tables" not in self.query["from"]:
            self.query["from"]["tables"] = []

        if "cond" not in self.query["from"]:
            self.query["from"]["cond"] = []

        if new_table not in self.query["from"]["tables"]:
            self.query["from"]["tables"].append(new_table)

        # On ne précise pas la table dans la condition, il est attendu de l'écrivain de le faire lui même
        self.query["from"]["cond"].append([first_field, second_field])

        return self

    def copy(self) -> Model:
        """
        Permet de copier l'objet, de rendre un nouvel objet avec des valeurs identiques au sien
        """
        new_model = Model(self.database)
        # Utilisation de la bibliothèque deep_copy puisque query peut contenir des tableaux ou dictionnaires,
        # Qui ne serait copiés par une approche naïve
        new_model.query = copy.deepcopy(self.query)

        if hasattr(self, "table_name"):
            new_model.table_name = self.table_name

        return new_model

    def insert_default_values(self):
        insert_into_table_name = self.query.get("table")

        class_table = tables.get(insert_into_table_name)

        for key in class_table.__annotations__:
            exists = False

            for value in self.query.get("valeurs", []):
                if key == value[0]:
                    exists = True

            if not exists:
                default_value_function = class_table.__dict__.get(key)

                if isinstance(default_value_function, type(lambda: "")):
                    value = str(default_value_function())
                    self.query.get("valeurs").append([key, value])

                    pk_name = class_table.__dict__.get("primary_key", "id")

                    if key == pk_name:
                        while len(self.new().table(insert_into_table_name)
                                          .where(pk_name, value)
                                          .execute()
                                  ) > 0:
                            value = str(default_value_function())
                            self.query.get("valeurs")[-1][1] = value

    def execute_action(self, commit: bool = True):
        return_value = None

        if self.action == "insert":
            self.insert_default_values()
            pk_name = tables.get(self.query.get("table")).primary_key

            for value in self.query.get("valeurs"):
                if value[0] == pk_name:
                    return_value = value[1]

            self.database.execute(self.query)
        else:
            return_value = self.database.execute(self.query)

        if commit:
            self.database.commit()
        return return_value

    def execute(self, export: bool = True, commit: bool = True) -> Union[list[dict[str, str]], list[Table.Table]]:
        """
        Exécute la requette crée, choisi la bonne méthode si la requête modifiera ou non la BDD

        :param export: Si vrai, renvoie un dictionnaire de valeurs, plutôt qu'un ensemble d'objets
        :param commit: Si les changements doivent ou non être sauvegardés
        """

        if self.action is not None:
            if self.query.get("table").lower() in tables:
                return self.execute_action(commit)
            else:
                return_value = self.database.execute(self.query)

                if commit:
                    self.database.commit()
                return return_value

        parsed_query_response = self.database.query(self.query)

        # Dans le cas d'une query, on transforme la réponse de la requête en l'objet correspondant pour le stocker,
        # Et éventuellement effectuer d'autre actions dessus
        for i in range(len(parsed_query_response)):
            row = parsed_query_response[i]

            # Utilisation de **row pour passer des paramètres nommés et ne pas avoir de soucis d'ordre, et également
            # Permettre de facilement toujours passer le bon nombre de paramètres, peu importe les différences entre
            # Les tables

            parsed_query_response[i] = tables.get(self.table_name)(self.new(), **row)

        if export:
            return [row.export() for row in parsed_query_response]

        return parsed_query_response

    def new(self) -> Model:
        """
        Permet de retourner un nouveau Modèle vide, dans le cas ou un objet partiellement rempli est donné, et qu'une
        ardoise blanche est souhaitée
        """
        return Model(self.database)

    def rec_call(self, query_res: Union[Table, list[Table]], arg, cond: Model = None, *chain_load) -> Table.Table:
        """
        Fonction récursive prenant en compte le chargement de variables successif

        :param query_res: Résultat de la requête précédante, donc les objets sur lequel appliquer le chargement
        :param arg: Nom du paramètre à charger
        :param cond: Requête incomplète
        :param chain_load: Eventuellement des chargements à effectuer à la fin de celui-ci
        """

        if len(chain_load) > 0:
            # S'il y a un chargement à enchainer
            next_table_name = chain_load[0]
            next_cond = None

            # S'il ne s'agit pas d'un str le premier paramètre, alors il s'agit d'une liste contenant une condition
            if type(next_table_name) != str:
                next_table_name = chain_load[0][0]
                next_cond = chain_load[0][1]

        # Si nous n'avons qu'un seul élément, par exemple de un HasOne, on met dans une liste pour parcourir
        if type(query_res) == list:
            iterate_on = query_res
        else:
            iterate_on = [query_res]

        for row in iterate_on:
            # Chargement sur chaque ligne
            row.load(arg, cond)

            if len(chain_load) > 0:
                # Dans le cas d'un enchainement, appel récursif pour le gérer
                self.rec_call(row.__dict__.get(arg.lower(), []), next_table_name, next_cond, *chain_load[1:])

    def rollback(self):
        """
        Permet d'effectuer un rollback sur la BDD

        N'ajoute aucune fonctionalité, offre simplement une porte simple à la connection
        """
        self.database.rollback()

    def commit(self):
        """
        Permet d'effectuer un commit sur la BDD

        N'ajoute aucune fonctionalité, offre simplement une porte simple à la connection
        """
        self.database.commit()

    def load(self, arg, cond: Model = None, *chain_load) -> list[Table.Table]:
        """
        Permet d'effectuer un chargement d'une table liée à celle-ci facilement sans s'embêter à parcourir le résultat
        d'un execute

        :param arg: Nom de la variable déclarée dans la table à charger
        :param cond: Eventuellement une requête (incomplète) sélectionnant les valeurs à retourner ou des conditions
        (select / where)
        :param chain_load: Eventuellement un chargement à effectuer sur le résultat du chargement effectuer
        N'est pas effectué sur la table actuelle.
        """

        # Forcément nous avons un Model, donc il faut exécuter la requête pour continuer
        query_res = self.execute(False)

        # Appel de la fonction récursive
        self.rec_call(query_res, arg, cond, *chain_load)

        return query_res
