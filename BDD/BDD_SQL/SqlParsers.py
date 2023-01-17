from typing import *


def jsonToSql(request: dict[str, Union[list[list[str]], dict[str, list[Union[str, list[str]]]]]]) -> str:
    query = "select"

    select = request.get("select", [["", "*"]])
    where = request.get("where", {})
    liste_union = request.get("from", None)

    if liste_union is None:
        # TODO: Erreur custom plus adaptée
        raise TypeError("Liste des tables non données")

    liste_tables = liste_union["tables"]
    liste_conditions = liste_union.get("cond", [])

    for selectionneur in select:
        if selectionneur[0] == "":
            query = " * , "
        else:
            query += f" {selectionneur[0]}.{selectionneur[1]}, "

    query = query[:-2] + f" from {', '.join(liste_tables)}"

    if len(where) > 0 or len(liste_conditions) > 0:
        query += " where"

    for condition in liste_conditions:
        query += f" {condition[0][0]}.{condition[0][1]} = {condition[1][0]}.{condition[1][1]} and"

    for condition in where:
        query += f" {condition[0]}.{condition[1]} = "
        query += str(condition[2]) if (type(condition[2]) == int) else ('"' + condition[2] + '"')
        query += " and"

    if len(where) > 0:
        query = query[:-4]

    return query + ";"
