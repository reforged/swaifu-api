import Utils.Repeater as Repeater

import BDD.Database as Database
import copy
import BDD.Model as Model
import BDD.Table as Table


class CacheDatabase(Database.Database):
    # dict containing for each table a list of the table values (dicts)
    tables_dict = {}
    tables_list = {}
    tables: dict[str, Table.Table]

    database: Database.Database

    to_commit = []
    stop = False

    def __init__(self, database: Database.Database, tables: dict[str, Table.Table]):
        self.database = database
        self.query_builder = Model.Model(self.database)
        self.tables = tables
        # {object: tables[object] for object in tables if issubclass(tables[object], Table.Table)}

        for key in self.tables:
            self.get_table(key)

        self.repeater = Repeater.RepeatedTimer(300, self.invalidate)

    def __del__(self):
        self.repeater.stop()
        del self

    def invalidate(self):
        print("Cache renewed")

        self.renew_cache()

    def renew_cache(self):
        for key in self.tables:
            self.get_table(key)

    def getPkName(self, table_name):
        return self.tables.get(table_name).__dict__.get("primary_key")

    def get_table(self, table_name):
        table_name = table_name.lower()
        pk_name = self.getPkName(table_name)

        self.tables_list[table_name] = self.query_builder.table(table_name).execute()
        self.tables_dict[table_name] = {row.get(pk_name): row for row in self.tables_list[table_name]}

    def query(self, request):
        if len(request.get("from", {}).get("tables", [])) != 1:
            return self.database.query(request)

        if request.get("select", ["*"])[0] != "*":
            for i in range(len(request.get("select"))):
                request["select"][i] = request["select"][i].split(".")[-1]

        table_name = request.get("from").get("tables")[0].lower()

        if table_name not in self.tables_dict.keys():
            print("Not in self list")
            return self.database.query(request)

        if len(request.get("where", [])) == 0:
            print("Where not detected")
            if request.get("select", ["*"])[0] != "*":
                print(f"Selected ids : {request.get('select')}")
                return [{key: row.get(key) for key in row if key in request.get("select")} for row in self.tables_list.get(table_name)]
            print("Everything selected")
            return copy.deepcopy(self.tables_list.get(table_name))

        if len(request.get("where")) == 1:
            print("1 where found")
            pk_name = self.getPkName(table_name)
            if request.get("where")[0][0] == pk_name:
                print("Where concerns id")

                filtered = [self.tables_dict.get(table_name).get(request.get("where")[0][1])]

                if filtered == [None]:
                    return []

                if request.get("select", ["*"])[0] != "*":
                    print(f"Selected ids : {request.get('select')}")
                    return [{key: row[key] for key in row if key in request.get("select")} for row in filtered]
                return filtered

            else:
                print("Where on non primary")
                column, value = request["where"][0]

                filtered = [row for row in self.tables_list.get(table_name) if row.get(column) == value]

                if request.get("select", ["*"])[0] != "*":
                    print(f"Selected ids : {request.get('select')}")
                    return [{key: row[key] for key in row if key in request.get("select")} for row in filtered]
                return filtered

        print("Query : ", request)

        print("Cannot handle")

        return self.database.query(request)

    def execute(self, request):
        self.to_commit.append(request)

    def commit_insert(self, nom_table, valeurs):
        pk_name = self.getPkName(nom_table)
        value = {row[0]: row[1] for row in valeurs}

        self.tables_dict[nom_table][value.get(pk_name)] = {value.get(pk_name): value}
        self.tables_list[nom_table].append(value)

    def commit_delete(self, table_name, valeurs):
        affected_table = self.tables_list.get(table_name)

        for i in range(len(affected_table) - 1, -1, -1):
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

        # self.tables_dict[table_name] = {row["id"]: row for row in self.tables_list[table_name]}

    def commit_alter(self, table_name, valeurs, pk_name, pk_value):
        table_pk_name = self.getPkName(table_name)
        if pk_name != table_pk_name:
            affected_table = self.tables_list.get(table_name)

            for row in affected_table:
                if row[pk_name] == pk_value:
                    for couple in valeurs:
                        column = couple[0]
                        new = couple[1]

                        row[column] = new

        else:
            affected_table = self.tables_dict.get(table_name)

            for couple in valeurs:
                column = couple[0]
                new = couple[1]

                affected_table[pk_value][column] = new

    def commit(self):
        for to_add in self.to_commit:
            self.database.execute(to_add)

        self.database.commit()

        for to_add in self.to_commit:
            nom_table = to_add.get("table")
            if nom_table in self.tables_list:
                action = to_add.get("action")
                valeurs = to_add.get("valeurs")

                if action == "insert":
                    self.commit_insert(nom_table, valeurs)
                elif action == "delete":
                    self.commit_delete(nom_table, valeurs)
                elif action == "alter":
                    pk_name, pk_value = to_add.get("primary")
                    self.commit_alter(nom_table, valeurs, pk_name, pk_value)

        self.to_commit = []

    def lastVal(self):
        return None

    def rollback(self):
        self.to_commit = []
