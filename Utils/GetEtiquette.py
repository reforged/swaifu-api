def getEtiquette(database, etiquette_id):
    sql_etiquette_query = {
        "select": [
            ["etiquettes", "id"],
            ["etiquettes", "label"],
            ["etiquettes", "description"],
            ["etiquettes", "color"],
            ["etiquettes", "created_at"],
            ["etiquettes", "updated_at"]
        ],
        "where": [
            ["questions", "id", etiquette_id, "and"]
        ],
        "from": {
            "tables": ["questions", "etiquette_question", "etiquettes"],
            "cond": [
                [
                    ["questions", "id"],
                    ["etiquette_question", "question_id"]
                ],
                [
                    ["etiquette_question", "etiquette_id"],
                    ["etiquettes", "id"]
                ]
            ]
        }
    }

    return database.query(sql_etiquette_query)
