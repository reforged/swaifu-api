from Utils.Route import route
from datetime import datetime
from flask import make_response
from Erreurs.HttpErreurs import token_invalide, requete_malforme
from Permissions.Policies import check_token
import uuid


@route(method="post")
def etiquette_create(database, request):
    token = check_token(request, database)

    if token is None:
        return make_response(token_invalide, 400, token_invalide)

    data = request.get_json()

    label = data.get("label", None)
    description = data.get("description", None)
    color = data.get("color", None)
    user_id = token['id']

    for object in [label, description, color, user_id]:
        if object is None:
            return make_response(requete_malforme, 400, requete_malforme)

    conflict = True

    while conflict:
        id = str(uuid.uuid4())

        verification_query = {
            "where": [
                ["etiquettes", "id", id, "and"]
            ],
            "from": {
                "tables": ["etiquettes"]
            }
        }

        if len(database.query(verification_query)) == 0:
            conflict = False

    insert_query = {
        "table": "etiquettes",
        "action": "insert",
        "valeurs": [
            ["id", id],
            ["label", label],
            ["description", description],
            ["color", color],
            ["created_at", datetime.now().astimezone()],
            ["updated_at", datetime.now().astimezone()]
        ]
    }

    database.execute(insert_query)
    database.commit()

    return {"success": "yes"}
