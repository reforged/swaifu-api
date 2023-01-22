def etiquettes(database):
    etiquette_query = {
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(etiquette_query)

