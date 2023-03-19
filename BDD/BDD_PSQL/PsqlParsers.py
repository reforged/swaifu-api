from Utils.Erreurs.TablesManquantes import TablesManquantes


def jsonToPsqlQuery(request: dict) -> tuple[str, list[str]]:
    """
    Prends en paramètre un dictionnaire structuré (Voir documentation pour la structure) de type 'Query' et construit
    Une requête SQL à partir de ce dernier et renvoie en complément un dictionnaire contenant les valeurs
    (utilisateurs) à placer dans la requête par psycopg2.
    :param request: Dictionnaire correspondant à une requête SQL
    :return:
    """
    query = "select"
    arg_list = []

    select = request.get("select", [["", "*"]])
    where = request.get("where", {})
    liste_union = request.get("from")

    if liste_union.get("tables") is None:
        raise TablesManquantes("Liste des tables non données")

    liste_tables = liste_union["tables"]
    liste_conditions = liste_union.get("cond", [])

    for selection in select:
        if selection[0] == "":
            query += " *, "
        else:
            query += f"{selection[0]}.{selection[1]}, "

    query = query[:-2] + f" from {', '.join(liste_tables)}"

    if len(where) > 0 or len(liste_conditions) > 0:
        query += " where"

    for condition in liste_conditions:
        query += f" {condition[0][0]}.{condition[0][1]} = {condition[1][0]}.{condition[1][1]} and"

    for condition in where:
        query += f" {condition[0]}.{condition[1]} = %s"
        query += " and"

        arg_list.append(condition[2])

    if len(where) > 0 or len(liste_conditions) > 0:
        # Suppression du 'and' supplémentaire
        query = query[:-3]

    return query, arg_list


def jsonToPsqlExecute(request: dict) -> tuple[str, dict[str]]:
    """
    Prends en paramètre un dictionnaire structuré (Voir documentation pour la structure) de type 'execute' et construit
    Une requête SQL à partir de ce dernier.
    :param request: Dictionnaire correspondant à une requête SQL
    :return:
    """
    query = ""
    arg_list = []

    table = request.get("table")
    valeurs = request.get("valeurs")
    action = request.get("action", "insert")

    if table is None:
        raise TablesManquantes("Liste des tables non données")

    if action == "insert":
        query = f"insert into {table} ("

        for colonne in valeurs:
            query += f"{colonne[0]}, "

        query = query[:-2] + ") values ("

        for colonne in valeurs:
            query += f"%s, "
            arg_list.append(colonne[1])

        query = query[:-2] + ");"

    if action == "delete":
        query = f"delete from {table}"

        if len(valeurs) > 0:
            query += " where"

        for colonne in valeurs:
            query += f" {colonne[0]} = %s and"
            arg_list.append(colonne[1])

        if len(valeurs) > 0:
            query = query[:-4]

    return query, arg_list
