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
    reponses = data.get("reponses", None)
    etiquettes= data.get("etiquettes", None)
    user_id = token['id']

    for object in [label, enonce, type, user_id, reponses, etiquettes]:
        if object is None:
            return make_response(requete_malforme, 400, requete_malforme)

    conflict = True

    while conflict:
        question_id = str(uuid.uuid4())

        verification_query = {
            "where": [
                ["questions", "id", question_id, "and"]
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
            ["id", question_id],
            ["label", label],
            ["enonce", enonce],
            ["type", type],
            ["user_id", user_id],
            ["created_at", datetime.now().astimezone()],
            ["updated_at", datetime.now().astimezone()]
        ]
    }

    database.execute(insert_query)


    for reponse in reponses:
        conflict = True

        body = reponse.get("body", None)
        valide = reponse.get("valide", None)

        if body is None or valide is None:
            return make_response(requete_malforme, 400, requete_malforme)

        while conflict:
            reponse_id = str(uuid.uuid4())

            verification_query = {
                "where": [
                    ["reponses", "id", reponse_id, "and"]
                ],
                "from": {
                    "tables": ["reponses"]
                }
            }

            if len(database.query(verification_query)) == 0:
                conflict = False

        insert_reponse_query = {
            "table": "reponses",
            "action": "insert",
            "valeurs": [
                ["id", reponse_id],
                ["body", body],
                ["valide", bool(valide)],
                ["question_id", question_id],
                ["created_at", datetime.now().astimezone()],
                ["updated_at", datetime.now().astimezone()]
            ]
        }

        database.execute(insert_reponse_query)
        
       
    for etiquette_id in etiquettes:
        conflict = True

        if body is None or valide is None:
            return make_response(requete_malforme, 400, requete_malforme)

        while conflict:
            etiquette_question_id = str(uuid.uuid4())

            verification_query = {
                "where": [
                    ["etiquette_question", "id", etiquette_question_id, "and"]
                ],
                "from": {
                    "tables": ["etiquette_question"]
                }
            }

            if len(database.query(verification_query)) == 0:
                conflict = False

        insert_question_etiquette_query = {
            "table": "etiquette_question",
            "action": "insert",
            "valeurs": [
                ["id", etiquette_question_id],
                ["etiquette_id", etiquette_id],
                ["question_id", question_id],
            ]
        }

        database.execute(insert_question_etiquette_query)
        
        

    database.commit()

    return {"success": "yes"}
