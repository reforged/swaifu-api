from Utils.Types import sql_json_format
from Erreurs.TablesManquantes import TablesManquantes


def jsonToPsqlQuery(request: sql_json_format) -> str:
    """
    Prends en paramètre un dictionnaire structuré (Voir documentation pour la structure) et construit une
    Requête SQL à partir de ce dernier
    :param request:
    :return:
    """
    query = "select"

    select = request.get("select", [["", "*"]])
    where = request.get("where", {})
    liste_union = request.get("from", None)

    if liste_union.get("tables") is None:
        raise TablesManquantes("Liste des tables non données")

    liste_tables = liste_union["tables"]
    liste_conditions = liste_union.get("cond", [])

    for selection in select:
        if selection[0] == "":
            query += " *, "
        else:
            query += f" {selection[0]}.{selection[1]}, "

    query = query[:-2] + f" from {', '.join(liste_tables)}"

    if len(where) > 0 or len(liste_conditions) > 0:
        query += " where"

    for condition in liste_conditions:
        query += f" {condition[0][0]}.{condition[0][1]} = {condition[1][0]}.{condition[1][1]} and"

    for condition in where:
        # Utilisation de ' et non " obligatoire car postgresql
        query += f" {condition[0]}.{condition[1]} = "
        query += str(condition[2]) if (type(condition[2]) == int) else ("'" + condition[2] + "'")
        query += " and"

    if len(where) > 0 or len(liste_conditions) > 0:
        query = query[:-4]

    return query + ";"

