import Utils.Repeater as Repeater

import BDD.Database as Database
import copy
import BDD.Model as Model
import BDD.Table as Table


class CacheDatabase(Database.Database):
    """
    Système de cache permettant de mettre en mémoire des requêtes dans le but de minimiser les accès à la base de donnée
    """
    # dict containing for each table a list of the table values (dicts)
    tables_dict: dict[str, dict] = {}
    tables_list: dict[str, list] = {}
    tables: dict[str, Table.Table]

    database: Database.Database

    to_commit: list[dict] = []
    stop: bool = False

    def __init__(self, database: Database.Database, tables: dict[str, Table.Table]):
        """
        Initiateur de la classe
        :param database: Connection à la base de donnée, pour lequel cet objet sera l'intermédiaire
        :param tables: Dictionnaire associant à chaque classe de table, leur nom
        """
        self.database = database
        self.query_builder = Model.Model(self.database)
        self.tables = tables

        for key in self.tables:
            self.get_table(key)

        self.repeater = Repeater.RepeatedTimer(300, self.invalidate)

    def __del__(self):
        self.repeater.stop()
        del self

    def invalidate(self):
        """
        Appelée occasionnellement, permet de renouveler les tables en mémoire
        """
        self.renew_cache()

    def renew_cache(self):
        """
        Effectue les appels nécessaires pour stocker une version récente des tables en mémoire
        """
        for key in self.tables:
            self.get_table(key)

    def getPkName(self, table_name):
        """
        Pour le nom d'une table donnée, renvoie le nom de sa clé primaire associée
        :param table_name: Nom de la table désirée
        """
        return self.tables.get(table_name).__dict__.get("primary_key")

    def get_table(self, table_name):
        """
        Récupère dans la base de données la table demandées.
        :param table_name: Nom de la table concernée
        """
        table_name = table_name.lower()
        # Clé primaire nécessaire pour stocker dans le dictionnaire en fonction de cette dernière
        pk_name = self.getPkName(table_name)

        self.tables_list[table_name] = self.query_builder.table(table_name).execute()
        self.tables_dict[table_name] = {row.get(pk_name): row for row in self.tables_list[table_name]}

    def query(self, request):
        """
        Pour une requête donnée, renvoie les données demandées.
        :param request: Dictionnaire correspondant à la requête
        """
        # S'il s'agit d'une requête entre plusieurs tables, so long
        if len(request.get("from", {}).get("tables", [])) != 1:
            return self.database.query(request)

        # Sinon, si on ne veut que certains champs dans la table, on les parcourt afin de s'assurer de gérer le cas où
        # Un champ est précédé par le nom d'une table
        if request.get("select", ["*"])[0] != "*":
            for i in range(len(request.get("select"))):
                request["select"][i] = request["select"][i].split(".")[-1]

        table_name = request.get("from").get("tables")[0].lower()

        # Vérification de si la table est dans le cache
        if table_name not in self.tables_dict.keys():
            print("Not in self list")
            return self.database.query(request)

        # Si aucune condition est posée, on renvoie tout
        if len(request.get("where", [])) == 0:
            print("Where not detected")
            # En respectant les champs sélectionnées, éventuellement
            if request.get("select", ["*"])[0] != "*":
                print(f"Selected ids : {request.get('select')}")
                return [{key: row.get(key) for key in row if key in request.get("select")} for row in self.tables_list.get(table_name)]
            print("Everything selected")
            return copy.deepcopy(self.tables_list.get(table_name))

        # Sinon si on ne filtre que sur un seul champ
        if len(request.get("where")) == 1:
            print("1 where found")
            pk_name = self.getPkName(table_name)
            # Si on filtre sur une clé primaire, l'élément est unique et on utilise le dictionnaire pour immédiatement
            # Renvoyer l'élément demandé
            if request.get("where")[0][0] == pk_name:
                print("Where concerns id")

                filtered = [self.tables_dict.get(table_name).get(request.get("where")[0][1])]

                # SI aucun élément ne correspond à la clé primaire, on renvoie rien
                if filtered == [None]:
                    return []

                # On vérifie les champs demandées, et filtre en fonction
                if request.get("select", ["*"])[0] != "*":
                    print(f"Selected ids : {request.get('select')}")
                    return [{key: row[key] for key in row if key in request.get("select")} for row in filtered]
                return filtered

            else:
                # Sinon la condition est sur une clée non primaire, donc non unique
                print("Where on non primary")
                column, value = request["where"][0]

                # Filtrage avec une bien belle compréhension de listes
                filtered = [row for row in self.tables_list.get(table_name) if row.get(column) == value]

                # Prise en compte des champs sélectionnées
                if request.get("select", ["*"])[0] != "*":
                    print(f"Selected ids : {request.get('select')}")
                    return [{key: row[key] for key in row if key in request.get("select")} for row in filtered]
                return filtered

        print("Query : ", request)

        print("Cannot handle")
        # Si nous atteignons cette étape, alors nous n'avons pas su gérer la requête, et demandons donc à la BDD de s'en
        # Occuper pour nous
        return self.database.query(request)

    def execute(self, request):
        """
        Permet d'exécuter une modification de données sur la BDD
        Aucune action effectuée sur la BDD pour l'instant afin de permettre le rollback et commit
        """
        self.to_commit.append(request)

    def commit_insert(self, nom_table, valeurs):
        """
        Lors d'une insertion de données suite à un commit, gère l'addition des informations aux tables internes
        :param nom_table: Nom de la table concernée
        :param valeurs: Valeurs à ajouter
        """
        pk_name = self.getPkName(nom_table)
        value = {row[0]: row[1] for row in valeurs}

        self.tables_dict[nom_table][value.get(pk_name)] = {value.get(pk_name): value}
        self.tables_list[nom_table].append(value)

    def commit_delete(self, table_name, valeurs):
        """
        Lors d'une suppression de données suite à un commit, gère leur suppression des tables internes
        :param table_name: Nom de la table concernée
        :param valeurs: Conditions de suppresions
        """


        # Obligation de parcourir l'ensemble du tableau, même dans le cas d'une condition sur une clé primaire afin de
        # S'assurer de la bonne mise à jour des deux tables
        affected_table = self.tables_list.get(table_name)

        for i in range(len(affected_table) - 1, -1, -1):
            # On parcourt de la fin du tableau jusqu'au début afin de supprimer des éléments de la liste sans soucis
            row = affected_table[i]
            delete = True

            for condition in valeurs:
                column = condition[0]
                expected_value = condition[1]

                if row[column] != expected_value:
                    delete = False

            if delete:
                pk_name = self.getPkName(table_name)
                id_value = affected_table[i].get(pk_name)

                if id_value in self.tables_dict[table_name]:
                    del self.tables_dict[table_name][id_value]

                del affected_table[i]

    def commit_alter(self, table_name, valeurs, pk_name, pk_value):
        """
        Lors d'une modification de données suite à un commit, gère leur modification sur les tables internes
        :param table_name: Nom de la table concernée
        :param valeurs: Nouvelles valeurs
        :param pk_name: Nom de la clé primaire (Sur laquelle trier)
        :param pk_value: Valeur de la colonne souhaitée
        """

        table_pk_name = self.getPkName(table_name)
        if pk_name != table_pk_name:
            # On examine chaque colonne afin de trouver celles ayant besoin d'être modifiée, avant de les modifier
            affected_table = self.tables_list.get(table_name)

            for row in affected_table:
                if row[pk_name] == pk_value:
                    for couple in valeurs:
                        column = couple[0]
                        new = couple[1]

                        row[column] = new

        else:
            # Si la clé primaire donnée est bien celle de la table, on peut utiliser le dictionnaire pour rapidement
            # Accéder à la donnée souhaitée et la modifier
            affected_table = self.tables_dict.get(table_name)

            for couple in valeurs:
                column = couple[0]
                new = couple[1]

                affected_table[pk_value][column] = new

    def commit(self):
        """
        Simule le commit d'une base de données, en envoyant tout d'un coup afin de gérer si des erreurs se passent entre
        """

        # Pour chaque modification à apporter, on les parcourt et les exécute
        for to_add in self.to_commit:
            self.database.execute(to_add)

        self.database.commit()

        # Une fois la modification sur la base de données appliquée (En cas d'erreurs)
        # On modifie les tables internes
        for to_add in self.to_commit:
            nom_table = to_add.get("table")
            if nom_table in self.tables_list:
                action = to_add.get("action")
                valeurs = to_add.get("valeurs")

                # Appel du handler approprié en fonction de l'action
                if action == "insert":
                    self.commit_insert(nom_table, valeurs)
                elif action == "delete":
                    self.commit_delete(nom_table, valeurs)
                elif action == "alter":
                    pk_name, pk_value = to_add.get("primary")
                    self.commit_alter(nom_table, valeurs, pk_name, pk_value)

        self.to_commit = []

    def lastVal(self):
        # Adapter le code pour l'enlever
        return None

    def rollback(self):
        """
        Annule tout les changements effectués jusqu'au dernier commit
        """
        self.to_commit = []
