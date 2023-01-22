from Utils.Route import route


@route(url="<etiquette_id>")
def etiquette_get_etiquette_id(etiquette_id, database):
    etiquette_query = {
        "where": [
            ["etiquettes", "id", etiquette_id, "and"]
        ],
        "from": {
            "tables": ["etiquettes"]
        }
    }

    return database.query(etiquette_query[0])


@route(method="put", url="<etiquette_id>")
def put_id(etiquette_id, database):
    pass


@route(method="delete", url="<etiquette_id>")
def delete_id(etiquette_id, database):
    question_etiquette_execute = {
        "table": "etiquette_question",
        "action": "delete",
        "valeurs": [
            ["question_id", etiquette_id]
        ]
    }

    etiquette_execute = {
        "table": "etiquettes",
        "action": "delete",
        "valeurs": [
            ["id", etiquette_id]
        ]
    }

    database.execute(question_etiquette_execute)
    database.execute(etiquette_execute)
    database.commit()

    return "yes"
