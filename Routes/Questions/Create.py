from Permissions.Policies import check_token
from flask import make_response
from Erreurs.HttpErreurs import token_invalide, requete_malforme
from datetime import datetime
import uuid
from Utils.Route import route


@route(method="post")
def questions_create(database, request):
    token = check_token(request, database)

    if token is None:
        return make_response(token_invalide, 400, token_invalide)

    data = request.get_json()

    label = data.get("label", None)
    enonce = data.get("enonce", None)
    type = data.get("type", None)
    user_id = token['id']

    for object in [label, enonce, type, user_id]:
        if object is None:
            print("AAAAAAAH")
            return make_response(requete_malforme, 400, requete_malforme)

    conflict = True

    while conflict:
        id = str(uuid.uuid4())

        verification_query = {
            "where": [
                ["questions", "id", id, "and"]
            ],
            "from": {
                "tables": ["questions"]
            }
        }

        if len(database.query(verification_query)) == 0:
            conflict = False

    insert_query = {
        "table": "questions",
        "action": "insert",
        "valeurs": [
            ["id", id],
            ["label", label],
            ["enonce", enonce],
            ["type", type],
            ["user_id", user_id],
            ["created_at", datetime.now().astimezone()],
            ["updated_at", datetime.now().astimezone()]
        ]
    }

    database.execute(insert_query)
    database.commit()

    return {"success": "yes"}
